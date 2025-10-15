import subprocess
import os
from PyQt6.QtCore import QObject, pyqtSignal
import platform
import webbrowser
import json
import re

class CommandHandler(QObject):
    command_executed = pyqtSignal(str)  # Emitted when a command is executed
    command_failed = pyqtSignal(str)    # Emitted when a command fails
    suggestion_updated = pyqtSignal(list)  # Emitted when command suggestions change

    def __init__(self):
        super().__init__()
        self.setup_commands()
        self.last_command = None
        self.command_history = []

    def setup_commands(self):
        """Set up available commands and their handlers"""
        self.commands = {
            # App control
            "open": self._handle_open_command,
            "close": self._handle_close_command,
            "switch to": self._handle_switch_command,
            
            # System controls
            "volume": self._handle_volume_command,
            "brightness": self._handle_brightness_command,
            "mute": lambda _: self._handle_volume_command("mute"),
            "unmute": lambda _: self._handle_volume_command("unmute"),
            
            # Web commands
            "search": self._handle_search_command,
            "go to": self._handle_goto_command,
            
            # Assistant control
            "switch mode": self._handle_mode_switch,
            "help": self._handle_help_command,
            
            # System commands
            "sleep": lambda _: self._handle_system_command("sleep"),
            "shutdown": lambda _: self._handle_system_command("shutdown"),
            "restart": lambda _: self._handle_system_command("restart"),
        }

        # Common applications for quick access
        self.common_apps = {
            "browser": "Safari",
            "mail": "Mail",
            "music": "Music",
            "settings": "System Preferences",
            "terminal": "Terminal",
            "notes": "Notes",
            "calendar": "Calendar",
        }

    def process_command(self, command_text):
        """Process a voice command"""
        try:
            # Convert to lowercase and strip whitespace
            command_text = command_text.lower().strip()
            
            # Find matching command
            for cmd_key in self.commands.keys():
                if command_text.startswith(cmd_key):
                    # Extract parameters (everything after the command)
                    params = command_text[len(cmd_key):].strip()
                    # Execute the command
                    self.commands[cmd_key](params)
                    self.command_executed.emit(f"Executed: {command_text}")
                    self.command_history.append(command_text)
                    return True
            
            self.command_failed.emit(f"Unknown command: {command_text}")
            return False
            
        except Exception as e:
            self.command_failed.emit(f"Error executing command: {str(e)}")
            return False

    def get_suggestions(self, partial_command):
        """Get command suggestions based on partial input"""
        suggestions = []
        partial_command = partial_command.lower()
        
        # Add matching commands
        for cmd in self.commands.keys():
            if cmd.startswith(partial_command):
                suggestions.append(cmd)
        
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
                subprocess.run(["open", "-a", app_name])
            else:
                subprocess.run([app_name.lower()])
        except Exception as e:
            self.command_failed.emit(f"Failed to open {app_name}: {str(e)}")

    def _handle_close_command(self, params):
        """Handle 'close' command"""
        app_name = params.strip()
        
        if platform.system() == "Darwin":  # macOS
            try:
                apple_script = f'''
                tell application "{app_name}"
                    quit
                end tell
                '''
                subprocess.run(["osascript", "-e", apple_script])
            except Exception as e:
                self.command_failed.emit(f"Failed to close {app_name}: {str(e)}")

    def _handle_switch_command(self, params):
        """Handle 'switch to' command"""
        app_name = params.strip()
        
        if platform.system() == "Darwin":  # macOS
            try:
                apple_script = f'''
                tell application "{app_name}"
                    activate
                end tell
                '''
                subprocess.run(["osascript", "-e", apple_script])
            except Exception as e:
                self.command_failed.emit(f"Failed to switch to {app_name}: {str(e)}")

    def _handle_volume_command(self, params):
        """Handle volume control commands"""
        if platform.system() == "Darwin":  # macOS
            try:
                if params == "mute":
                    subprocess.run(["osascript", "-e", "set volume output muted true"])
                elif params == "unmute":
                    subprocess.run(["osascript", "-e", "set volume output muted false"])
                else:
                    # Expect volume level 0-100
                    try:
                        volume = int(params)
                        volume = max(0, min(100, volume))
                        # Convert to macOS volume (0-7)
                        mac_volume = int((volume / 100) * 7)
                        subprocess.run(["osascript", "-e", f"set volume output volume {mac_volume}"])
                    except ValueError:
                        self.command_failed.emit("Invalid volume level")
            except Exception as e:
                self.command_failed.emit(f"Failed to control volume: {str(e)}")

    def _handle_brightness_command(self, params):
        """Handle brightness control command"""
        if platform.system() == "Darwin":  # macOS
            try:
                brightness = int(params)
                brightness = max(0, min(100, brightness))
                # This requires additional permissions/setup on macOS
                self.command_failed.emit("Brightness control not implemented yet")
            except ValueError:
                self.command_failed.emit("Invalid brightness level")

    def _handle_search_command(self, params):
        """Handle web search command"""
        search_query = params.strip()
        search_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(search_url)

    def _handle_goto_command(self, params):
        """Handle 'go to' website command"""
        url = params.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        webbrowser.open(url)

    def _handle_mode_switch(self, params):
        """Handle mode switch command"""
        mode = params.strip()
        self.command_executed.emit(f"Switching to {mode} mode")
        return mode

    def _handle_help_command(self, params):
        """Handle help command"""
        if not params:
            # Show general help
            help_text = "Available commands:\n" + "\n".join(self.commands.keys())
            self.command_executed.emit(help_text)
        else:
            # Show specific command help
            command = params.strip()
            if command in self.commands:
                help_text = f"Help for '{command}' command..."  # Add specific help text
                self.command_executed.emit(help_text)
            else:
                self.command_failed.emit(f"No help available for '{command}'")

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
                    subprocess.run(commands[command])
                except Exception as e:
                    self.command_failed.emit(f"Failed to execute {command}: {str(e)}")
            else:
                self.command_failed.emit(f"Unknown system command: {command}")
