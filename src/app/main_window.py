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
from .utils.settings_manager import SettingsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize managers before UI
        self.settings_manager = SettingsManager()
        self.theme_manager = ThemeManager()
        self.voice_widget = None
        self.help_center = None
        self.floating_button = None
        self.init_ui()
        
    def closeEvent(self, event):
        """Handle application closure"""
        if self.voice_widget:
            self.voice_widget.voice_manager.cleanup()
        super().closeEvent(event)
        
    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Voice Assistant")
        self.setMinimumSize(800, 600)
        
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
        try:
            # Initialize main widgets
            self.voice_widget = VoiceWidget(settings_manager=self.settings_manager)
            self.help_center = HelpCenter()
            
            # Add widgets to stack if successfully created
            if self.voice_widget and self.help_center:
                self.stacked_widget.addWidget(self.voice_widget)
                self.stacked_widget.addWidget(self.help_center)
            
            # Create floating microphone button
            print("Creating floating button...")
            self.floating_button = FloatingButton(self)
            print(f"Floating button created: {self.floating_button}")
            
            if self.floating_button:
                # Connect floating button to voice widget
                self.floating_button.clicked_to_toggle.connect(self.voice_widget.handle_global_toggle)
                # Update floating button state when voice state changes
                self.voice_widget.voice_manager.state_changed.connect(self.update_floating_button_state)
                # Update floating button for browser mode
                self.voice_widget.window_detector.browser_active.connect(lambda b: self.floating_button.set_browser_mode(True))
                self.voice_widget.window_detector.browser_inactive.connect(lambda: self.floating_button.set_browser_mode(False))
                
                # IMPORTANT: Show the floating button
                print("Showing floating button...")
                self.floating_button.show()
                print(f"✓ Floating button should now be visible at position: {self.floating_button.pos()}")
            
            # Show onboarding only if not completed
            if not self.settings_manager.get_setting('interface', 'onboarding_completed'):
                self.show_onboarding()
            
        except Exception as e:
            print(f"Error initializing widgets: {str(e)}")
            raise  # Re-raise the exception to be caught by main error handler
        
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
        if self.help_center:
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
        self.settings_manager.update_setting('interface', 'onboarding_completed', True)
        self.settings_manager.update_setting('interface', 'skip_intro', True)
        
    def navigate_back(self):
        """Go back to the previous page"""
        if self.navigation_history:
            previous_widget = self.navigation_history.pop()
            self.stacked_widget.setCurrentWidget(previous_widget)
            
    def return_home(self):
        """Return to the main voice widget"""
        if self.voice_widget and self.stacked_widget.currentWidget() != self.voice_widget:
            self.navigation_history.append(self.stacked_widget.currentWidget())
            self.stacked_widget.setCurrentWidget(self.voice_widget)
    
    def update_floating_button_state(self, state):
        """Update floating button visual state based on voice manager state"""
        if self.floating_button:
            # Update listening state (listening, processing, or ready)
            is_active = state in ['listening', 'processing']
            self.floating_button.set_listening(is_active)