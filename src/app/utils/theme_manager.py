from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
import darkdetect

class ThemeManager:
    def __init__(self):
        self.current_theme = 'light'
        self.setup_theme()
        
    def setup_theme(self):
        # Detect system theme
        is_dark = darkdetect.isDark()
        self.set_theme('dark' if is_dark else 'light')
        
    def set_theme(self, theme):
        self.current_theme = theme
        palette = QPalette()
        
        if theme == 'dark':
            # Dark theme colors
            palette.setColor(QPalette.ColorRole.Window, QColor("#1E1E1E"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#2D2D2D"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#353535"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#353535"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Link, QColor("#60A5FA"))
        else:
            # Light theme colors
            palette.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#F5F5F5"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#EAEAEA"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#F0F0F0"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Link, QColor("#007AFF"))
            
        QApplication.instance().setPalette(palette)
        
    def toggle_theme(self):
        new_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.set_theme(new_theme)
