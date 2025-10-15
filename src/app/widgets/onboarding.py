from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QStackedWidget, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta

class OnboardingDialog(QDialog):
    completed = pyqtSignal()  # Emitted when onboarding is completed

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Voice Assistant")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create stacked widget for multiple pages
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        # Create pages
        self.create_welcome_page()
        self.create_voice_typing_page()
        self.create_commands_page()
        self.create_quick_actions_page()
        self.create_finish_page()
        
        # Style
        self.setStyleSheet("""
            OnboardingDialog {
                background: #2D2D2D;
                border: 1px solid #555;
                border-radius: 10px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 5px;
                background: #007AFF;
                color: white;
            }
            QPushButton:hover {
                background: #0064D1;
            }
        """)
        
        # Set size
        self.setFixedSize(600, 400)
        
    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Welcome message
        title = QLabel("Welcome to Voice Assistant!")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        description = QLabel(
            "Let's get you started with your new voice assistant. "
            "This quick guide will show you the main features and how to use them."
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Next button
        next_button = QPushButton("Start Tour")
        next_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(next_button)
        
        self.stack.addWidget(page)
        
    def create_voice_typing_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Voice typing info
        title = QLabel("Voice Typing")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        features = [
            "🎤 Click 'Start Typing' or say 'Start typing'",
            "📝 Speak naturally and see your words appear",
            "⌨️ Use commands like 'period', 'new line', 'delete that'",
            "⏹️ Say 'stop typing' or click the button to finish"
        ]
        
        for feature in features:
            label = QLabel(feature)
            layout.addWidget(label)
        
        # Navigation buttons
        button_layout = QVBoxLayout()
        next_button = QPushButton("Next")
        next_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        button_layout.addWidget(next_button)
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)
        
        self.stack.addWidget(page)
        
    def create_commands_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Voice Commands")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        commands = [
            "🖥️ 'Open [app]' - Launch applications",
            "🔍 'Search for [topic]' - Web search",
            "🔊 'Volume [0-100]' - Adjust system volume",
            "💻 'Switch to [app]' - Switch applications"
        ]
        
        for command in commands:
            label = QLabel(command)
            layout.addWidget(label)
        
        # Navigation
        button_layout = QVBoxLayout()
        next_button = QPushButton("Next")
        next_button.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        button_layout.addWidget(next_button)
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)
        
        self.stack.addWidget(page)
        
    def create_quick_actions_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Quick Actions")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        description = QLabel(
            "Access common commands quickly:\n"
            "• Click the ⚡ button for quick actions\n"
            "• Use the floating microphone button\n"
            "• Check the help center for all commands"
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Navigation
        button_layout = QVBoxLayout()
        next_button = QPushButton("Next")
        next_button.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        button_layout.addWidget(next_button)
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)
        
        self.stack.addWidget(page)
        
    def create_finish_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("You're Ready!")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        description = QLabel(
            "You're all set to use your voice assistant!\n\n"
            "Remember to check the help center if you need assistance.\n"
            "You can always access this guide from the settings menu."
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Finish button
        finish_button = QPushButton("Get Started")
        finish_button.clicked.connect(self.complete_onboarding)
        layout.addWidget(finish_button)
        
        self.stack.addWidget(page)
        
    def complete_onboarding(self):
        self.completed.emit()
        self.accept()
