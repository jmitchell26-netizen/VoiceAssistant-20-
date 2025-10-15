from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QTreeWidget, QTreeWidgetItem,
                             QSplitter, QTextBrowser)
from PyQt6.QtCore import Qt

class HelpCenter(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search commands...")
        self.search_bar.textChanged.connect(self.search_commands)
        layout.addWidget(self.search_bar)
        
        # Create splitter for categories and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Command categories tree
        self.categories_tree = QTreeWidget()
        self.categories_tree.setHeaderLabel("Categories")
        self.setup_categories()
        splitter.addWidget(self.categories_tree)
        
        # Command details view
        self.details_view = QTextBrowser()
        self.details_view.setOpenExternalLinks(True)
        splitter.addWidget(self.details_view)
        
        layout.addWidget(splitter)
        
        # Connect signals
        self.categories_tree.itemClicked.connect(self.show_command_details)
        
    def setup_categories(self):
        categories = {
            "📝 Voice Typing": ["Start typing", "Stop typing", "Delete that"],
            "🎯 Navigation": ["Switch mode", "Open app", "Close app"],
            "🔤 Text Formatting": ["New line", "Period", "Comma"],
            "⚙️ Settings": ["Open settings", "Change theme", "Configure shortcuts"]
        }
        
        for category, commands in categories.items():
            category_item = QTreeWidgetItem([category])
            self.categories_tree.addTopLevelItem(category_item)
            
            for command in commands:
                command_item = QTreeWidgetItem([command])
                category_item.addChild(command_item)
                
    def search_commands(self, text):
        # TODO: Implement command search
        pass
        
    def show_command_details(self, item):
        # Example command details
        if item.parent():  # This is a command, not a category
            command_name = item.text(0)
            details = f"""
                <h2>{command_name}</h2>
                <p><b>Voice Command:</b> "{command_name}"</p>
                <p><b>Description:</b> Example description for {command_name}</p>
                <p><b>Usage:</b> Example usage instructions</p>
                <p><b>Tips:</b> Example tips and tricks</p>
            """
            self.details_view.setHtml(details)
