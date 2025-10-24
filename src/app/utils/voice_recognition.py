import speech_recognition as sr
import pyttsx3
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import pyaudio
import wave
import numpy as np
import time
import queue

class VoiceRecognitionManager(QObject):
    text_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    audio_level = pyqtSignal(float)
    state_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        print("\nInitializing Voice Recognition Manager...")
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.audio_buffer = queue.Queue()
        
        # Adjusted settings for high audio levels
        self.recognizer.energy_threshold = 4000  # Higher threshold since we're getting strong input
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.2
        self.recognizer.pause_threshold = 0.6  # Longer pause to get complete phrases
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.4
        
        # Audio settings optimized for your microphone
        self.RATE = 16000  # Standard rate for speech recognition
        self.CHUNK = 1024  # Smaller chunks for more frequent processing
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.AUDIO_THRESHOLD = 0.1  # Adjusted for your audio levels
        self.GAIN = 0.2  # Reduced gain since we're getting strong input
        
        print("Recognition settings configured:")
        print(f"- Energy threshold: {self.recognizer.energy_threshold}")
        print(f"- Audio threshold: {self.AUDIO_THRESHOLD}")
        print(f"- Gain: {self.GAIN}")
        print(f"- Sample rate: {self.RATE}")
        
        self.list_audio_devices()

    def list_audio_devices(self):
        print("\n=== Available Audio Input Devices ===")
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        
        for i in range(0, numdevices):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                print(f"Device {i}: {device_info.get('name')}")
                print(f"  Max Input Channels: {device_info.get('maxInputChannels')}")
                print(f"  Default Sample Rate: {device_info.get('defaultSampleRate')}")
                if device_info.get('index') == self.audio.get_default_input_device_info().get('index'):
                    print("  ^^^ DEFAULT INPUT DEVICE ^^^")
        print("=====================================\n")

    def start_listening(self):
        if not self.is_listening:
            try:
                print("\nStarting voice recognition...")
                self.is_listening = True
                self.state_changed.emit("listening")
                
                # Get default input device
                default_device = self.audio.get_default_input_device_info()
                print(f"Using input device: {default_device.get('name')}")
                
                # Initialize microphone with PyAudio
                self.stream = self.audio.open(
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    input_device_index=default_device.get('index'),
                    frames_per_buffer=self.CHUNK,
                    stream_callback=self._audio_callback
                )
                
                self.stream.start_stream()
                print("Audio stream started successfully")
                
                # Initialize recognizer with microphone
                with sr.Microphone(sample_rate=self.RATE) as source:
                    print("\nCalibrating for ambient noise... Please be quiet.")
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    print(f"Calibration complete. Energy threshold now: {self.recognizer.energy_threshold}")
                
                self.error_occurred.emit("Ready to listen - speak normally")
                
            except Exception as e:
                print(f"Error starting audio: {str(e)}")
                self.error_occurred.emit(f"Error starting audio: {str(e)}")
                self.stop_listening()

    def stop_listening(self):
        if self.is_listening:
            print("Stopping audio listening...")
            self.is_listening = False
            self.state_changed.emit("stopped")
            
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except Exception as e:
                    print(f"Error closing stream: {str(e)}")
                self.stream = None
            
            while not self.audio_buffer.empty():
                try:
                    self.audio_buffer.get_nowait()
                except queue.Empty:
                    break
            
            print("Audio cleanup complete")
            self.error_occurred.emit("Stopped listening")

    def _audio_callback(self, in_data, frame_count, time_info, status):
        if not self.is_listening:
            return (None, pyaudio.paComplete)
            
        try:
            # Convert audio data to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            
            # Normalize the audio (reduce very high levels)
            audio_data = np.clip(audio_data, -1.0, 1.0)
            
            # Apply gain (reduced since we have strong input)
            audio_data = audio_data * self.GAIN
            
            # Calculate audio level
            audio_level = float(np.max(np.abs(audio_data)))
            self.audio_level.emit(audio_level)
            
            # If we detect sound above threshold
            if audio_level > self.AUDIO_THRESHOLD:
                print(f"Audio detected - Level: {audio_level:.4f}")
                # Store normalized audio
                self.audio_buffer.put(audio_data.tobytes())
                
                # Process audio if we have enough data
                if self.audio_buffer.qsize() >= 8:  # About 0.5 seconds of audio
                    try:
                        print("Processing audio chunk...")
                        # Combine audio data
                        audio_data = b''
                        while not self.audio_buffer.empty():
                            audio_data += self.audio_buffer.get()
                        
                        # Convert to AudioData object
                        audio = sr.AudioData(audio_data, self.RATE, 4)
                        
                        # Try recognition with multiple attempts
                        print("Attempting speech recognition...")
                        try:
                            text = self.recognizer.recognize_google(audio, language='en-US')
                            print(f"Successfully recognized: {text}")
                            self.text_received.emit(text)
                        except sr.UnknownValueError:
                            # Try again with adjusted settings
                            try:
                                self.recognizer.energy_threshold = int(self.recognizer.energy_threshold * 0.8)
                                print(f"Retrying with energy threshold: {self.recognizer.energy_threshold}")
                                text = self.recognizer.recognize_google(audio, language='en-US')
                                print(f"Second attempt succeeded: {text}")
                                self.text_received.emit(text)
                            except sr.UnknownValueError:
                                print("\nSpeech not recognized. Please try:")
                                print("1. Speaking clearly and at a normal pace")
                                print("2. Using simple test phrases like 'test' or 'hello'")
                                print("3. Waiting a moment before speaking")
                                print(f"Current audio level: {audio_level:.4f}")
                        
                    except sr.RequestError as e:
                        print(f"Recognition error: {str(e)}")
                        self.error_occurred.emit(f"Recognition error: {str(e)}")
            
            return (None, pyaudio.paContinue)
            
        except Exception as e:
            print(f"Error in audio callback: {str(e)}")
            self.error_occurred.emit(f"Error processing audio: {str(e)}")
            return (None, pyaudio.paContinue)

    def update_sensitivity(self, value):
        try:
            self.recognizer.energy_threshold = value
            print(f"Sensitivity updated to: {value}")
            self.error_occurred.emit(f"Sensitivity set to {value}")
        except Exception as e:
            print(f"Error updating sensitivity: {str(e)}")
            self.error_occurred.emit(f"Error updating sensitivity: {str(e)}")

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            self.error_occurred.emit(f"Error speaking text: {str(e)}")

    def cleanup(self):
        print("Cleaning up voice recognition resources...")
        self.stop_listening()
        if self.audio:
            self.audio.terminate()

    def __del__(self):
        self.cleanup()