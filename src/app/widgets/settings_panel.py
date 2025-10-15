from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QDialog, QTabWidget,
                             QCheckBox, QSpinBox, QComboBox,
                             QFormLayout, QHBoxLayout, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta

class SettingsDialog(QDialog):
    settings_updated = pyqtSignal(dict)  # Emitted when settings are saved

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add tabs
        tabs.addTab(GeneralSettings(), "General")
        tabs.addTab(VoiceSettings(), "Voice")
        tabs.addTab(ShortcutSettings(), "Shortcuts")
        tabs.addTab(AppearanceSettings(), "Appearance")
        
        layout.addWidget(tabs)
        
        # Add save/cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # Set size
        self.setMinimumSize(500, 400)
        
    def save_settings(self):
        # TODO: Collect and save all settings
        self.accept()

class GeneralSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout(self)
        
        # Startup settings
        self.start_with_system = QCheckBox("Start with system")
        self.show_floating_button = QCheckBox("Show floating button")
        self.start_minimized = QCheckBox("Start minimized")
        
        layout.addRow("Startup:", self.start_with_system)
        layout.addRow("Floating Button:", self.show_floating_button)
        layout.addRow("Window:", self.start_minimized)
        
        # Language selection
        self.language_select = QComboBox()
        self.language_select.addItems(["English", "Spanish", "French", "German"])
        layout.addRow("Language:", self.language_select)

class VoiceSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout(self)
        
        # Voice recognition settings
        self.wake_word = QLineEdit("Hey Assistant")
        self.sensitivity = QSpinBox()
        self.sensitivity.setRange(0, 100)
        self.sensitivity.setValue(50)
        
        self.continuous_listening = QCheckBox("Enable continuous listening")
        self.audio_feedback = QCheckBox("Enable audio feedback")
        self.auto_punctuation = QCheckBox("Enable auto-punctuation")
        
        layout.addRow("Wake Word:", self.wake_word)
        layout.addRow("Microphone Sensitivity:", self.sensitivity)
        layout.addRow("Listening:", self.continuous_listening)
        layout.addRow("Feedback:", self.audio_feedback)
        layout.addRow("Punctuation:", self.auto_punctuation)

class ShortcutSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Shortcuts list
        shortcuts = [
            ("Start/Stop Listening", "Ctrl+Space"),
            ("Show/Hide Window", "Ctrl+Alt+V"),
            ("Quick Commands", "Ctrl+Q"),
            ("Switch Mode", "Ctrl+M")
        ]
        
        form_layout = QFormLayout()
        for action, default_shortcut in shortcuts:
            shortcut_edit = QLineEdit(default_shortcut)
            shortcut_edit.setPlaceholderText("Click to set shortcut")
            form_layout.addRow(action + ":", shortcut_edit)
            
        layout.addLayout(form_layout)
        
        # Reset button
        reset_button = QPushButton("Reset to Defaults")
        layout.addWidget(reset_button)

class AppearanceSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout(self)
        
        # Theme selection
        self.theme_select = QComboBox()
        self.theme_select.addItems(["System", "Light", "Dark"])
        layout.addRow("Theme:", self.theme_select)
        
        # Opacity slider
        self.opacity = QSpinBox()
        self.opacity.setRange(50, 100)
        self.opacity.setValue(100)
        self.opacity.setSuffix("%")
        layout.addRow("Window Opacity:", self.opacity)
        
        # Animation settings
        self.enable_animations = QCheckBox("Enable animations")
        self.enable_animations.setChecked(True)
        layout.addRow("Animations:", self.enable_animations)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(12)
        layout.addRow("Font Size:", self.font_size)
