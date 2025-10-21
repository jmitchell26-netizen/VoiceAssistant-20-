import speech_recognition as sr
import pyttsx3
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import queue
import sounddevice as sd
import numpy as np
import threading
import time

class AudioProcessingThread(QThread):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.running = True

    def run(self):
        while self.running:
            if not self.manager.audio_queue.empty():
                audio_data = []
                # Collect audio data for 1 second
                start_time = time.time()
                while time.time() - start_time < 1.0:
                    if not self.manager.audio_queue.empty():
                        audio_data.extend(self.manager.audio_queue.get())
                if audio_data:
                    self.manager.process_audio_data(bytes(audio_data))
            time.sleep(0.1)

    def stop(self):
        self.running = False

class VoiceRecognitionManager(QObject):
    text_received = pyqtSignal(str)  # Emitted when new text is recognized
    error_occurred = pyqtSignal(str)  # Emitted when an error occurs
    audio_level = pyqtSignal(float)   # Emitted to update audio level visualization
    state_changed = pyqtSignal(str)   # Emitted when recognition state changes

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.setup_audio_processing()
        
        # Set default recognition settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
        # Initialize processing thread
        self.processing_thread = None

    def load_recognition_settings(self):
        """Load recognition settings from settings manager"""
        settings = self.settings_manager.get_setting('voice_recognition', {})
        self.recognizer.energy_threshold = settings.get('energy_threshold', 300)
        self.recognizer.dynamic_energy_threshold = settings.get('dynamic_energy_threshold', True)
        self.recognizer.pause_threshold = settings.get('pause_threshold', 0.8)
        self.recognizer.phrase_threshold = settings.get('phrase_threshold', 0.3)
        self.audio_threshold = settings.get('audio_threshold', 0.01)

    def save_recognition_settings(self):
        """Save current recognition settings"""
        settings = {
            'energy_threshold': self.recognizer.energy_threshold,
            'dynamic_energy_threshold': self.recognizer.dynamic_energy_threshold,
            'pause_threshold': self.recognizer.pause_threshold,
            'phrase_threshold': self.recognizer.phrase_threshold,
            'audio_threshold': self.audio_threshold
        }
        self.settings_manager.update_setting('voice_recognition', settings)

    def setup_audio_processing(self):
        """Set up audio processing parameters"""
        self.sample_rate = 16000
        self.block_size = 1024
        self.audio_threshold = self.settings_manager.get_setting(
            'voice_recognition', 'audio_threshold') or 0.01

    def start_listening(self):
        """Start listening for audio input"""
        if not self.is_listening:
            self.is_listening = True
            self.state_changed.emit("listening")
            
            # Start processing thread
            if self.processing_thread is None or not self.processing_thread.isRunning():
                self.processing_thread = AudioProcessingThread(self)
                self.processing_thread.start()
            
            self._start_audio_stream()

    def stop_listening(self):
        """Stop listening for audio input"""
        if self.is_listening:
            self.is_listening = False
            self.state_changed.emit("stopped")
            
            # Stop processing thread
            if self.processing_thread and self.processing_thread.isRunning():
                self.processing_thread.stop()
                self.processing_thread.wait()
            
            # Close audio stream
            if hasattr(self, 'stream'):
                self.stream.stop()
                self.stream.close()

    def _start_audio_stream(self):
        """Start the audio input stream"""
        try:
            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                callback=self._audio_callback
            )
            self.stream.start()
        except Exception as e:
            self.error_occurred.emit(f"Error starting audio stream: {str(e)}")

    def _audio_callback(self, indata, frames, time, status):
        """Process incoming audio data"""
        if status:
            self.error_occurred.emit(str(status))
        if self.is_listening:
            # Calculate audio level for visualization
            audio_level = np.max(np.abs(indata))
            self.audio_level.emit(float(audio_level))

            # Add audio data to queue for processing
            if audio_level > self.audio_threshold:
                self.audio_queue.put(indata.tobytes())

    def process_audio_data(self, audio_data):
        """Process collected audio data"""
        try:
            # Convert audio data to AudioData object
            audio = sr.AudioData(audio_data, self.sample_rate, 2)
            # Perform recognition
            text = self.recognizer.recognize_google(audio)
            self.text_received.emit(text)
        except sr.UnknownValueError:
            pass  # Ignore unrecognized audio
        except sr.RequestError as e:
            self.error_occurred.emit(f"Error with speech recognition service: {str(e)}")

    def update_sensitivity(self, value):
        """Update microphone sensitivity"""
        self.recognizer.energy_threshold = value
        self.save_recognition_settings()
        self.error_occurred.emit(f"Microphone sensitivity updated to {value}")

    def speak(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.error_occurred.emit(f"Error speaking text: {str(e)}")

class VoiceTypingMode:
    """Handles voice typing specific functionality"""
    def __init__(self, voice_manager):
        self.voice_manager = voice_manager
        self.is_active = False
        self.setup_punctuation_commands()
        self.last_text = ""  # Store last processed text for undo

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