import speech_recognition as sr
import pyttsx3
from PyQt6.QtCore import QObject, pyqtSignal
import pyaudio
import numpy as np

class VoiceRecognitionManager(QObject):
    text_received = pyqtSignal(str)
    partial_text_received = pyqtSignal(str)  # For real-time transcription preview
    error_occurred = pyqtSignal(str)
    audio_level = pyqtSignal(float)
    state_changed = pyqtSignal(str)  # States: ready, listening, processing, speaking, error

    def __init__(self, settings_manager=None):
        super().__init__()
        print("\nInitializing Voice Recognition Manager...")
        
        self.settings_manager = settings_manager
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.microphone = None
        self.stop_listening_callback = None
        self.audio = pyaudio.PyAudio()
        self.level_stream = None  # Separate stream for audio level monitoring
        
        # Load settings from settings_manager or use defaults
        if self.settings_manager:
            energy_threshold = self.settings_manager.get_setting('voice_recognition', 'energy_threshold')
            pause_threshold = self.settings_manager.get_setting('voice_recognition', 'pause_threshold')
            dynamic_energy_threshold = self.settings_manager.get_setting('voice_recognition', 'dynamic_energy_threshold')
            dynamic_energy_adjustment_damping = self.settings_manager.get_setting('voice_recognition', 'dynamic_energy_adjustment_damping')
            dynamic_energy_ratio = self.settings_manager.get_setting('voice_recognition', 'dynamic_energy_ratio')
            phrase_threshold = self.settings_manager.get_setting('voice_recognition', 'phrase_threshold')
            non_speaking_duration = self.settings_manager.get_setting('voice_recognition', 'non_speaking_duration')
        else:
            # Use optimal defaults from testing
            energy_threshold = 150
            pause_threshold = 0.8
            dynamic_energy_threshold = True
            dynamic_energy_adjustment_damping = 0.15
            dynamic_energy_ratio = 1.5
            phrase_threshold = 0.2
            non_speaking_duration = 0.5
        
        # Apply optimal settings from testing
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy_threshold
        self.recognizer.dynamic_energy_adjustment_damping = dynamic_energy_adjustment_damping
        self.recognizer.dynamic_energy_ratio = dynamic_energy_ratio
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.phrase_threshold = phrase_threshold
        self.recognizer.non_speaking_duration = non_speaking_duration
        
        # Audio settings optimized for your microphone
        self.RATE = 44100  # Higher quality sample rate for better recognition
        self.CHUNK = 2048  # Larger chunks for smoother processing
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.AUDIO_THRESHOLD = 0.1  # Adjusted for your audio levels
        self.GAIN = 0.2  # Reduced gain since we're getting strong input
        
        print("Recognition settings configured:")
        print(f"- Energy threshold: {self.recognizer.energy_threshold}")
        print(f"- Pause threshold: {self.recognizer.pause_threshold}")
        print(f"- Dynamic energy threshold: {self.recognizer.dynamic_energy_threshold}")
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
                
                # Initialize microphone
                print("Initializing microphone...")
                self.microphone = sr.Microphone(sample_rate=self.RATE)
                
                # Calibrate for ambient noise
                with self.microphone as source:
                    print("\nCalibrating for ambient noise... Please be quiet.")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    print(f"Calibration complete. Energy threshold now: {self.recognizer.energy_threshold}")
                
                # Start listening in background (like the test version)
                print("Starting background listening...")
                self.stop_listening_callback = self.recognizer.listen_in_background(
                    self.microphone,
                    self._audio_callback,
                    phrase_time_limit=None  # No limit on phrase length
                )
                
                # Start audio level monitoring stream
                self._start_level_monitoring()
                
                print("Listening started successfully")
                self.error_occurred.emit("Ready to listen - speak normally")
                
            except Exception as e:
                print(f"Error starting audio: {str(e)}")
                import traceback
                traceback.print_exc()
                self.error_occurred.emit(f"Error starting audio: {str(e)}")
                self.stop_listening()

    def stop_listening(self):
        if self.is_listening:
            print("Stopping audio listening...")
            self.is_listening = False
            self.state_changed.emit("ready")
            
            # Stop background listening
            if self.stop_listening_callback:
                try:
                    self.stop_listening_callback(wait_for_stop=False)
                except Exception as e:
                    print(f"Error stopping background listener: {str(e)}")
                self.stop_listening_callback = None
            
            # Stop level monitoring
            self._stop_level_monitoring()
            
            self.microphone = None
            print("Audio cleanup complete")
            self.error_occurred.emit("Stopped listening")

    def _audio_callback(self, recognizer, audio):
        """Callback for listen_in_background - handles recognized audio"""
        if not self.is_listening:
            return
            
        try:
            # Calculate audio level for UI display
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            audio_level = float(np.max(np.abs(audio_data))) / 32768.0
            self.audio_level.emit(audio_level)
            
            # Emit processing state (yellow indicator)
            self.state_changed.emit("processing")
            
            # Show typing indicator while processing
            self.partial_text_received.emit("...")
            
            # Try to recognize speech
            print("Attempting speech recognition...")
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                print(f"Successfully recognized: {text}")
                
                # Clear partial text and emit final text
                self.partial_text_received.emit("")
                self.text_received.emit(text)
                
                # Return to listening state
                self.state_changed.emit("listening")
            except sr.UnknownValueError:
                print("Speech not recognized")
                self.partial_text_received.emit("")
                self.state_changed.emit("listening")
            except sr.RequestError as e:
                print(f"Recognition error: {str(e)}")
                self.partial_text_received.emit("")
                self.state_changed.emit("error")
                self.error_occurred.emit(f"Recognition error: {str(e)}")
                
        except Exception as e:
            print(f"Error in audio callback: {str(e)}")
            import traceback
            traceback.print_exc()
            self.partial_text_received.emit("")
            self.state_changed.emit("error")
            self.error_occurred.emit(f"Error processing audio: {str(e)}")
    
    def _level_monitoring_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio level monitoring stream"""
        if not self.is_listening:
            return (None, pyaudio.paComplete)
        
        try:
            # Convert audio data to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            # Calculate audio level (normalize to 0-1)
            audio_level = float(np.max(np.abs(audio_data))) / 32768.0
            self.audio_level.emit(audio_level)
            
            return (None, pyaudio.paContinue)
        except Exception as e:
            return (None, pyaudio.paContinue)
    
    def _start_level_monitoring(self):
        """Start a separate audio stream for level monitoring"""
        try:
            default_device = self.audio.get_default_input_device_info()
            self.level_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.RATE,
                input=True,
                input_device_index=default_device.get('index'),
                frames_per_buffer=self.CHUNK,
                stream_callback=self._level_monitoring_callback
            )
            self.level_stream.start_stream()
        except Exception as e:
            print(f"Warning: Could not start level monitoring: {str(e)}")
    
    def _stop_level_monitoring(self):
        """Stop the audio level monitoring stream"""
        if self.level_stream:
            try:
                self.level_stream.stop_stream()
                self.level_stream.close()
            except Exception as e:
                print(f"Error stopping level monitoring: {str(e)}")
            self.level_stream = None

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
            self.state_changed.emit("speaking")
            self.engine.say(text)
            self.engine.runAndWait()
            if self.is_listening:
                self.state_changed.emit("listening")
            else:
                self.state_changed.emit("ready")
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            self.state_changed.emit("error")
            self.error_occurred.emit(f"Error speaking text: {str(e)}")

    def cleanup(self):
        print("Cleaning up voice recognition resources...")
        self.stop_listening()
        if self.audio:
            self.audio.terminate()

    def __del__(self):
        self.cleanup()