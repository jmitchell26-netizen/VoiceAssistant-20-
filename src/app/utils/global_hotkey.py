"""
Global Hotkey Manager
Allows voice assistant to be activated from any application without switching focus
"""

from PyQt6.QtCore import QObject, pyqtSignal
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import threading


class GlobalHotkeyManager(QObject):
    """Manages global keyboard shortcuts that work across all applications"""
    
    # Signals
    hotkey_triggered = pyqtSignal(str)  # Emits the hotkey name
    toggle_listening = pyqtSignal()  # For Ctrl+Space toggle
    
    def __init__(self):
        super().__init__()
        self.listener = None
        self.is_running = False
        self.current_keys = set()
        
        # Define hotkey combinations
        self.hotkeys = {
            'toggle_listening': {Key.ctrl_l, Key.space},  # Left Ctrl + Space
            'toggle_listening_r': {Key.ctrl_r, Key.space},  # Right Ctrl + Space (also works)
        }
        
        print("Global hotkey manager initialized")
        print("Hotkeys available:")
        print("  - Ctrl+Space: Toggle voice listening")
    
    def start(self):
        """Start listening for global hotkeys"""
        if self.is_running:
            return
        
        print("Starting global hotkey listener...")
        self.is_running = True
        
        # Start the listener in a separate thread
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        print("✅ Global hotkeys active: Press Ctrl+Space to toggle voice listening")
    
    def stop(self):
        """Stop listening for global hotkeys"""
        if not self.is_running:
            return
        
        print("Stopping global hotkey listener...")
        self.is_running = False
        
        if self.listener:
            self.listener.stop()
            self.listener = None
        
        self.current_keys.clear()
        print("Global hotkeys stopped")
    
    def _normalize_key(self, key):
        """Normalize key representation for comparison"""
        # Handle both Key enum and KeyCode
        if isinstance(key, KeyCode):
            return key
        return key
    
    def _on_press(self, key):
        """Called when a key is pressed"""
        if not self.is_running:
            return
        
        try:
            # Add the key to current pressed keys
            self.current_keys.add(self._normalize_key(key))
            
            # Check if any hotkey combination is pressed
            self._check_hotkeys()
            
        except Exception as e:
            print(f"Error in hotkey press handler: {e}")
    
    def _on_release(self, key):
        """Called when a key is released"""
        if not self.is_running:
            return
        
        try:
            # Remove the key from current pressed keys
            normalized_key = self._normalize_key(key)
            if normalized_key in self.current_keys:
                self.current_keys.remove(normalized_key)
        except Exception as e:
            print(f"Error in hotkey release handler: {e}")
    
    def _check_hotkeys(self):
        """Check if the currently pressed keys match any hotkey combination"""
        # Check for Ctrl+Space (either left or right Ctrl)
        if self.hotkeys['toggle_listening'].issubset(self.current_keys) or \
           self.hotkeys['toggle_listening_r'].issubset(self.current_keys):
            print("🎤 Ctrl+Space detected - toggling voice listening")
            self.toggle_listening.emit()
            self.hotkey_triggered.emit('toggle_listening')
            
            # Clear keys to prevent repeated triggers
            # (wait for release before allowing another trigger)
            self.current_keys.clear()
    
    def cleanup(self):
        """Clean up resources"""
        self.stop()
    
    def __del__(self):
        """Destructor"""
        self.cleanup()


class HotkeyConfig:
    """Configuration for customizable hotkeys (for future enhancement)"""
    
    DEFAULT_HOTKEYS = {
        'toggle_listening': 'Ctrl+Space',
        'start_typing': 'Ctrl+Shift+T',
        'stop_all': 'Ctrl+Shift+S',
        'show_commands': 'Ctrl+Shift+H',
    }
    
    @classmethod
    def get_hotkey_display(cls, action):
        """Get human-readable hotkey string"""
        return cls.DEFAULT_HOTKEYS.get(action, 'Not set')

