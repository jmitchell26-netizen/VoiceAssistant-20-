class ContextualHelp:
    def __init__(self):
        self.setup_help_content()

    def setup_help_content(self):
        """Set up help content for different contexts"""
        self.typing_help = {
            "punctuation": [
                "Say 'period' to add a period",
                "Say 'comma' to add a comma",
                "Say 'question mark' to add a question mark",
                "Say 'exclamation mark' to add an exclamation mark"
            ],
            "formatting": [
                "Say 'new line' to start a new line",
                "Say 'new paragraph' to start a new paragraph",
                "Say 'capitalize that' to capitalize the last phrase",
                "Say 'all caps' to convert to uppercase",
                "Say 'lowercase' to convert to lowercase"
            ],
            "editing": [
                "Say 'undo that' to undo the last change",
                "Say 'delete that' to delete the last phrase"
            ]
        }

        self.command_help = {
            "system": [
                "Say 'open [app name]' to open an application",
                "Say 'close [app name]' to close an application",
                "Say 'switch to [app name]' to switch to an open application"
            ],
            "window": [
                "Say 'minimize window' to minimize the current window",
                "Say 'maximize window' to maximize the current window"
            ]
        }

    def get_contextual_help(self, context):
        """Get help information based on context"""
        help_info = []
        
        # Convert context to lowercase for matching
        context = context.lower()
        
        # Add relevant help based on context keywords
        if any(word in context for word in ["type", "write", "dictate"]):
            help_info.extend(self.typing_help["punctuation"])
            help_info.extend(self.typing_help["formatting"])
        
        if any(word in context for word in ["edit", "change", "fix"]):
            help_info.extend(self.typing_help["editing"])
        
        if any(word in context for word in ["open", "close", "switch", "app"]):
            help_info.extend(self.command_help["system"])
        
        if any(word in context for word in ["window", "minimize", "maximize"]):
            help_info.extend(self.command_help["window"])
        
        return help_info

    def get_quick_tip(self, context):
        """Get a quick tip based on context"""
        context = context.lower()
        
        # Tips for common scenarios
        if "help" in context:
            return "Try saying 'what commands are available' for a full list"
        
        if "not working" in context or "doesn't work" in context:
            return "Try speaking more clearly and a bit louder"
        
        if "type" in context or "write" in context:
            return "You can use punctuation commands like 'period' and 'comma'"
        
        if "open" in context or "close" in context:
            return "Specify the app name, like 'open Safari' or 'close Mail'"
        
        return None  # No specific tip for this context