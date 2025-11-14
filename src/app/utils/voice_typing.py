import re
from deepmultilingualpunctuation import PunctuationModel

class VoiceTypingMode:
    """Handles voice typing specific functionality"""
    def __init__(self, voice_manager, settings_manager=None):
        self.voice_manager = voice_manager
        self.settings_manager = settings_manager
        self.is_active = False
        self.setup_punctuation_commands()
        self.last_text = ""
        
        # Initialize automatic punctuation model (lazy loading)
        self._punctuation_model = None
        self._auto_punctuation_enabled = False
        
        # Load auto-punctuation setting
        if self.settings_manager:
            try:
                self._auto_punctuation_enabled = self.settings_manager.get_setting(
                    'voice_typing', 'auto_punctuation'
                )
            except (KeyError, AttributeError):
                self._auto_punctuation_enabled = False
    
    @property
    def punctuation_model(self):
        """Lazy load the punctuation model when first needed"""
        if self._punctuation_model is None and self._auto_punctuation_enabled:
            print("Loading automatic punctuation model...")
            try:
                self._punctuation_model = PunctuationModel()
                print("Punctuation model loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load punctuation model: {e}")
                self._auto_punctuation_enabled = False
        return self._punctuation_model
    
    def set_auto_punctuation(self, enabled):
        """Enable or disable automatic punctuation"""
        self._auto_punctuation_enabled = enabled
        if self.settings_manager:
            self.settings_manager.set_setting('voice_typing', 'auto_punctuation', enabled)

    def setup_punctuation_commands(self):
        """Set up voice commands for punctuation"""
        self.punctuation_commands = {
            # Basic punctuation
            "period": ".",
            "comma": ",",
            "question mark": "?",
            "exclamation mark": "!",
            "exclamation point": "!",
            "semicolon": ";",
            "colon": ":",
            
            # Quotes and brackets
            "open quote": '"',
            "close quote": '"',
            "quote": '"',
            "apostrophe": "'",
            "open parenthesis": "(",
            "close parenthesis": ")",
            "open bracket": "[",
            "close bracket": "]",
            "open brace": "{",
            "close brace": "}",
            
            # Dashes and special characters
            "hyphen": "-",
            "dash": " – ",
            "em dash": " — ",
            "underscore": "_",
            "ellipsis": "...",
            
            # Line breaks
            "new line": "\n",
            "new paragraph": "\n\n",
            
            # Bullets and lists
            "bullet": "• ",
            "bullet point": "• ",
            "star": "* ",
            "dash bullet": "- ",
            "number one": "1. ",
            "number two": "2. ",
            "number three": "3. ",
            "number four": "4. ",
            "number five": "5. ",
        }
        
        # Common list formatting
        self.list_commands = {
            "add bullets": "bullet",
            "start list": "bullet",
            "numbered list": "number one",
        }

    def process_text(self, text):
        """Process recognized text for voice typing"""
        self.last_text = text

        if text.lower() == "undo that":
            return self._handle_undo()
        
        # Check for list commands first
        text_lower = text.lower()
        for list_cmd, replacement in self.list_commands.items():
            if text_lower == list_cmd:
                return self.punctuation_commands.get(replacement, replacement)
        
        # Handle formatting commands (capitalize, all caps, etc.)
        formatted_text = self._handle_formatting_commands(text)
        if formatted_text != text:
            return formatted_text
        
        # Apply automatic punctuation if enabled
        if self._auto_punctuation_enabled and self.punctuation_model:
            try:
                text = self._apply_auto_punctuation(text)
            except Exception as e:
                print(f"Auto-punctuation error: {e}")
                # Fall through to manual punctuation
        
        # Apply voice-commanded punctuation (replace spoken punctuation)
        for command, punctuation in self.punctuation_commands.items():
            # Match whole words only to avoid partial replacements
            pattern = r'\b' + re.escape(command) + r'\b'
            text = re.sub(pattern, punctuation, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_auto_punctuation(self, text):
        """Apply automatic punctuation using the AI model"""
        if not text or not self.punctuation_model:
            return text
        
        # The model adds punctuation to unpunctuated text
        try:
            result = self.punctuation_model.restore_punctuation(text)
            return result
        except Exception as e:
            print(f"Error applying auto-punctuation: {e}")
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
        """Handle the undo command"""
        return ""
