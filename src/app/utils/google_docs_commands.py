"""
Google Docs Command Handlers
Provides voice command handlers specifically for Google Docs formatting via browser automation.
"""

from PyQt6.QtCore import QObject, pyqtSignal
import subprocess


class GoogleDocsCommands(QObject):
    """Command handler for Google Docs formatting and control"""
    
    command_executed = pyqtSignal(str)
    command_failed = pyqtSignal(str)
    
    def __init__(self, browser_name="Google Chrome"):
        super().__init__()
        self.browser_name = browser_name
        self.process_name = "Google Chrome" if "chrome" in browser_name.lower() else browser_name
    
    def set_browser(self, browser_name):
        """Update which browser Google Docs is running in"""
        if not browser_name:
            return
        self.browser_name = browser_name
        self.process_name = "Google Chrome" if "chrome" in browser_name.lower() else browser_name
    
    def execute_applescript(self, script):
        """Execute an AppleScript command and return result"""
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                error_msg = result.stderr.strip()
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def _click_menu_item(self, *menu_path):
        """Click a menu item by navigating the menu hierarchy"""
        script_parts = [f'tell application "System Events"',
                       f'    tell process "{self.process_name}"',
                       f'        tell menu bar 1']
        
        # Build the menu navigation
        for i, item in enumerate(menu_path):
            if i == 0:
                script_parts.append(f'            tell menu bar item "{item}"')
            else:
                script_parts.append(f'                tell menu "{menu_path[i-1]}"')
                if i == len(menu_path) - 1:
                    # Last item - click it
                    script_parts.append(f'                    click menu item "{item}"')
                else:
                    # Intermediate menu
                    script_parts.append(f'                    tell menu item "{item}"')
        
        # Close the tell blocks
        for i in range(len(menu_path)):
            script_parts.append('                end tell')
        script_parts.append('            end tell')
        script_parts.append('        end tell')
        script_parts.append('    end tell')
        script_parts.append('end tell')
        
        script = '\n'.join(script_parts)
        return self.execute_applescript(script)
    
    # Text Style Commands
    def make_bold(self):
        """Toggle bold formatting"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "b" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Toggled bold")
        else:
            self.command_failed.emit(f"Failed to toggle bold: {msg}")
    
    def make_italic(self):
        """Toggle italic formatting"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "i" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Toggled italic")
        else:
            self.command_failed.emit(f"Failed to toggle italic: {msg}")
    
    def make_underline(self):
        """Toggle underline formatting"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "u" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Toggled underline")
        else:
            self.command_failed.emit(f"Failed to toggle underline: {msg}")
    
    # Font Size Commands
    def increase_font_size(self):
        """Increase font size"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke ">" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Increased font size")
        else:
            self.command_failed.emit(f"Failed to increase font size: {msg}")
    
    def decrease_font_size(self):
        """Decrease font size"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "<" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Decreased font size")
        else:
            self.command_failed.emit(f"Failed to decrease font size: {msg}")
    
    # Line Spacing Commands
    def single_space(self):
        """Set line spacing to single"""
        success, msg = self._click_menu_item("Format", "Line spacing", "Single")
        if success:
            self.command_executed.emit("Set to single spacing")
        else:
            self.command_failed.emit(f"Failed to set single spacing: {msg}")
    
    def double_space(self):
        """Set line spacing to double"""
        success, msg = self._click_menu_item("Format", "Line spacing", "Double")
        if success:
            self.command_executed.emit("Set to double spacing")
        else:
            self.command_failed.emit(f"Failed to set double spacing: {msg}")
    
    def line_spacing_one_five(self):
        """Set line spacing to 1.5"""
        success, msg = self._click_menu_item("Format", "Line spacing", "1.5")
        if success:
            self.command_executed.emit("Set to 1.5 line spacing")
        else:
            self.command_failed.emit(f"Failed to set 1.5 spacing: {msg}")
    
    # List Commands
    def add_bullets(self):
        """Add bullet list formatting"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "8" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Added bullets")
        else:
            self.command_failed.emit(f"Failed to add bullets: {msg}")
    
    def add_numbering(self):
        """Add numbered list formatting"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "7" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Added numbering")
        else:
            self.command_failed.emit(f"Failed to add numbering: {msg}")
    
    def remove_bullets(self):
        """Remove list formatting (same shortcut as add bullets - it toggles)"""
        self.add_bullets()  # Toggle off
    
    # Alignment Commands
    def align_left(self):
        """Align text to the left"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "l" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Aligned left")
        else:
            self.command_failed.emit(f"Failed to align left: {msg}")
    
    def align_center(self):
        """Align text to the center"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "e" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Aligned center")
        else:
            self.command_failed.emit(f"Failed to align center: {msg}")
    
    def align_right(self):
        """Align text to the right"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "r" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Aligned right")
        else:
            self.command_failed.emit(f"Failed to align right: {msg}")
    
    def align_justify(self):
        """Justify text"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "j" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Justified text")
        else:
            self.command_failed.emit(f"Failed to justify: {msg}")
    
    # Heading Commands
    def heading_one(self):
        """Apply Heading 1 style"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "1" using {{command down, option down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Applied Heading 1")
        else:
            self.command_failed.emit(f"Failed to apply Heading 1: {msg}")
    
    def heading_two(self):
        """Apply Heading 2 style"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "2" using {{command down, option down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Applied Heading 2")
        else:
            self.command_failed.emit(f"Failed to apply Heading 2: {msg}")
    
    def heading_three(self):
        """Apply Heading 3 style"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "3" using {{command down, option down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Applied Heading 3")
        else:
            self.command_failed.emit(f"Failed to apply Heading 3: {msg}")
    
    def normal_text(self):
        """Apply normal text style"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "0" using {{command down, option down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Applied normal text")
        else:
            self.command_failed.emit(f"Failed to apply normal text: {msg}")
    
    # Color Commands (using Format menu)
    def change_text_color(self, color_name):
        """Change text color (basic implementation - opens color picker)"""
        success, msg = self._click_menu_item("Format", "Text", "Text color")
        if success:
            self.command_executed.emit(f"Opening text color picker")
        else:
            self.command_failed.emit(f"Failed to open color picker: {msg}")
    
    def highlight_text(self):
        """Highlight text (opens highlight picker)"""
        success, msg = self._click_menu_item("Format", "Text", "Highlight color")
        if success:
            self.command_executed.emit("Opening highlight color picker")
        else:
            self.command_failed.emit(f"Failed to open highlight picker: {msg}")
    
    # Additional Formatting
    def strikethrough(self):
        """Toggle strikethrough"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "5" using {{command down, shift down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Toggled strikethrough")
        else:
            self.command_failed.emit(f"Failed to toggle strikethrough: {msg}")
    
    def clear_formatting(self):
        """Clear all formatting"""
        script = f'''
        tell application "System Events"
            tell process "{self.process_name}"
                keystroke "\\" using {{command down}}
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Cleared formatting")
        else:
            self.command_failed.emit(f"Failed to clear formatting: {msg}")

