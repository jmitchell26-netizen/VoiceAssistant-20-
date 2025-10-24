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
        self.last_text = text

        if text.lower() == "undo that":
            return self._handle_undo()

        for command, punctuation in self.punctuation_commands.items():
            text = text.replace(f" {command}", punctuation)
        
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
        """Handle the undo command"""
        return ""
