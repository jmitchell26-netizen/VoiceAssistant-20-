import speech_recognition as sr
import pyttsx3
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import queue
import sounddevice as sd
import numpy as np
import threading
import time
import pyaudio

class AudioProcessingThread(QThread):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.running = False

    def run(self):
        self.running = True
        while self.running and self.manager.is_listening:
            if not self.manager.audio_queue.empty():
                audio_data = []
                start_time = time.time()
                while time.time() - start_time < 1.0:
                    if not self.manager.audio_queue.empty():
                        audio_data.extend(self.manager.audio_queue.get())
                if audio_data:
                    self.manager.process_audio_data(bytes(audio_data))
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.wait()

class VoiceRecognitionManager(QObject):
    text_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    audio_level = pyqtSignal(float)
    state_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.stream = None
        self.processing_thread = None
        
        # Recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.audio_threshold = 0.01
        
        # Audio settings
        self.sample_rate = 44100
        self.block_size = 2048
        
        # Initialize microphone
        try:
            with sr.Microphone() as source:
                print("Initializing microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone initialized")
        except Exception as e:
            print(f"Error initializing microphone: {str(e)}")
            self.error_occurred.emit(f"Error initializing microphone: {str(e)}")

    def __del__(self):
        """Cleanup when object is destroyed"""
        self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up voice recognition resources...")
        self.stop_listening()
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

    def start_listening(self):
        """Start listening for audio input"""
        if not self.is_listening:
            try:
                self.is_listening = True
                self.state_changed.emit("listening")
                print("Starting audio listening...")
                
                # Start processing thread
                if self.processing_thread is None or not self.processing_thread.isRunning():
                    self.processing_thread = AudioProcessingThread(self)
                    self.processing_thread.start()
                
                self._start_audio_stream()
                print("Audio stream started successfully")
            except Exception as e:
                print(f"Error in start_listening: {str(e)}")
                self.error_occurred.emit(f"Error starting listening: {str(e)}")
                self.stop_listening()

    def stop_listening(self):
        """Stop listening for audio input"""
        print("Stopping audio listening...")
        self.is_listening = False
        self.state_changed.emit("stopped")
        
        # Stop processing thread
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
            self.processing_thread = None
        
        # Close audio stream
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            except Exception as e:
                print(f"Error closing audio stream: {str(e)}")
        
        # Clear audio queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                pass

    def _start_audio_stream(self):
        """Start the audio input stream"""
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None

            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                callback=self._audio_callback,
                dtype=np.float32
            )
            self.stream.start()
        except Exception as e:
            print(f"Error starting audio stream: {str(e)}")
            self.error_occurred.emit(f"Error starting audio stream: {str(e)}")
            self.stop_listening()

    def _audio_callback(self, indata, frames, time, status):
        """Process incoming audio data"""
        if not self.is_listening:
            return
            
        try:
            if status:
                print(f"Audio callback status: {status}")
            
            # Calculate audio level for visualization
            audio_level = float(np.max(np.abs(indata)))
            self.audio_level.emit(audio_level)

            # Add audio data to queue if above threshold
            if audio_level > self.audio_threshold:
                self.audio_queue.put(indata.tobytes())
                
        except Exception as e:
            print(f"Error in audio callback: {str(e)}")
            self.error_occurred.emit(f"Error processing audio: {str(e)}")

    def process_audio_data(self, audio_data):
        """Process collected audio data"""
        if not self.is_listening:
            return
            
        try:
            # Convert audio data to AudioData object
            audio = sr.AudioData(audio_data, self.sample_rate, 2)
            
            # Perform recognition
            text = self.recognizer.recognize_google(audio, language='en-US')
            print(f"Recognized text: {text}")
            self.text_received.emit(text)
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results: {str(e)}")
            self.error_occurred.emit(f"Error with speech recognition service: {str(e)}")
        except Exception as e:
            print(f"Error processing audio data: {str(e)}")
            self.error_occurred.emit(f"Error processing audio: {str(e)}")

    def update_sensitivity(self, value):
        """Update microphone sensitivity"""
        try:
            self.recognizer.energy_threshold = value
            print(f"Sensitivity updated to: {value}")
        except Exception as e:
            print(f"Error updating sensitivity: {str(e)}")
            self.error_occurred.emit(f"Error updating sensitivity: {str(e)}")

    def speak(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            self.error_occurred.emit(f"Error speaking text: {str(e)}")

class VoiceTypingMode:
    """Handles voice typing specific functionality"""
    def __init__(self, voice_manager):
        self.voice_manager = voice_manager
        self.is_active = False
        self.setup_punctuation_commands()
        self.last_text = ""

    def setup_punctuation_commands(self):
        """Set up voice commands for punctuation"""
        self.punctuation_commands = {
            "period": ".",
            "comma": ",",
            "question mark": "?",
            "exclamation mark": "!",
            "new line": "\n",
            "new paragraph": "\n\n",
            "semicolon": ";",
            "colon": ":",
            "open parenthesis": "(",
            "close parenthesis": ")",
            "hyphen": "-",
            "dash": " - ",
        }

    def process_text(self, text):
        """Process recognized text for voice typing"""
        # Store current text for undo
        self.last_text = text

        # Check for special commands first
        if text.lower() == "undo that":
            return self._handle_undo()

        # Check for punctuation commands
        for command, punctuation in self.punctuation_commands.items():
            text = text.replace(f" {command}", punctuation)
        
        # Handle basic formatting commands
        text = self._handle_formatting_commands(text)
        
        return text

    def _handle_formatting_commands(self, text):
        """Handle basic text formatting commands"""
        commands = {
            "capitalize that": lambda t: t.capitalize(),
            "all caps": lambda t: t.upper(),
            "lowercase": lambda t: t.lower(),
            "delete that": lambda t: "",
        }

        for command, action in commands.items():
            if text.lower().startswith(command):
                return action(text[len(command):].strip())
        
        return text

    def _handle_undo(self):
        """Handle undo command"""
        return ""  # Clear last input