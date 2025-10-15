from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta

class QuickActionsPanel(QDialog):
    action_triggered = pyqtSignal(str)  # Emitted when an action is selected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quick Actions")
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Quick Actions")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Grid of quick actions
        grid = QGridLayout()
        
        # Common actions with icons
        actions = [
            ("Start Typing", "fa5s.keyboard", "start typing"),
            ("Stop Listening", "fa5s.microphone-slash", "stop listening"),
            ("Open Browser", "fa5s.globe", "open browser"),
            ("Open Mail", "fa5s.envelope", "open mail"),
            ("Search Web", "fa5s.search", "search"),
            ("System Volume", "fa5s.volume-up", "volume"),
            ("System Settings", "fa5s.cog", "open settings"),
            ("Help", "fa5s.question-circle", "help")
        ]
        
        # Add buttons to grid
        for i, (label, icon, command) in enumerate(actions):
            row = i // 2
            col = i % 2
            
            button = QPushButton(qta.icon(icon), label)
            button.setStyleSheet("""
                QPushButton {
                    padding: 10px;
                    border-radius: 5px;
                    background: #353535;
                    color: white;
                    text-align: left;
                }
                QPushButton:hover {
                    background: #454545;
                }
                QPushButton:pressed {
                    background: #555555;
                }
            """)
            button.clicked.connect(lambda checked, cmd=command: self.action_triggered.emit(cmd))
            grid.addWidget(button, row, col)
            
        layout.addLayout(grid)
        
        # Style the panel
        self.setStyleSheet("""
            QuickActionsPanel {
                background: #2D2D2D;
                border: 1px solid #555;
                border-radius: 10px;
            }
        """)
        
        # Set size
        self.setFixedWidth(400)
        
    def show_at_button(self, button):
        """Show the panel below the quick actions button"""
        pos = button.mapToGlobal(button.rect().bottomLeft())
        self.move(pos)
        self.show()
        
    def mousePressEvent(self, event):
        """Close panel when clicking outside"""
        if not self.rect().contains(event.pos()):
            self.close()
        super().mousePressEvent(event)
