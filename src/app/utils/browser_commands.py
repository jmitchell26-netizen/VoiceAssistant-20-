"""
Browser Command Handlers
Provides voice command handlers for controlling web browsers (Safari, Chrome, etc.)
"""

from PyQt6.QtCore import QObject, pyqtSignal
import subprocess
import platform
import urllib.parse


class BrowserCommandHandler(QObject):
    """Base class for browser command handling"""
    
    command_executed = pyqtSignal(str)
    command_failed = pyqtSignal(str)
    
    def __init__(self, browser_name):
        super().__init__()
        self.browser_name = browser_name
        
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


class SafariCommands(BrowserCommandHandler):
    """Command handler for Safari browser"""
    
    def __init__(self):
        super().__init__("Safari")
    
    def close_tab(self):
        """Close the current tab"""
        script = '''
        tell application "Safari"
            close current tab of front window
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Closed current tab")
        else:
            self.command_failed.emit(f"Failed to close tab: {msg}")
    
    def close_all_tabs(self):
        """Close all tabs in current window"""
        script = '''
        tell application "Safari"
            close every tab of front window
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Closed all tabs")
        else:
            self.command_failed.emit(f"Failed to close tabs: {msg}")
    
    def new_tab(self, url=None):
        """Open a new tab, optionally with a URL"""
        if url:
            script = f'''
            tell application "Safari"
                tell front window
                    set current tab to (make new tab with properties {{URL:"{url}"}})
                end tell
            end tell
            '''
        else:
            script = '''
            tell application "Safari"
                tell front window
                    make new tab
                end tell
            end tell
            '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Opened new tab")
        else:
            self.command_failed.emit(f"Failed to open tab: {msg}")
    
    def go_back(self):
        """Navigate back in history"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke "[" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Navigated back")
        else:
            self.command_failed.emit(f"Failed to go back: {msg}")
    
    def go_forward(self):
        """Navigate forward in history"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke "]" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Navigated forward")
        else:
            self.command_failed.emit(f"Failed to go forward: {msg}")
    
    def refresh(self):
        """Refresh the current page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke "r" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Refreshed page")
        else:
            self.command_failed.emit(f"Failed to refresh: {msg}")
    
    def bookmark_page(self):
        """Bookmark the current page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke "d" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Bookmarked page")
        else:
            self.command_failed.emit(f"Failed to bookmark: {msg}")
    
    def go_to_url(self, url):
        """Navigate to a specific URL"""
        # Add https:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        script = f'''
        tell application "Safari"
            set URL of current tab of front window to "{url}"
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit(f"Navigating to {url}")
        else:
            self.command_failed.emit(f"Failed to navigate: {msg}")
    
    def search(self, query):
        """Search using the default search engine"""
        # URL encode the search query
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        script = f'''
        tell application "Safari"
            set URL of current tab of front window to "{search_url}"
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit(f"Searching for: {query}")
        else:
            self.command_failed.emit(f"Failed to search: {msg}")
    
    def zoom_in(self):
        """Zoom in on the page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke "+" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Zoomed in")
        else:
            self.command_failed.emit(f"Failed to zoom: {msg}")
    
    def zoom_out(self):
        """Zoom out on the page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke "-" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Zoomed out")
        else:
            self.command_failed.emit(f"Failed to zoom: {msg}")
    
    def find_on_page(self, text=None):
        """Open find dialog or search for text"""
        if text:
            # Open find and type the text
            script = f'''
            tell application "System Events"
                tell process "Safari"
                    keystroke "f" using command down
                    delay 0.2
                    keystroke "{text}"
                end tell
            end tell
            '''
            success, msg = self.execute_applescript(script)
            if success:
                self.command_executed.emit(f"Finding: {text}")
            else:
                self.command_failed.emit(f"Failed to find: {msg}")
        else:
            # Just open the find dialog
            script = '''
            tell application "System Events"
                tell process "Safari"
                    keystroke "f" using command down
                end tell
            end tell
            '''
            success, msg = self.execute_applescript(script)
            if success:
                self.command_executed.emit("Opened find dialog")
            else:
                self.command_failed.emit(f"Failed to open find: {msg}")
    
    def scroll_up(self):
        """Scroll up on the page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                key code 126
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled up")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def scroll_down(self):
        """Scroll down on the page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                key code 125
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled down")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke (ASCII character 28) using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled to top")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        script = '''
        tell application "System Events"
            tell process "Safari"
                keystroke (ASCII character 31) using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled to bottom")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def get_current_url(self):
        """Get the URL of the current tab"""
        script = '''
        tell application "Safari"
            return URL of current tab of front window
        end tell
        '''
        success, url = self.execute_applescript(script)
        if success:
            return url.strip()
        return None


class ChromeCommands(BrowserCommandHandler):
    """Command handler for Google Chrome browser"""
    
    def __init__(self):
        super().__init__("Google Chrome")
    
    def close_tab(self):
        """Close the current tab"""
        script = '''
        tell application "Google Chrome"
            close active tab of front window
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Closed current tab")
        else:
            self.command_failed.emit(f"Failed to close tab: {msg}")
    
    def close_all_tabs(self):
        """Close all tabs in current window"""
        script = '''
        tell application "Google Chrome"
            close every tab of front window
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Closed all tabs")
        else:
            self.command_failed.emit(f"Failed to close tabs: {msg}")
    
    def new_tab(self, url=None):
        """Open a new tab, optionally with a URL"""
        if url:
            script = f'''
            tell application "Google Chrome"
                tell front window
                    make new tab with properties {{URL:"{url}"}}
                end tell
            end tell
            '''
        else:
            script = '''
            tell application "Google Chrome"
                tell front window
                    make new tab
                end tell
            end tell
            '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Opened new tab")
        else:
            self.command_failed.emit(f"Failed to open tab: {msg}")
    
    def go_back(self):
        """Navigate back in history"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "[" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Navigated back")
        else:
            self.command_failed.emit(f"Failed to go back: {msg}")
    
    def go_forward(self):
        """Navigate forward in history"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "]" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Navigated forward")
        else:
            self.command_failed.emit(f"Failed to go forward: {msg}")
    
    def refresh(self):
        """Refresh the current page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "r" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Refreshed page")
        else:
            self.command_failed.emit(f"Failed to refresh: {msg}")
    
    def bookmark_page(self):
        """Bookmark the current page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "d" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Bookmarked page")
        else:
            self.command_failed.emit(f"Failed to bookmark: {msg}")
    
    def go_to_url(self, url):
        """Navigate to a specific URL"""
        # Add https:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        script = f'''
        tell application "Google Chrome"
            set URL of active tab of front window to "{url}"
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit(f"Navigating to {url}")
        else:
            self.command_failed.emit(f"Failed to navigate: {msg}")
    
    def search(self, query):
        """Search using the default search engine"""
        # URL encode the search query
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        script = f'''
        tell application "Google Chrome"
            set URL of active tab of front window to "{search_url}"
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit(f"Searching for: {query}")
        else:
            self.command_failed.emit(f"Failed to search: {msg}")
    
    def zoom_in(self):
        """Zoom in on the page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "+" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Zoomed in")
        else:
            self.command_failed.emit(f"Failed to zoom: {msg}")
    
    def zoom_out(self):
        """Zoom out on the page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke "-" using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Zoomed out")
        else:
            self.command_failed.emit(f"Failed to zoom: {msg}")
    
    def find_on_page(self, text=None):
        """Open find dialog or search for text"""
        if text:
            # Open find and type the text
            script = f'''
            tell application "System Events"
                tell process "Google Chrome"
                    keystroke "f" using command down
                    delay 0.2
                    keystroke "{text}"
                end tell
            end tell
            '''
            success, msg = self.execute_applescript(script)
            if success:
                self.command_executed.emit(f"Finding: {text}")
            else:
                self.command_failed.emit(f"Failed to find: {msg}")
        else:
            # Just open the find dialog
            script = '''
            tell application "System Events"
                tell process "Google Chrome"
                    keystroke "f" using command down
                end tell
            end tell
            '''
            success, msg = self.execute_applescript(script)
            if success:
                self.command_executed.emit("Opened find dialog")
            else:
                self.command_failed.emit(f"Failed to open find: {msg}")
    
    def scroll_up(self):
        """Scroll up on the page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                key code 126
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled up")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def scroll_down(self):
        """Scroll down on the page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                key code 125
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled down")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def scroll_to_top(self):
        """Scroll to top of page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke (ASCII character 28) using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled to top")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        script = '''
        tell application "System Events"
            tell process "Google Chrome"
                keystroke (ASCII character 31) using command down
            end tell
        end tell
        '''
        success, msg = self.execute_applescript(script)
        if success:
            self.command_executed.emit("Scrolled to bottom")
        else:
            self.command_failed.emit(f"Failed to scroll: {msg}")
    
    def get_current_url(self):
        """Get the URL of the current tab"""
        script = '''
        tell application "Google Chrome"
            return URL of active tab of front window
        end tell
        '''
        success, url = self.execute_applescript(script)
        if success:
            return url.strip()
        return None


class BrowserCommandRouter(QObject):
    """Routes browser commands to the appropriate browser handler"""
    
    command_executed = pyqtSignal(str)
    command_failed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.handlers = {
            'Safari': SafariCommands(),
            'Google Chrome': ChromeCommands(),
            'Chrome': ChromeCommands(),  # Alias for Google Chrome
        }
        
        # Connect all handler signals
        for handler in self.handlers.values():
            handler.command_executed.connect(self.command_executed.emit)
            handler.command_failed.connect(self.command_failed.emit)
        
        self.current_browser = None
    
    def set_active_browser(self, browser_name):
        """Set which browser is currently active"""
        self.current_browser = browser_name
        print(f"Browser command router set to: {browser_name}")
    
    def get_handler(self):
        """Get the handler for the current browser"""
        if not self.current_browser:
            return None
        
        # Try exact match first
        if self.current_browser in self.handlers:
            return self.handlers[self.current_browser]
        
        # Try partial match
        for key, handler in self.handlers.items():
            if key.lower() in self.current_browser.lower():
                return handler
        
        return None
    
    def execute_command(self, command, *args, **kwargs):
        """Execute a browser command on the active browser"""
        handler = self.get_handler()
        
        if not handler:
            self.command_failed.emit(f"No handler for browser: {self.current_browser}")
            return
        
        # Check if the handler has this command
        if not hasattr(handler, command):
            self.command_failed.emit(f"Unknown browser command: {command}")
            return
        
        # Execute the command
        try:
            method = getattr(handler, command)
            method(*args, **kwargs)
        except Exception as e:
            self.command_failed.emit(f"Error executing {command}: {str(e)}")

