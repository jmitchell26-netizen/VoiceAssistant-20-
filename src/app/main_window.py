from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QStackedWidget, QHBoxLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
import qtawesome as qta

from .widgets.floating_button import FloatingButton
from .widgets.voice_widget import VoiceWidget
from .widgets.help_center import HelpCenter
from .widgets.onboarding import OnboardingDialog
from .widgets.settings_panel import SettingsDialog
from .utils.theme_manager import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Voice Assistant")
        self.setMinimumSize(800, 600)
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create header with controls
        header = self.create_header()
        layout.addWidget(header)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create and add main views
        self.voice_widget = VoiceWidget()
        self.help_center = HelpCenter()
        
        self.stacked_widget.addWidget(self.voice_widget)
        self.stacked_widget.addWidget(self.help_center)
        
        # Create floating microphone button
        self.floating_button = FloatingButton(self)
        self.floating_button.show()
        
        # Show onboarding for first-time users
        self.show_onboarding()
        
        # Initialize navigation history
        self.navigation_history = []
        
    def create_header(self):
        header = QWidget()
        header_layout = QVBoxLayout(header)
        
        # Create navigation buttons
        nav_layout = QHBoxLayout()
        
        # Back button
        back_button = QPushButton(qta.icon('fa5s.arrow-left'), "")
        back_button.setToolTip("Go Back")
        back_button.setFixedSize(32, 32)
        
        # Home button
        home_button = QPushButton(qta.icon('fa5s.home'), "")
        home_button.setToolTip("Return to Main")
        home_button.setFixedSize(32, 32)
        
        # Help and Settings buttons
        help_button = QPushButton(qta.icon('fa5s.question-circle'), "Help")
        settings_button = QPushButton(qta.icon('fa5s.cog'), "Settings")
        
        # Add buttons to navigation layout
        nav_layout.addWidget(back_button)
        nav_layout.addWidget(home_button)
        nav_layout.addStretch()  # This pushes help/settings to the right
        nav_layout.addWidget(help_button)
        nav_layout.addWidget(settings_button)
        
        # Add navigation layout to header
        header_layout.addLayout(nav_layout)
        
        # Connect signals
        help_button.clicked.connect(self.show_help)
        settings_button.clicked.connect(self.show_settings)
        back_button.clicked.connect(self.navigate_back)
        home_button.clicked.connect(self.return_home)
        
        return header
    
    def show_help(self):
        """Show the help center and add current page to navigation history"""
        self.navigation_history.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.help_center)
    
    def show_settings(self):
        """Show the settings dialog"""
        settings = SettingsDialog(self)
        settings.settings_updated.connect(self.apply_settings)
        settings.exec()
        
    def apply_settings(self, settings):
        """Apply updated settings"""
        # TODO: Apply the new settings to all components
        pass
        
    def show_onboarding(self):
        """Show the onboarding dialog for first-time users"""
        onboarding = OnboardingDialog(self)
        onboarding.completed.connect(self.onboarding_completed)
        onboarding.exec()
        
    def onboarding_completed(self):
        """Handle onboarding completion"""
        # TODO: Save onboarding completion status
        pass
        
    def navigate_back(self):
        """Go back to the previous page"""
        if self.navigation_history:
            previous_widget = self.navigation_history.pop()
            self.stacked_widget.setCurrentWidget(previous_widget)
            
    def return_home(self):
        """Return to the main voice widget"""
        if self.stacked_widget.currentWidget() != self.voice_widget:
            self.navigation_history.append(self.stacked_widget.currentWidget())
            self.stacked_widget.setCurrentWidget(self.voice_widget)