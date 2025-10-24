from PyQt6.QtCore import QObject, pyqtSignal
import subprocess
import platform

class CommandHandler(QObject):
    command_executed = pyqtSignal(str)
    command_failed = pyqtSignal(str)
    suggestion_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setup_commands()

    def setup_commands(self):
        """Set up available commands and their handlers"""
        self.commands = {
            'open': self._handle_open,
            'close': self._handle_close,
            'switch to': self._handle_switch,
            'minimize': self._handle_minimize,
            'maximize': self._handle_maximize,
            'help': self._handle_help
        }

    def process_command(self, command_text):
        """Process a voice command"""
        try:
            command_text = command_text.lower().strip()
            
            # Find matching command
            for cmd, handler in self.commands.items():
                if command_text.startswith(cmd):
                    args = command_text[len(cmd):].strip()
                    handler(args)
                    return
            
            self.command_failed.emit(f"Unknown command: {command_text}")
            
        except Exception as e:
            self.command_failed.emit(f"Error executing command: {str(e)}")

    def get_suggestions(self, partial_command):
        """Get command suggestions based on partial input"""
        suggestions = []
        partial_command = partial_command.lower()
        
        # Add basic commands
        basic_commands = [
            "open [app name]",
            "close [app name]",
            "switch to [app name]",
            "minimize window",
            "maximize window",
            "show help"
        ]
        
        # Filter suggestions based on partial command
        for cmd in basic_commands:
            if partial_command in cmd.lower():
                suggestions.append(cmd)
        
        self.suggestion_updated.emit(suggestions)

    def _handle_open(self, app_name):
        """Handle the 'open' command"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', '-a', app_name])
                self.command_executed.emit(f"Opened {app_name}")
            else:
                self.command_failed.emit("Open command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to open {app_name}: {str(e)}")

    def _handle_close(self, app_name):
        """Handle the 'close' command"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['osascript', '-e', f'tell application "{app_name}" to quit'])
                self.command_executed.emit(f"Closed {app_name}")
            else:
                self.command_failed.emit("Close command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to close {app_name}: {str(e)}")

    def _handle_switch(self, app_name):
        """Handle the 'switch to' command"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['osascript', '-e', f'tell application "{app_name}" to activate'])
                self.command_executed.emit(f"Switched to {app_name}")
            else:
                self.command_failed.emit("Switch command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to switch to {app_name}: {str(e)}")

    def _handle_minimize(self, args):
        """Handle the 'minimize' command"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['osascript', '-e', 'tell application "System Events" to keystroke "m" using command down'])
                self.command_executed.emit("Minimized window")
            else:
                self.command_failed.emit("Minimize command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to minimize window: {str(e)}")

    def _handle_maximize(self, args):
        """Handle the 'maximize' command"""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['osascript', '-e', 'tell application "System Events" to keystroke "f" using {command down, control down}'])
                self.command_executed.emit("Maximized window")
            else:
                self.command_failed.emit("Maximize command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to maximize window: {str(e)}")

    def _handle_help(self, args):
        """Handle the 'help' command"""
        help_text = """Available Commands:
        - open [app name]: Opens an application
        - close [app name]: Closes an application
        - switch to [app name]: Switches to an open application
        - minimize window: Minimizes the current window
        - maximize window: Maximizes the current window
        - help: Shows this help message"""
        
        self.command_executed.emit(help_text)