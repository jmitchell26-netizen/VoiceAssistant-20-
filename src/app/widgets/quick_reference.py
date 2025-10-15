from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QScrollArea, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
import qtawesome as qta

from ..utils.command_database import CommandDatabase

class CommandCard(QFrame):
    def __init__(self, command_info):
        super().__init__()
        self.init_ui(command_info)
        
    def init_ui(self, command_info):
        layout = QVBoxLayout(self)
        
        # Command phrase
        phrase = QLabel(command_info['info']['phrase'])
        phrase.setStyleSheet("font-weight: bold; color: #007AFF;")
        layout.addWidget(phrase)
        
        # Description
        description = QLabel(command_info['info']['description'])
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Example
        if command_info['info']['examples']:
            example = QLabel(f"Example: {command_info['info']['examples'][0]}")
            example.setStyleSheet("font-style: italic; color: #666;")
            layout.addWidget(example)
            
        # Shortcut if available
        if 'shortcut' in command_info['info']:
            shortcut = QLabel(f"⌨️ {command_info['info']['shortcut']}")
            shortcut.setStyleSheet("color: #666;")
            layout.addWidget(shortcut)
            
        # Style the card
        self.setStyleSheet("""
            CommandCard {
                background: #353535;
                border-radius: 8px;
                padding: 10px;
            }
            QLabel {
                color: white;
            }
        """)

class QuickReferenceCard(QWidget):
    def __init__(self):
        super().__init__()
        self.command_db = CommandDatabase()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Quick Reference")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Create scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Container for command cards
        container = QWidget()
        grid_layout = QGridLayout(container)
        
        # Get common commands
        commands = self.command_db.get_quick_reference()
        
        # Add command cards to grid
        for i, command in enumerate(commands):
            card = CommandCard(command)
            row = i // 2  # Two columns
            col = i % 2
            grid_layout.addWidget(card, row, col)
            
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Style
        self.setStyleSheet("""
            QuickReferenceCard {
                background: #2D2D2D;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                color: white;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
    def update_commands(self, context=None):
        """Update commands based on context"""
        if context:
            commands = self.command_db.get_contextual_suggestions(context)
        else:
            commands = self.command_db.get_quick_reference()
            
        # Clear and rebuild the grid
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QScrollArea):
                scroll = widget
                container = scroll.widget()
                grid_layout = container.layout()
                
                # Clear grid
                for j in reversed(range(grid_layout.count())):
                    grid_layout.itemAt(j).widget().deleteLater()
                
                # Add new command cards
                for i, command in enumerate(commands):
                    card = CommandCard(command)
                    row = i // 2
                    col = i % 2
                    grid_layout.addWidget(card, row, col)
                break
