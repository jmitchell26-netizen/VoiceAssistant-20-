from PyQt6.QtWidgets import QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QIcon, QPainter, QColor
import qtawesome as qta

class FloatingButton(QPushButton):
    clicked_to_toggle = pyqtSignal()  # Signal for toggle listening
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.dragging = False
        self.is_listening = False
        self.browser_mode = False
        
    def init_ui(self):
        # Set up the floating button appearance
        self.setFixedSize(60, 60)
        self.update_icon()
        
        # Remove window frame and keep on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                          Qt.WindowType.WindowStaysOnTopHint |
                          Qt.WindowType.Tool)
        
        # Make the button circular and styled
        self.update_style()
        
        # Enable mouse tracking
        self.setMouseTracking(True)
        
        # Set tooltip
        self.setToolTip("Click to toggle voice listening\nCtrl+Space works from any app!\nDrag to move")
        
        # Set initial position (bottom-right corner)
        screen_geometry = self.screen().geometry()
        self.move(screen_geometry.width() - self.width() - 20,
                 screen_geometry.height() - self.height() - 100)
    
    def update_icon(self):
        """Update icon based on listening state"""
        if self.is_listening:
            self.setIcon(qta.icon('fa5s.microphone', color='white'))
        else:
            self.setIcon(qta.icon('fa5s.microphone-slash', color='white'))
        self.setIconSize(self.size() * 0.5)
    
    def update_style(self):
        """Update button style based on state"""
        if self.is_listening:
            if self.browser_mode:
                # Green for browser mode listening
                bg_color = '#4CAF50'
            else:
                # Blue for regular listening
                bg_color = '#2196F3'
        else:
            # Gray when not listening
            bg_color = '#757575'
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border-radius: 30px;
                border: 3px solid white;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(bg_color)};
                border: 3px solid #FFF;
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(bg_color)};
            }}
        """)
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color"""
        # Simple lightening - add 20 to each RGB component
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r, g, b = min(255, r + 30), min(255, g + 30), min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _darken_color(self, hex_color):
        """Darken a hex color"""
        # Simple darkening - subtract 20 from each RGB component
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r, g, b = max(0, r - 30), max(0, g - 30), max(0, b - 30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def set_listening(self, listening):
        """Update visual state when listening status changes"""
        if self.is_listening != listening:
            self.is_listening = listening
            self.update_icon()
            self.update_style()
    
    def set_browser_mode(self, active):
        """Update visual state when browser mode changes"""
        if self.browser_mode != active:
            self.browser_mode = active
            self.update_style()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.globalPosition().toPoint()
            self.drag_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            # Only start moving if dragged more than 5 pixels (prevents accidental moves when clicking)
            if (event.globalPosition().toPoint() - self.drag_start_pos).manhattanLength() > 5:
                self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # If didn't move much, treat as click
            if (event.globalPosition().toPoint() - self.drag_start_pos).manhattanLength() < 5:
                # Single click toggles listening
                self.clicked_to_toggle.emit()
            self.dragging = False
        
    def mouseDoubleClickEvent(self, event):
        # Double click shows main window
        if self.parent():
            self.parent().show()
            self.parent().activateWindow()
        event.accept()
