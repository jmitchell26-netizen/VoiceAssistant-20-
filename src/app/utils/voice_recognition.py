import speech_recognition as sr
import pyttsx3
from PyQt6.QtCore import QObject, pyqtSignal, QThread
import queue
import sounddevice as sd
import numpy as np

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

    def setup_audio_processing(self):
        """Set up audio processing parameters"""
        self.sample_rate = 16000
        self.block_size = 1024
        self.audio_threshold = 0.01

    def start_listening(self):
        """Start listening for audio input"""
        if not self.is_listening:
            self.is_listening = True
            self.state_changed.emit("listening")
            self._start_audio_stream()

    def stop_listening(self):
        """Stop listening for audio input"""
        if self.is_listening:
            self.is_listening = False
            self.state_changed.emit("stopped")
            # Audio stream will be closed in the stream callback

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
                self.audio_queue.put(bytes(indata))

    def process_audio(self):
        """Process audio data from queue"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                self.text_received.emit(text)
        except sr.UnknownValueError:
            self.error_occurred.emit("Could not understand audio")
        except sr.RequestError as e:
            self.error_occurred.emit(f"Error with speech recognition service: {str(e)}")

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
