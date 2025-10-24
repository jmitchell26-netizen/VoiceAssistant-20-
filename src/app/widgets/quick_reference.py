from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class QuickReferenceCard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Quick Reference")
        layout.addWidget(title)
        
        # Reference text area
        self.reference_text = QTextEdit()
        self.reference_text.setReadOnly(True)
        self.reference_text.setPlaceholderText("Available commands will appear here...")
        layout.addWidget(self.reference_text)

    def update_commands(self, context=None):
        """Update the quick reference based on context"""
        if context:
            # Add relevant commands based on context
            commands = self._get_context_commands(context)
            self.reference_text.setText(commands)
        else:
            # Show default commands
            self.show_default_commands()

    def _get_context_commands(self, context):
        """Get commands relevant to the current context"""
        # Basic command reference
        commands = "Common Commands:\n\n"
        
        if "typing" in context.lower():
            commands += "Voice Typing Commands:\n"
            commands += "- 'period' - Add a period\n"
            commands += "- 'comma' - Add a comma\n"
            commands += "- 'question mark' - Add a question mark\n"
            commands += "- 'new line' - Start a new line\n"
            commands += "- 'new paragraph' - Start a new paragraph\n"
            commands += "- 'capitalize that' - Capitalize the last phrase\n"
            commands += "- 'all caps' - Convert to uppercase\n"
            commands += "- 'lowercase' - Convert to lowercase\n"
            commands += "- 'undo that' - Undo last change\n"
        else:
            commands += "System Commands:\n"
            commands += "- 'open [app name]' - Open an application\n"
            commands += "- 'close [app name]' - Close an application\n"
            commands += "- 'switch to [app name]' - Switch to an open application\n"
            commands += "- 'minimize window' - Minimize the current window\n"
            commands += "- 'maximize window' - Maximize the current window\n"
        
        return commands

    def show_default_commands(self):
        """Show the default command reference"""
        commands = "Basic Commands:\n\n"
        commands += "1. Voice Typing:\n"
        commands += "- Start/Stop typing\n"
        commands += "- Use punctuation commands\n"
        commands += "- Format text with voice\n\n"
        commands += "2. System Control:\n"
        commands += "- Open/close applications\n"
        commands += "- Switch between windows\n"
        commands += "- Control media playback\n"
        
        self.reference_text.setText(commands)