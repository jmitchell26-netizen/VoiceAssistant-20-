from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QProgressBar,
                             QHBoxLayout, QStackedWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
import qtawesome as qta

from ..utils.voice_recognition import VoiceRecognitionManager
from ..utils.voice_typing import VoiceTypingMode
from ..utils.command_handler import CommandHandler
from ..utils.contextual_help import ContextualHelp
from .command_suggestions import CommandSuggestions
from .quick_actions import QuickActionsPanel
from .quick_reference import QuickReferenceCard

class AudioLevelIndicator(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setTextVisible(False)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555;
                border-radius: 5px;
                background: #2D2D2D;
            }
            QProgressBar::chunk {
                background-color: #007AFF;
                border-radius: 3px;
            }
        """)

class VoiceWidget(QWidget):
    def __init__(self, settings_manager=None):
        super().__init__()
        self.settings_manager = settings_manager
        self.voice_manager = VoiceRecognitionManager()
        self.typing_mode = VoiceTypingMode(self.voice_manager)
        self.command_handler = CommandHandler()
        self.contextual_help = ContextualHelp()
        self.init_ui()
        self.setup_connections()
        
    def closeEvent(self, event):
        """Handle cleanup when widget is closed"""
        self.voice_manager.cleanup()
        super().closeEvent(event)
        
    def hideEvent(self, event):
        """Handle cleanup when widget is hidden"""
        self.voice_manager.stop_listening()
        super().hideEvent(event)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Status indicator
        self.status_label = QLabel("🎤 Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Audio level indicator
        self.audio_level = AudioLevelIndicator()
        layout.addWidget(self.audio_level)
        
        # Mode selector
        self.mode_button = QPushButton("Mode: Voice Typing")
        self.mode_button.clicked.connect(self.toggle_mode)
        layout.addWidget(self.mode_button)
        
        # Main content area (stacked widget for different modes)
        self.content_stack = QStackedWidget()
        
        # Typing mode widget
        self.typing_widget = QWidget()
        typing_layout = QVBoxLayout(self.typing_widget)
        
        self.preview_label = QLabel("Preview")
        typing_layout.addWidget(self.preview_label)
        
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setPlaceholderText("Your words will appear here...")
        typing_layout.addWidget(self.text_preview)
        
        # Command mode widget
        self.command_widget = QWidget()
        command_layout = QVBoxLayout(self.command_widget)
        
        # Command preview
        self.command_preview = QLabel("Listening for commands...")
        command_layout.addWidget(self.command_preview)
        
        # Command suggestions and quick reference
        suggestions_reference_layout = QHBoxLayout()
        
        # Left side: Command suggestions
        self.suggestions = CommandSuggestions()
        suggestions_reference_layout.addWidget(self.suggestions)
        
        # Right side: Quick reference
        self.quick_reference = QuickReferenceCard()
        suggestions_reference_layout.addWidget(self.quick_reference)
        
        command_layout.addLayout(suggestions_reference_layout)
        
        # Add widgets to stack
        self.content_stack.addWidget(self.typing_widget)
        self.content_stack.addWidget(self.command_widget)
        layout.addWidget(self.content_stack)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        self.type_button = QPushButton(qta.icon('fa5s.keyboard'), "Start Typing")
        self.command_button = QPushButton(qta.icon('fa5s.terminal'), "Command Mode")
        self.quick_commands_button = QPushButton(qta.icon('fa5s.bolt'), "Quick Commands")
        
        actions_layout.addWidget(self.type_button)
        actions_layout.addWidget(self.command_button)
        actions_layout.addWidget(self.quick_commands_button)
        
        layout.addLayout(actions_layout)
        
        # Set up button states
        self.is_typing = False
        self.is_command_mode = False
        self.update_button_states()
        
    def setup_connections(self):
        # Connect voice manager signals
        self.voice_manager.text_received.connect(self.handle_text_received)
        self.voice_manager.error_occurred.connect(self.handle_error)
        self.voice_manager.audio_level.connect(self.update_audio_level)
        self.voice_manager.state_changed.connect(self.handle_state_change)
        
        # Connect command handler signals
        self.command_handler.command_executed.connect(self.handle_command_executed)
        self.command_handler.command_failed.connect(self.handle_error)
        self.command_handler.suggestion_updated.connect(self.suggestions.update_suggestions)
        
        # Connect button signals
        self.type_button.clicked.connect(self.toggle_typing)
        self.command_button.clicked.connect(self.toggle_command_mode)
        self.quick_commands_button.clicked.connect(self.show_quick_commands)
        
        # Connect suggestions
        self.suggestions.command_selected.connect(self.handle_suggestion_selected)
        
    def toggle_typing(self):
        self.is_typing = not self.is_typing
        self.is_command_mode = False
        if self.is_typing:
            self.voice_manager.start_listening()
            self.type_button.setText("Stop Typing")
            self.status_label.setText("🎤 Listening for typing...")
            self.content_stack.setCurrentWidget(self.typing_widget)
        else:
            self.voice_manager.stop_listening()
            self.type_button.setText("Start Typing")
            self.status_label.setText("🎤 Ready")
        self.update_button_states()
        
    def toggle_command_mode(self):
        self.is_command_mode = not self.is_command_mode
        self.is_typing = False
        if self.is_command_mode:
            self.voice_manager.start_listening()
            self.command_button.setText("Stop Commands")
            self.status_label.setText("🎤 Listening for commands...")
            self.content_stack.setCurrentWidget(self.command_widget)
        else:
            self.voice_manager.stop_listening()
            self.command_button.setText("Command Mode")
            self.status_label.setText("🎤 Ready")
        self.update_button_states()
        
    def handle_text_received(self, text):
        if self.is_typing:
            processed_text = self.typing_mode.process_text(text)
            current_text = self.text_preview.toPlainText()
            if current_text:
                current_text += " "
            self.text_preview.setText(current_text + processed_text)
            
            # Update contextual help for typing mode
            help_info = self.contextual_help.get_contextual_help(text)
            self.quick_reference.update_commands(text)
            
        elif self.is_command_mode:
            self.command_preview.setText(f"Command: {text}")
            self.command_handler.process_command(text)
            
            # Update suggestions and contextual help
            self.command_handler.get_suggestions(text)
            help_info = self.contextual_help.get_contextual_help(text)
            self.quick_reference.update_commands(text)
            
            # Show quick tip
            tip = self.contextual_help.get_quick_tip(text)
            if tip:
                self.status_label.setText(f"💡 {tip}")
                QTimer.singleShot(5000, lambda: self.status_label.setText("🎤 Ready"))
        
    def handle_command_executed(self, message):
        self.status_label.setText(f"✅ {message}")
        QTimer.singleShot(3000, lambda: self.status_label.setText("🎤 Ready"))
        
    def handle_error(self, error_message):
        self.status_label.setText(f"⚠️ Error: {error_message}")
        QTimer.singleShot(3000, lambda: self.status_label.setText("🎤 Ready"))
        
    def update_audio_level(self, level):
        # Convert audio level to percentage (0-100)
        percentage = min(100, int(level * 100))
        self.audio_level.setValue(percentage)
        
    def handle_state_change(self, state):
        if state == "listening":
            self.status_label.setText("🎤 Listening...")
        elif state == "stopped":
            self.status_label.setText("🎤 Ready")
        
    def update_button_states(self):
        # Update button states based on current mode
        self.type_button.setEnabled(not self.is_command_mode)
        self.command_button.setEnabled(not self.is_typing)
        self.quick_commands_button.setEnabled(True)
        
    def toggle_mode(self):
        if "Voice Typing" in self.mode_button.text():
            self.mode_button.setText("Mode: Command")
            self.content_stack.setCurrentWidget(self.command_widget)
        else:
            self.mode_button.setText("Mode: Voice Typing")
            self.content_stack.setCurrentWidget(self.typing_widget)
        
    def handle_suggestion_selected(self, command):
        """Handle when a suggestion is selected"""
        self.command_handler.process_command(command)
        
    def show_quick_commands(self):
        """Show the quick actions panel"""
        if not hasattr(self, 'quick_actions_panel'):
            self.quick_actions_panel = QuickActionsPanel(self)
            self.quick_actions_panel.action_triggered.connect(self.handle_quick_action)
        
        # Show panel at button location
        self.quick_actions_panel.show_at_button(self.quick_commands_button)
        
    def handle_quick_action(self, command):
        """Handle quick action selection"""
        if command == "start typing":
            if not self.is_typing:
                self.toggle_typing()
        elif command == "stop listening":
            if self.is_typing or self.is_command_mode:
                self.voice_manager.stop_listening()
                self.is_typing = False
                self.is_command_mode = False
                self.update_button_states()
        else:
            # Process other commands through command handler
            self.command_handler.process_command(command)