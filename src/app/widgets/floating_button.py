from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
import qtawesome as qta

class FloatingButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.dragging = False
        
    def init_ui(self):
        # Set up the floating button appearance
        self.setFixedSize(48, 48)
        self.setIcon(qta.icon('fa5s.microphone'))
        self.setIconSize(self.size() * 0.6)
        
        # Remove window frame and keep on top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                          Qt.WindowType.WindowStaysOnTopHint |
                          Qt.WindowType.Tool)
        
        # Enable mouse tracking
        self.setMouseTracking(True)
        
        # Set initial position
        screen_geometry = self.screen().geometry()
        self.move(screen_geometry.width() - self.width() - 20,
                 screen_geometry.height() - self.height() - 20)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.pos()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        self.dragging = False
        
    def mouseDoubleClickEvent(self, event):
        # Show main window on double click
        if self.parent():
            self.parent().show()
            self.parent().activateWindow()
