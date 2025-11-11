from PyQt6.QtCore import QObject, pyqtSignal
import subprocess
import platform

from .browser_commands import BrowserCommandRouter
from .app_launcher import AppLauncher

class CommandHandler(QObject):
    command_executed = pyqtSignal(str)
    command_failed = pyqtSignal(str)
    suggestion_updated = pyqtSignal(list)
    context_changed = pyqtSignal(str)  # Emits 'general', 'browser', etc.

    def __init__(self):
        super().__init__()
        self.browser_router = BrowserCommandRouter()
        self.app_launcher = AppLauncher()
        self.current_context = 'general'
        self.is_browser_active = False
        
        # Connect browser command signals
        self.browser_router.command_executed.connect(self.command_executed.emit)
        self.browser_router.command_failed.connect(self.command_failed.emit)
        
        # Connect app launcher signals
        self.app_launcher.app_opened.connect(lambda name: self.command_executed.emit(f"Opened {name}"))
        self.app_launcher.app_not_found.connect(self._handle_app_not_found)
        
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
        
        # Browser-specific commands
        self.browser_commands = {
            'close tab': lambda: self.browser_router.execute_command('close_tab'),
            'new tab': lambda: self.browser_router.execute_command('new_tab'),
            'close all tabs': lambda: self.browser_router.execute_command('close_all_tabs'),
            'go back': lambda: self.browser_router.execute_command('go_back'),
            'go forward': lambda: self.browser_router.execute_command('go_forward'),
            'refresh': lambda: self.browser_router.execute_command('refresh'),
            'reload': lambda: self.browser_router.execute_command('refresh'),
            'bookmark': lambda: self.browser_router.execute_command('bookmark_page'),
            'bookmark this': lambda: self.browser_router.execute_command('bookmark_page'),
            'zoom in': lambda: self.browser_router.execute_command('zoom_in'),
            'zoom out': lambda: self.browser_router.execute_command('zoom_out'),
            'scroll up': lambda: self.browser_router.execute_command('scroll_up'),
            'scroll down': lambda: self.browser_router.execute_command('scroll_down'),
            'scroll to top': lambda: self.browser_router.execute_command('scroll_to_top'),
            'scroll to bottom': lambda: self.browser_router.execute_command('scroll_to_bottom'),
            'find on page': lambda: self.browser_router.execute_command('find_on_page'),
        }
    
    def set_browser_active(self, browser_name):
        """Called when a browser becomes the active app"""
        self.is_browser_active = True
        self.current_context = 'browser'
        self.browser_router.set_active_browser(browser_name)
        self.context_changed.emit('browser')
        print(f"Context changed to: browser ({browser_name})")
    
    def set_browser_inactive(self):
        """Called when switching away from a browser"""
        self.is_browser_active = False
        self.current_context = 'general'
        self.context_changed.emit('general')
        print("Context changed to: general")

    def process_command(self, command_text):
        """Process a voice command with context awareness"""
        try:
            command_text = command_text.lower().strip()
            
            # Try browser commands first if in browser context
            if self.is_browser_active:
                # Check for "go to" or "search for" commands (special handling)
                if command_text.startswith('go to '):
                    url = command_text[6:].strip()
                    self.browser_router.execute_command('go_to_url', url)
                    return
                elif command_text.startswith('search for '):
                    query = command_text[11:].strip()
                    self.browser_router.execute_command('search', query)
                    return
                elif command_text.startswith('find '):
                    text = command_text[5:].strip()
                    # Remove "on page" suffix if present
                    if text.endswith(' on page'):
                        text = text[:-8].strip()
                    self.browser_router.execute_command('find_on_page', text)
                    return
                
                # Check standard browser commands
                for cmd, handler in self.browser_commands.items():
                    if command_text.startswith(cmd):
                        handler()
                        return
            
            # Fall back to general commands
            for cmd, handler in self.commands.items():
                if command_text.startswith(cmd):
                    args = command_text[len(cmd):].strip()
                    handler(args)
                    return
            
            # No matching command found
            if self.is_browser_active:
                self.command_failed.emit(f"Unknown command: {command_text} (Try browser commands like 'close tab', 'go back', etc.)")
            else:
                self.command_failed.emit(f"Unknown command: {command_text}")
            
        except Exception as e:
            self.command_failed.emit(f"Error executing command: {str(e)}")

    def get_suggestions(self, partial_command):
        """Get command suggestions based on partial input and context"""
        suggestions = []
        partial_command = partial_command.lower()
        
        # Browser-specific commands if in browser context
        if self.is_browser_active:
            browser_commands = [
                "close tab",
                "new tab",
                "close all tabs",
                "go back",
                "go forward",
                "refresh",
                "bookmark this",
                "zoom in",
                "zoom out",
                "scroll up",
                "scroll down",
                "scroll to top",
                "scroll to bottom",
                "go to [url]",
                "search for [query]",
                "find [text] on page"
            ]
            
            # Filter browser suggestions
            for cmd in browser_commands:
                if partial_command in cmd.lower() or not partial_command:
                    suggestions.append(cmd)
        
        # Always include basic commands
        basic_commands = [
            "open [app name]",
            "close [app name]",
            "switch to [app name]",
            "minimize window",
            "maximize window",
            "show help"
        ]
        
        # Filter basic suggestions based on partial command
        for cmd in basic_commands:
            if partial_command in cmd.lower():
                suggestions.append(cmd)
        
        self.suggestion_updated.emit(suggestions)

    def _handle_open(self, app_name):
        """Handle the 'open' command with smart app matching"""
        if not app_name:
            self.command_failed.emit("Please specify an application to open")
            return
        
        # Use the smart app launcher (handles aliases and fuzzy matching)
        success, message = self.app_launcher.open_app(app_name)
        
        # Signals are already emitted by app_launcher connections
        # No need to emit here as well
    
    def _handle_app_not_found(self, app_name, suggestions):
        """Handle when an app is not found"""
        if suggestions:
            suggestion_text = ", ".join(suggestions)
            self.command_failed.emit(
                f"Could not find '{app_name}'. Did you mean: {suggestion_text}?"
            )
        else:
            self.command_failed.emit(
                f"Could not find application '{app_name}'. "
                f"Try saying the full application name, like 'Visual Studio Code' or 'Google Chrome'."
            )

    def _handle_close(self, app_name):
        """Handle the 'close' command with smart app name resolution"""
        if not app_name:
            self.command_failed.emit("Please specify an application to close")
            return
        
        # Resolve app name using aliases
        actual_name = self.app_launcher._resolve_alias(app_name.lower())
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['osascript', '-e', f'tell application "{actual_name}" to quit'])
                self.command_executed.emit(f"Closed {actual_name}")
            else:
                self.command_failed.emit("Close command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to close {actual_name}: {str(e)}")

    def _handle_switch(self, app_name):
        """Handle the 'switch to' command with smart app name resolution"""
        if not app_name:
            self.command_failed.emit("Please specify an application to switch to")
            return
        
        # Resolve app name using aliases
        actual_name = self.app_launcher._resolve_alias(app_name.lower())
        
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['osascript', '-e', f'tell application "{actual_name}" to activate'])
                self.command_executed.emit(f"Switched to {actual_name}")
            else:
                self.command_failed.emit("Switch command not implemented for this platform")
        except Exception as e:
            self.command_failed.emit(f"Failed to switch to {actual_name}: {str(e)}")

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