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
from ..utils.active_window_detector import ActiveWindowDetector
from ..utils.global_hotkey import GlobalHotkeyManager
from .command_suggestions import CommandSuggestions
from .quick_actions import QuickActionsPanel
from .quick_reference import QuickReferenceCard
from .animated_mic import AnimatedMicrophoneIcon

class AudioLevelIndicator(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setTextVisible(False)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self._current_state = 'ready'
        self._update_style()
    
    def set_state(self, state):
        """Update the color based on state (ready, listening, processing, error, speaking)"""
        self._current_state = state
        self._update_style()
    
    def _update_style(self):
        """Update stylesheet based on current state"""
        colors = {
            'ready': '#808080',      # Gray
            'listening': '#4CAF50',  # Green
            'processing': '#FFC107', # Yellow/Amber
            'error': '#F44336',      # Red
            'speaking': '#2196F3'    # Blue
        }
        color = colors.get(self._current_state, '#808080')
        
        self.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {color};
                border-radius: 5px;
                background: #2D2D2D;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)

class VoiceWidget(QWidget):
    def __init__(self, settings_manager=None):
        super().__init__()
        self.settings_manager = settings_manager
        self.voice_manager = VoiceRecognitionManager(settings_manager=self.settings_manager)
        self.typing_mode = VoiceTypingMode(self.voice_manager)
        self.command_handler = CommandHandler()
        self.contextual_help = ContextualHelp()
        self.window_detector = ActiveWindowDetector()
        self.hotkey_manager = GlobalHotkeyManager()
        self.init_ui()
        self.setup_connections()
        
        # Start window detection and hotkey listening
        self.window_detector.start()
        self.hotkey_manager.start()
        
    def closeEvent(self, event):
        """Handle cleanup when widget is closed"""
        self.voice_manager.cleanup()
        self.window_detector.cleanup()
        self.hotkey_manager.cleanup()
        super().closeEvent(event)
        
    def hideEvent(self, event):
        """Handle when widget is hidden - but keep listening in background!"""
        # Don't stop listening - we want background operation
        # The user can use Ctrl+Space or the floating button to control listening
        super().hideEvent(event)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Context indicator (shows browser mode, etc.)
        self.context_label = QLabel("")
        self.context_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.context_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                background: rgba(76, 175, 80, 0.1);
                border-radius: 5px;
                min-height: 20px;
            }
        """)
        self.context_label.hide()  # Hidden by default
        layout.addWidget(self.context_label)
        
        # Animated microphone icon with status
        self.animated_mic = AnimatedMicrophoneIcon()
        self.animated_mic.setFixedSize(150, 150)
        mic_container = QHBoxLayout()
        mic_container.addStretch()
        mic_container.addWidget(self.animated_mic)
        mic_container.addStretch()
        layout.addLayout(mic_container)
        
        # Partial/interim text display (real-time transcription preview)
        self.partial_text_label = QLabel("")
        self.partial_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.partial_text_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-style: italic;
                font-size: 11px;
                min-height: 20px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.partial_text_label)
        
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
        self.voice_manager.partial_text_received.connect(self.handle_partial_text)
        self.voice_manager.error_occurred.connect(self.handle_error)
        self.voice_manager.audio_level.connect(self.update_audio_level)
        self.voice_manager.state_changed.connect(self.handle_state_change)
        
        # Connect animated microphone
        self.voice_manager.audio_level.connect(self.animated_mic.set_audio_level)
        self.voice_manager.state_changed.connect(self.animated_mic.set_state)
        
        # Connect window detector signals
        self.window_detector.browser_active.connect(self.handle_browser_active)
        self.window_detector.browser_inactive.connect(self.handle_browser_inactive)
        self.window_detector.active_app_changed.connect(self.handle_app_changed)
        
        # Connect global hotkey signals
        self.hotkey_manager.toggle_listening.connect(self.handle_global_toggle)
        
        # Connect command handler signals
        self.command_handler.command_executed.connect(self.handle_command_executed)
        self.command_handler.command_failed.connect(self.handle_error)
        self.command_handler.suggestion_updated.connect(self.suggestions.update_suggestions)
        self.command_handler.context_changed.connect(self.handle_context_changed)
        
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
            self.content_stack.setCurrentWidget(self.typing_widget)
        else:
            self.voice_manager.stop_listening()
            self.type_button.setText("Start Typing")
        self.update_button_states()
        
    def toggle_command_mode(self):
        self.is_command_mode = not self.is_command_mode
        self.is_typing = False
        if self.is_command_mode:
            self.voice_manager.start_listening()
            self.command_button.setText("Stop Commands")
            self.content_stack.setCurrentWidget(self.command_widget)
        else:
            self.voice_manager.stop_listening()
            self.command_button.setText("Command Mode")
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
                self.partial_text_label.setText(f"💡 {tip}")
                QTimer.singleShot(5000, lambda: self._reset_partial_text_style())
        
    def handle_partial_text(self, text):
        """Update the partial text display with interim transcription"""
        self.partial_text_label.setText(text)
    
    def handle_command_executed(self, message):
        # Show success message briefly
        self.partial_text_label.setText(f"✅ {message}")
        self.partial_text_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-style: normal;
                font-size: 11px;
                font-weight: bold;
                min-height: 20px;
                padding: 5px;
            }
        """)
        QTimer.singleShot(3000, lambda: self._reset_partial_text_style())
        
    def handle_error(self, error_message):
        # Show error message briefly
        self.partial_text_label.setText(f"⚠️ {error_message}")
        self.partial_text_label.setStyleSheet("""
            QLabel {
                color: #F44336;
                font-style: normal;
                font-size: 11px;
                font-weight: bold;
                min-height: 20px;
                padding: 5px;
            }
        """)
        QTimer.singleShot(3000, lambda: self._reset_partial_text_style())
    
    def _reset_partial_text_style(self):
        """Reset partial text label to default style"""
        self.partial_text_label.setText("")
        self.partial_text_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-style: italic;
                font-size: 11px;
                min-height: 20px;
                padding: 5px;
            }
        """)
        
    def update_audio_level(self, level):
        # Convert audio level to percentage (0-100)
        percentage = min(100, int(level * 100))
        self.audio_level.setValue(percentage)
        
    def handle_state_change(self, state):
        """Handle state changes and update UI colors accordingly"""
        # Update audio level indicator color
        self.audio_level.set_state(state)
        
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
    
    def handle_browser_active(self, browser_name):
        """Handle when a browser becomes active"""
        # Notify command handler
        self.command_handler.set_browser_active(browser_name)
        
        # Show browser mode indicator
        self.context_label.setText(f"🌐 Browser Mode: {browser_name}")
        self.context_label.show()
        
        # Update suggestions to show browser commands
        if self.is_command_mode:
            self.command_handler.get_suggestions("")
    
    def handle_browser_inactive(self):
        """Handle when switching away from a browser"""
        # Notify command handler
        self.command_handler.set_browser_inactive()
        
        # Hide browser mode indicator
        self.context_label.hide()
        
        # Update suggestions back to general commands
        if self.is_command_mode:
            self.command_handler.get_suggestions("")
    
    def handle_app_changed(self, app_name):
        """Handle when the active app changes"""
        print(f"Active app: {app_name}")
    
    def handle_context_changed(self, context):
        """Handle when the command context changes"""
        print(f"Command context: {context}")
        
        # Update quick reference to show relevant commands
        if context == 'browser':
            self.quick_reference.show_browser_commands()
        else:
            self.quick_reference.show_general_commands()
    
    def handle_global_toggle(self):
        """Handle Ctrl+Space hotkey press to toggle listening"""
        print("🎤 Global hotkey triggered - toggling voice listening")
        
        # Toggle command mode if not already in a mode
        if not self.is_typing and not self.is_command_mode:
            # Start command mode
            self.toggle_command_mode()
        elif self.is_command_mode:
            # Stop command mode
            self.toggle_command_mode()
        elif self.is_typing:
            # Stop typing mode
            self.toggle_typing()
        
        # Show a brief notification
        self.partial_text_label.setText(f"🎤 {'Listening' if self.is_command_mode or self.is_typing else 'Stopped'} (Ctrl+Space)")
        QTimer.singleShot(2000, lambda: self._reset_partial_text_style())