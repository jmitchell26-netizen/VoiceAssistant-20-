import subprocess
import os
from PyQt6.QtCore import QObject, pyqtSignal
import platform
import webbrowser
import json
import re
from difflib import get_close_matches

class CommandHandler(QObject):
    command_executed = pyqtSignal(str)  # Emitted when a command is executed
    command_failed = pyqtSignal(str)    # Emitted when a command fails
    suggestion_updated = pyqtSignal(list)  # Emitted when command suggestions change

    def __init__(self):
        super().__init__()
        self.setup_commands()
        self.last_command = None
        self.command_history = []
        self.setup_aliases()

    def setup_commands(self):
        """Set up available commands and their handlers"""
        self.commands = {
            # App control
            "open": self._handle_open_command,
            "launch": self._handle_open_command,  # Alias for open
            "close": self._handle_close_command,
            "quit": self._handle_close_command,   # Alias for close
            "switch to": self._handle_switch_command,
            "focus": self._handle_switch_command, # Alias for switch to
            
            # System controls
            "volume": self._handle_volume_command,
            "set volume": self._handle_volume_command,
            "brightness": self._handle_brightness_command,
            "mute": lambda _: self._handle_volume_command("mute"),
            "unmute": lambda _: self._handle_volume_command("unmute"),
            
            # Web commands
            "search": self._handle_search_command,
            "search for": self._handle_search_command,
            "look up": self._handle_search_command,
            "go to": self._handle_goto_command,
            "open website": self._handle_goto_command,
            
            # Assistant control
            "switch mode": self._handle_mode_switch,
            "change mode": self._handle_mode_switch,
            "help": self._handle_help_command,
            "show help": self._handle_help_command,
            
            # System commands
            "sleep": lambda _: self._handle_system_command("sleep"),
            "shutdown": lambda _: self._handle_system_command("shutdown"),
            "restart": lambda _: self._handle_system_command("restart"),
        }

        # Common applications for quick access
        self.common_apps = {
            "browser": "Safari",
            "web browser": "Safari",
            "mail": "Mail",
            "email": "Mail",
            "music": "Music",
            "settings": "System Preferences",
            "preferences": "System Preferences",
            "terminal": "Terminal",
            "command line": "Terminal",
            "notes": "Notes",
            "calendar": "Calendar",
            "messages": "Messages",
            "text messages": "Messages",
            "finder": "Finder",
            "files": "Finder",
        }

    def setup_aliases(self):
        """Set up command aliases and variations"""
        self.command_aliases = {
            "open": ["launch", "start", "run"],
            "close": ["quit", "exit", "stop"],
            "switch to": ["focus", "go to", "show"],
            "volume": ["set volume", "change volume"],
            "search": ["search for", "look up", "find"],
            "help": ["show help", "get help", "need help"],
        }

    def find_matching_command(self, command_text):
        """Find the best matching command using fuzzy matching"""
        # Direct match
        for cmd in self.commands.keys():
            if command_text.startswith(cmd):
                return cmd

        # Check aliases
        for cmd, aliases in self.command_aliases.items():
            for alias in aliases:
                if command_text.startswith(alias):
                    return cmd

        # Fuzzy match if no direct match found
        all_commands = list(self.commands.keys()) + [
            alias for aliases in self.command_aliases.values() for alias in aliases
        ]
        matches = get_close_matches(command_text.split()[0], all_commands, n=1, cutoff=0.6)
        if matches:
            # Map alias back to main command if necessary
            for cmd, aliases in self.command_aliases.items():
                if matches[0] in aliases:
                    return cmd
            return matches[0]

        return None

    def process_command(self, command_text):
        """Process a voice command"""
        try:
            # Convert to lowercase and strip whitespace
            command_text = command_text.lower().strip()
            
            # Find matching command
            matching_command = self.find_matching_command(command_text)
            if matching_command:
                # Extract parameters (everything after the command)
                params = command_text[len(matching_command):].strip()
                # Execute the command
                self.commands[matching_command](params)
                self.command_executed.emit(f"Executed: {command_text}")
                self.command_history.append(command_text)
                return True
            
            # Try to interpret as an app name directly
            if command_text in self.common_apps or command_text in self.common_apps.values():
                self._handle_open_command(command_text)
                return True
            
            self.command_failed.emit(f"Unknown command: {command_text}")
            self._suggest_similar_commands(command_text)
            return False
            
        except Exception as e:
            self.command_failed.emit(f"Error executing command: {str(e)}")
            return False

    def _suggest_similar_commands(self, command_text):
        """Suggest similar commands when an unknown command is received"""
        all_commands = list(self.commands.keys()) + [
            alias for aliases in self.command_aliases.values() for alias in aliases
        ]
        matches = get_close_matches(command_text.split()[0], all_commands, n=3, cutoff=0.5)
        if matches:
            suggestions = "Did you mean: " + ", ".join(matches) + "?"
            self.command_failed.emit(suggestions)

    def get_suggestions(self, partial_command):
        """Get command suggestions based on partial input"""
        suggestions = []
        partial_command = partial_command.lower()
        
        # Add matching commands and their aliases
        for cmd, aliases in self.command_aliases.items():
            if cmd.startswith(partial_command):
                suggestions.append(cmd)
            for alias in aliases:
                if alias.startswith(partial_command):
                    suggestions.append(alias)
        
        # Add matching app names
        for app_alias, app_name in self.common_apps.items():
            if app_alias.startswith(partial_command) or app_name.lower().startswith(partial_command):
                suggestions.append(f"open {app_name}")
        
        # Add common phrases from history
        for hist_cmd in self.command_history:
            if hist_cmd.startswith(partial_command):
                suggestions.append(hist_cmd)
        
        self.suggestion_updated.emit(suggestions)
        return suggestions

    def _handle_open_command(self, params):
        """Handle 'open' command"""
        app_name = params.strip()
        
        # Check common apps dictionary first
        if app_name in self.common_apps:
            app_name = self.common_apps[app_name]
        
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.run(["open", "-a", app_name], capture_output=True, text=True)
                if result.returncode != 0:
                    # Try fuzzy matching app name
                    possible_apps = get_close_matches(app_name, self.common_apps.values(), n=1, cutoff=0.6)
                    if possible_apps:
                        correct_app = possible_apps[0]
                        self.command_executed.emit(f"Opening {correct_app} instead of {app_name}")
                        subprocess.run(["open", "-a", correct_app])
                    else:
                        self.command_failed.emit(f"Could not find application: {app_name}")
            else:
                subprocess.run([app_name.lower()])
        except Exception as e:
            self.command_failed.emit(f"Failed to open {app_name}: {str(e)}")

    def _handle_close_command(self, params):
        """Handle 'close' command"""
        app_name = params.strip()
        
        # Check common apps dictionary
        if app_name in self.common_apps:
            app_name = self.common_apps[app_name]
        
        if platform.system() == "Darwin":  # macOS
            try:
                apple_script = f'''
                tell application "{app_name}"
                    if it is running then
                        quit
                    end if
                end tell
                '''
                result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
                if result.returncode != 0:
                    self.command_failed.emit(f"Failed to close {app_name}: {result.stderr}")
            except Exception as e:
                self.command_failed.emit(f"Failed to close {app_name}: {str(e)}")

    def _handle_switch_command(self, params):
        """Handle 'switch to' command"""
        app_name = params.strip()
        
        # Check common apps dictionary
        if app_name in self.common_apps:
            app_name = self.common_apps[app_name]
        
        if platform.system() == "Darwin":  # macOS
            try:
                apple_script = f'''
                tell application "{app_name}"
                    activate
                end tell
                '''
                result = subprocess.run(["osascript", "-e", apple_script], capture_output=True, text=True)
                if result.returncode != 0:
                    self.command_failed.emit(f"Failed to switch to {app_name}: {result.stderr}")
            except Exception as e:
                self.command_failed.emit(f"Failed to switch to {app_name}: {str(e)}")

    def _handle_volume_command(self, params):
        """Handle volume control commands"""
        if platform.system() == "Darwin":  # macOS
            try:
                if params == "mute":
                    subprocess.run(["osascript", "-e", "set volume output muted true"])
                    self.command_executed.emit("Audio muted")
                elif params == "unmute":
                    subprocess.run(["osascript", "-e", "set volume output muted false"])
                    self.command_executed.emit("Audio unmuted")
                else:
                    # Handle various volume formats
                    try:
                        # Remove "percent", "%" if present
                        params = params.replace("percent", "").replace("%", "").strip()
                        volume = int(params)
                        volume = max(0, min(100, volume))
                        # Convert to macOS volume (0-7)
                        mac_volume = int((volume / 100) * 7)
                        subprocess.run(["osascript", "-e", f"set volume output volume {mac_volume}"])
                        self.command_executed.emit(f"Volume set to {volume}%")
                    except ValueError:
                        self.command_failed.emit("Please specify a volume level between 0 and 100")
            except Exception as e:
                self.command_failed.emit(f"Failed to control volume: {str(e)}")

    def _handle_brightness_command(self, params):
        """Handle brightness control command"""
        if platform.system() == "Darwin":  # macOS
            try:
                # Remove "percent", "%" if present
                params = params.replace("percent", "").replace("%", "").strip()
                brightness = int(params)
                brightness = max(0, min(100, brightness))
                
                # Use brightness control script if available
                brightness_script = os.path.join(os.path.dirname(__file__), "brightness.sh")
                if os.path.exists(brightness_script):
                    subprocess.run(["bash", brightness_script, str(brightness)])
                    self.command_executed.emit(f"Brightness set to {brightness}%")
                else:
                    self.command_failed.emit("Brightness control requires additional setup")
            except ValueError:
                self.command_failed.emit("Please specify a brightness level between 0 and 100")
            except Exception as e:
                self.command_failed.emit(f"Failed to control brightness: {str(e)}")

    def _handle_search_command(self, params):
        """Handle web search command"""
        search_query = params.strip()
        if search_query:
            search_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(search_url)
            self.command_executed.emit(f"Searching for: {search_query}")
        else:
            self.command_failed.emit("Please specify what to search for")

    def _handle_goto_command(self, params):
        """Handle 'go to' website command"""
        url = params.strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            self.command_executed.emit(f"Opening website: {url}")
        else:
            self.command_failed.emit("Please specify a website to visit")

    def _handle_mode_switch(self, params):
        """Handle mode switch command"""
        mode = params.strip()
        if mode:
            self.command_executed.emit(f"Switching to {mode} mode")
            return mode
        else:
            self.command_failed.emit("Please specify which mode to switch to")
            return None

    def _handle_help_command(self, params):
        """Handle help command"""
        if not params:
            # Show general help
            help_text = "Available commands:\n"
            categories = {
                "App Control": ["open", "close", "switch to"],
                "System Controls": ["volume", "mute", "unmute", "brightness"],
                "Web Commands": ["search", "go to"],
                "System Commands": ["sleep", "shutdown", "restart"],
                "Assistant Control": ["switch mode", "help"]
            }
            
            for category, cmds in categories.items():
                help_text += f"\n{category}:\n"
                for cmd in cmds:
                    aliases = self.command_aliases.get(cmd, [])
                    if aliases:
                        help_text += f"  • {cmd} (also: {', '.join(aliases)})\n"
                    else:
                        help_text += f"  • {cmd}\n"
            
            self.command_executed.emit(help_text)
        else:
            # Show specific command help
            command = params.strip()
            matching_command = self.find_matching_command(command)
            if matching_command:
                aliases = self.command_aliases.get(matching_command, [])
                help_text = f"Help for '{matching_command}' command:\n"
                if aliases:
                    help_text += f"Aliases: {', '.join(aliases)}\n"
                # Add specific command instructions here
                self.command_executed.emit(help_text)
            else:
                self.command_failed.emit(f"No help available for '{command}'")
                self._suggest_similar_commands(command)

    def _handle_system_command(self, command):
        """Handle system commands (sleep, shutdown, restart)"""
        if platform.system() == "Darwin":  # macOS
            commands = {
                "sleep": ["pmset", "sleepnow"],
                "shutdown": ["shutdown", "-h", "now"],
                "restart": ["shutdown", "-r", "now"]
            }
            
            if command in commands:
                try:
                    # Confirm dangerous commands
                    if command in ["shutdown", "restart"]:
                        self.command_executed.emit(f"Warning: System will {command}. Say 'cancel' to abort.")
                        # TODO: Add confirmation handling
                        return
                    
                    subprocess.run(commands[command])
                    self.command_executed.emit(f"Executing system {command}")
                except Exception as e:
                    self.command_failed.emit(f"Failed to execute {command}: {str(e)}")
            else:
                self.command_failed.emit(f"Unknown system command: {command}")
                self._suggest_similar_commands(command)