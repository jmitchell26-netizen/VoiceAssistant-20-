"""
Keyboard Typing Utility
Simulates keyboard typing for voice dictation into applications
"""

from pynput.keyboard import Controller, Key
import time


class KeyboardTyper:
    """Handles keyboard typing simulation for dictation"""
    
    def __init__(self):
        self.keyboard = Controller()
        self.typing_delay = 0.01  # Small delay between characters for reliability
        self.word_delay = 0.02    # Slightly longer delay between words
    
    def type_text(self, text, delay=None):
        """
        Type text using keyboard simulation
        
        Args:
            text: The text to type
            delay: Optional custom delay between characters (seconds)
        """
        if not text:
            return
        
        char_delay = delay if delay is not None else self.typing_delay
        
        # Split into words to handle spacing better
        words = text.split(' ')
        
        for i, word in enumerate(words):
            # Type each character in the word
            for char in word:
                self._type_character(char)
                time.sleep(char_delay)
            
            # Add space between words (except after last word)
            if i < len(words) - 1:
                self.keyboard.press(' ')
                self.keyboard.release(' ')
                time.sleep(self.word_delay)
    
    def _type_character(self, char):
        """
        Type a single character, handling special characters
        
        Args:
            char: Character to type
        """
        try:
            # Handle newlines
            if char == '\n':
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
            # Handle tabs
            elif char == '\t':
                self.keyboard.press(Key.tab)
                self.keyboard.release(Key.tab)
            # Handle regular characters
            else:
                self.keyboard.press(char)
                self.keyboard.release(char)
        except Exception as e:
            # If character can't be typed, skip it silently
            print(f"Warning: Could not type character '{char}': {e}")
    
    def press_key(self, key):
        """
        Press a special key (like Enter, Backspace, etc.)
        
        Args:
            key: Key from pynput.keyboard.Key enum
        """
        try:
            self.keyboard.press(key)
            self.keyboard.release(key)
        except Exception as e:
            print(f"Warning: Could not press key {key}: {e}")
    
    def type_with_hotkey(self, text, *modifiers):
        """
        Type text with modifier keys held (e.g., Cmd+V for paste)
        
        Args:
            text: The text/key to type
            *modifiers: Modifier keys (Key.cmd, Key.ctrl, etc.)
        """
        try:
            # Press all modifiers
            for mod in modifiers:
                self.keyboard.press(mod)
            
            # Type the text
            self.keyboard.press(text)
            self.keyboard.release(text)
            
            # Release all modifiers
            for mod in reversed(modifiers):
                self.keyboard.release(mod)
        except Exception as e:
            print(f"Warning: Hotkey typing failed: {e}")
    
    def backspace(self, count=1):
        """Delete characters using backspace"""
        for _ in range(count):
            self.press_key(Key.backspace)
            time.sleep(0.05)
    
    def set_typing_speed(self, speed='normal'):
        """
        Set typing speed
        
        Args:
            speed: 'slow', 'normal', or 'fast'
        """
        if speed == 'slow':
            self.typing_delay = 0.05
            self.word_delay = 0.1
        elif speed == 'fast':
            self.typing_delay = 0.005
            self.word_delay = 0.01
        else:  # normal
            self.typing_delay = 0.01
            self.word_delay = 0.02


class SmartTyper(KeyboardTyper):
    """
    Enhanced typer with smart features like auto-capitalization,
    space management, etc.
    """
    
    def __init__(self):
        super().__init__()
        self.last_char = ''
        self.sentence_start = True
    
    def type_smart(self, text):
        """
        Type with smart features enabled
        - Auto-capitalize after periods
        - Smart spacing around punctuation
        - Handle common typing patterns
        """
        if not text:
            return
        
        # Process text for smart features
        processed = self._apply_smart_rules(text)
        
        # Type the processed text
        self.type_text(processed)
    
    def _apply_smart_rules(self, text):
        """Apply smart typing rules to text"""
        # For now, return as-is
        # Can add rules like:
        # - Auto-capitalize after period
        # - Remove double spaces
        # - Smart quotes
        return text
    
    def reset_state(self):
        """Reset typing state"""
        self.last_char = ''
        self.sentence_start = True

