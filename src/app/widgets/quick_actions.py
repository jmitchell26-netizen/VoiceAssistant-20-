from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import pyqtSignal, Qt

class QuickActionsPanel(QFrame):
    action_triggered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Quick action buttons
        actions = [
            ("Start Typing", "start typing"),
            ("Stop Listening", "stop listening"),
            ("Open Settings", "open settings"),
            ("Show Help", "show help")
        ]
        
        for label, command in actions:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, cmd=command: self._trigger_action(cmd))
            layout.addWidget(btn)

    def show_at_button(self, button):
        """Show the panel below the button that triggered it"""
        pos = button.mapToGlobal(button.rect().bottomLeft())
        self.move(pos)
        self.show()

    def _trigger_action(self, command):
        """Emit the action and hide the panel"""
        self.action_triggered.emit(command)
        self.hide()