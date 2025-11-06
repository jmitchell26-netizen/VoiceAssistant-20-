"""
Active Window Detector
Monitors the currently active application on macOS and emits signals when it changes.
"""

from PyQt6.QtCore import QObject, pyqtSignal, QTimer
import subprocess
import platform


class ActiveWindowDetector(QObject):
    """Detects and monitors the currently active application window"""
    
    # Signals
    active_app_changed = pyqtSignal(str)  # Emits the app name
    browser_active = pyqtSignal(str)  # Emits browser name (Safari, Chrome, etc.)
    browser_inactive = pyqtSignal()  # Emits when leaving a browser
    
    # Supported browsers
    BROWSERS = [
        "Safari",
        "Google Chrome",
        "Chrome",
        "Firefox",
        "Arc",
        "Brave Browser",
        "Microsoft Edge"
    ]
    
    def __init__(self, poll_interval=500):
        """
        Initialize the active window detector
        
        Args:
            poll_interval: How often to check active window in milliseconds (default 500ms)
        """
        super().__init__()
        self.poll_interval = poll_interval
        self.current_app = None
        self.current_browser = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_active_window)
        self._is_running = False
        
    def start(self):
        """Start monitoring active windows"""
        if not self._is_running and platform.system() == 'Darwin':
            print("Starting active window detection...")
            self._is_running = True
            self.timer.start(self.poll_interval)
            # Do an immediate check
            self._check_active_window()
        elif platform.system() != 'Darwin':
            print("Warning: Active window detection only supported on macOS")
    
    def stop(self):
        """Stop monitoring active windows"""
        if self._is_running:
            print("Stopping active window detection...")
            self._is_running = False
            self.timer.stop()
    
    def get_current_app(self):
        """Get the currently active application name"""
        return self.current_app
    
    def is_browser_active(self):
        """Check if a browser is currently active"""
        return self.current_browser is not None
    
    def get_active_browser(self):
        """Get the currently active browser name, or None"""
        return self.current_browser
    
    def _check_active_window(self):
        """Check which application is currently active"""
        try:
            # Use AppleScript to get the frontmost application
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
            end tell
            return frontApp
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=1
            )
            
            if result.returncode == 0:
                app_name = result.stdout.strip()
                
                # Check if the app changed
                if app_name != self.current_app:
                    self.current_app = app_name
                    self.active_app_changed.emit(app_name)
                    print(f"Active app changed to: {app_name}")
                    
                    # Check if it's a browser
                    self._check_browser_status(app_name)
            else:
                # Permission error or other issue
                error_msg = result.stderr.strip()
                if "not allowed" in error_msg.lower() or "permission" in error_msg.lower():
                    print("⚠️  Accessibility permission needed!")
                    print("Go to: System Settings > Privacy & Security > Accessibility")
                    print("Add Python or your terminal app to the allowed list.")
                    self.stop()  # Stop trying until permission is granted
                
        except subprocess.TimeoutExpired:
            print("Warning: AppleScript timeout checking active window")
        except Exception as e:
            print(f"Error checking active window: {str(e)}")
    
    def _check_browser_status(self, app_name):
        """Check if the app is a supported browser and emit appropriate signals"""
        # Check if it's a browser
        is_browser = False
        browser_name = None
        
        for browser in self.BROWSERS:
            if browser.lower() in app_name.lower():
                is_browser = True
                browser_name = browser
                break
        
        if is_browser:
            # Browser became active
            if self.current_browser != browser_name:
                self.current_browser = browser_name
                self.browser_active.emit(browser_name)
                print(f"🌐 Browser mode activated: {browser_name}")
        else:
            # Non-browser became active
            if self.current_browser is not None:
                self.current_browser = None
                self.browser_inactive.emit()
                print("Browser mode deactivated")
    
    def cleanup(self):
        """Clean up resources"""
        self.stop()

