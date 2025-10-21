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
        
        # Set default recognition settings
        self.recognizer.energy_threshold = 1000  # Increased for better detection
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Reduced for faster response
        self.recognizer.phrase_threshold = 0.3
        self.audio_threshold = 0.005  # Reduced for better sensitivity
        
        # Initialize microphone
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Microphone initialized and adjusted for ambient noise")
        except Exception as e:
            print(f"Error initializing microphone: {str(e)}")
            self.error_occurred.emit(f"Error initializing microphone: {str(e)}")
        
        # Initialize processing thread
        self.processing_thread = None
        
        # Initialize audio parameters
        self.setup_audio_processing()

    def setup_audio_processing(self):
        """Set up audio processing parameters"""
        self.sample_rate = 44100  # Standard audio rate
        self.block_size = 2048    # Increased for better quality
        
        # List available audio devices
        print("\nAvailable Audio Devices:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"Device {i}: {device['name']} (inputs: {device['max_input_channels']}, outputs: {device['max_output_channels']})")
        
        # Try to find default input device
        try:
            default_device = sd.query_devices(kind='input')
            print(f"\nDefault Input Device: {default_device['name']}")
        except Exception as e:
            print(f"Error finding default input device: {str(e)}")

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

    def stop_listening(self):
        """Stop listening for audio input"""
        if self.is_listening:
            try:
                self.is_listening = False
                self.state_changed.emit("stopped")
                print("Stopping audio listening...")
                
                # Stop processing thread
                if self.processing_thread and self.processing_thread.isRunning():
                    self.processing_thread.stop()
                    self.processing_thread.wait()
                
                # Close audio stream
                if hasattr(self, 'stream'):
                    self.stream.stop()
                    self.stream.close()
                print("Audio stream stopped successfully")
            except Exception as e:
                print(f"Error in stop_listening: {str(e)}")
                self.error_occurred.emit(f"Error stopping listening: {str(e)}")

    def _start_audio_stream(self):
        """Start the audio input stream"""
        try:
            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.block_size,
                callback=self._audio_callback,
                dtype=np.float32
            )
            self.stream.start()
            print("Audio stream initialized successfully")
        except Exception as e:
            print(f"Error starting audio stream: {str(e)}")
            self.error_occurred.emit(f"Error starting audio stream: {str(e)}")

    def _audio_callback(self, indata, frames, time, status):
        """Process incoming audio data"""
        try:
            if status:
                print(f"Audio callback status: {status}")
                self.error_occurred.emit(str(status))
            if self.is_listening:
                # Calculate audio level for visualization
                audio_level = float(np.max(np.abs(indata)))
                self.audio_level.emit(audio_level)
                print(f"Audio level: {audio_level}")

                # Add audio data to queue for processing if above threshold
                if audio_level > self.audio_threshold:
                    self.audio_queue.put(indata.tobytes())
                    print("Audio data queued for processing")
        except Exception as e:
            print(f"Error in audio callback: {str(e)}")
            self.error_occurred.emit(f"Error processing audio: {str(e)}")

    def process_audio_data(self, audio_data):
        """Process collected audio data"""
        try:
            # Convert audio data to AudioData object
            audio = sr.AudioData(audio_data, self.sample_rate, 2)
            print("Processing audio data...")
            
            # Perform recognition
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            self.text_received.emit(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
            pass  # Ignore unrecognized audio
        except sr.RequestError as e:
            print(f"Speech recognition service error: {str(e)}")
            self.error_occurred.emit(f"Error with speech recognition service: {str(e)}")
        except Exception as e:
            print(f"Error processing audio data: {str(e)}")
            self.error_occurred.emit(f"Error processing audio: {str(e)}")

    def update_sensitivity(self, value):
        """Update microphone sensitivity"""
        try:
            self.recognizer.energy_threshold = value
            print(f"Sensitivity updated to: {value}")
            self.error_occurred.emit(f"Microphone sensitivity updated to {value}")
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