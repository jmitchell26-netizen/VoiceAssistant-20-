from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal

class CommandSuggestions(QWidget):
    command_selected = pyqtSignal(str)  # Emitted when a suggestion is selected

    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Suggested Commands")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        
        # Suggestions list
        self.suggestions_list = QListWidget()
        self.suggestions_list.itemClicked.connect(self._handle_selection)
        layout.addWidget(self.suggestions_list)
        
        # Style
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:hover {
                background: #353535;
            }
            QListWidget::item:selected {
                background: #454545;
                color: #fff;
            }
        """)
        
    def update_suggestions(self, suggestions):
        """Update the suggestions list"""
        self.suggestions_list.clear()
        for suggestion in suggestions:
            item = QListWidgetItem(suggestion)
            self.suggestions_list.addItem(item)
            
    def _handle_selection(self, item):
        """Handle suggestion selection"""
        self.command_selected.emit(item.text())
