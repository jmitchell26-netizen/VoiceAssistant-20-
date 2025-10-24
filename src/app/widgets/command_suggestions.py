from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt6.QtCore import pyqtSignal

class CommandSuggestions(QWidget):
    command_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Suggested Commands")
        layout.addWidget(title)
        
        # List widget for suggestions
        self.suggestions_list = QListWidget()
        self.suggestions_list.itemClicked.connect(self._handle_selection)
        layout.addWidget(self.suggestions_list)

    def update_suggestions(self, suggestions):
        """Update the list of command suggestions"""
        self.suggestions_list.clear()
        if isinstance(suggestions, list):
            self.suggestions_list.addItems(suggestions)

    def _handle_selection(self, item):
        """Emit the selected command"""
        self.command_selected.emit(item.text())