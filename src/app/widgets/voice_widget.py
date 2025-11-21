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
from ..utils.keyboard_typing import KeyboardTyper
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
        self.typing_mode = VoiceTypingMode(self.voice_manager, settings_manager=self.settings_manager)
        self.command_handler = CommandHandler()
        self.contextual_help = ContextualHelp()
        self.window_detector = ActiveWindowDetector()
        self.hotkey_manager = GlobalHotkeyManager()
        self.keyboard_typer = KeyboardTyper()  # For actual typing into applications
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
        
        # Context indicator (shows browser mode, Google Docs mode, etc.)
        self.context_label = QLabel("")
        self.context_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.context_label.hide()  # Hidden by default
        layout.addWidget(self.context_label)
        
        # Store current context for dynamic styling
        self.current_context = 'general'
        
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
        self.window_detector.google_docs_active.connect(self.handle_google_docs_active)
        self.window_detector.google_docs_inactive.connect(self.handle_google_docs_inactive)
        self.window_detector.active_app_changed.connect(self.handle_app_changed)
        
        # Connect window detector to browser router for URL checking
        self.window_detector.set_browser_router(self.command_handler.browser_router)
        
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
        # Check if this looks like a command or typing
        is_likely_command = self._is_likely_command(text)
        
        # In Google Docs, default to typing mode unless explicitly a command
        if self.current_context == 'google_docs' and not is_likely_command:
            # Auto-typing mode in Google Docs
            processed_text = self.typing_mode.process_text(text)
            self.text_preview.setText(f"📝 Typing: {processed_text}")
            
            # Actually type the text into Google Docs
            try:
                self.keyboard_typer.type_text(processed_text)
                print(f"✓ Typed into Google Docs: {processed_text}")
            except Exception as e:
                print(f"✗ Typing failed: {e}")
                self.text_preview.setText(f"⚠️ Typing error: {processed_text}")
            
        elif self.is_typing:
            # Explicit typing mode
            processed_text = self.typing_mode.process_text(text)
            current_text = self.text_preview.toPlainText()
            if current_text:
                current_text += " "
            self.text_preview.setText(current_text + processed_text)
            
            # Update contextual help for typing mode
            help_info = self.contextual_help.get_contextual_help(text)
            self.quick_reference.update_commands(text)
            
        elif self.is_command_mode or is_likely_command:
            # Command mode - process as command
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
        else:
            # Default: try as command first
            self.command_preview.setText(f"Command: {text}")
            self.command_handler.process_command(text)
    
    def _is_likely_command(self, text):
        """Detect if text is likely a command vs regular speech"""
        text_lower = text.lower().strip()
        
        # Common command action verbs
        command_verbs = [
            'open', 'close', 'switch', 'go', 'search', 'find', 'new', 'refresh',
            'scroll', 'zoom', 'bookmark', 'make', 'add', 'remove', 'change',
            'increase', 'decrease', 'set', 'align', 'clear', 'apply', 'insert'
        ]
        
        # Check if starts with a command verb
        for verb in command_verbs:
            if text_lower.startswith(verb + ' ') or text_lower == verb:
                return True
        
        # Very short phrases are likely commands
        if len(text_lower.split()) <= 3 and any(verb in text_lower for verb in command_verbs):
            return True
        
        # If it's a complete sentence (has multiple words and doesn't start with command verb), likely typing
        if len(text_lower.split()) > 5:
            return False
        
        return False  # Default to not a command (will be treated as typing)
        
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
        
        # Show browser mode indicator (but only if not in Google Docs)
        if not self.command_handler.is_google_docs_active:
            self.current_context = 'browser'
            self._update_context_label(f"🌐 Browser Mode: {browser_name}")
        
        # Update suggestions to show browser commands
        if self.is_command_mode:
            self.command_handler.get_suggestions("")
    
    def handle_browser_inactive(self):
        """Handle when switching away from a browser"""
        # Notify command handler
        self.command_handler.set_browser_inactive()
        
        # Hide browser mode indicator
        self.current_context = 'general'
        self.context_label.hide()
        
        # Update suggestions back to general commands
        if self.is_command_mode:
            self.command_handler.get_suggestions("")
    
    def handle_google_docs_active(self, browser_name):
        """Handle when Google Docs becomes active"""
        # Notify command handler
        self.command_handler.set_google_docs_active(browser_name)
        
        # Show Google Docs mode indicator
        self.current_context = 'google_docs'
        self._update_context_label(f"📝 Google Docs Mode: {browser_name}")
        
        # Update suggestions to show Google Docs commands
        if self.is_command_mode:
            self.command_handler.get_suggestions("")
    
    def handle_google_docs_inactive(self):
        """Handle when switching away from Google Docs"""
        # Notify command handler
        self.command_handler.set_google_docs_inactive()
        
        # Update UI - might go back to browser mode or general
        if self.command_handler.is_browser_active:
            self.current_context = 'browser'
            browser_name = self.window_detector.get_active_browser()
            self._update_context_label(f"🌐 Browser Mode: {browser_name}")
        else:
            self.current_context = 'general'
            self.context_label.hide()
        
        # Update suggestions
        if self.is_command_mode:
            self.command_handler.get_suggestions("")
    
    def _update_context_label(self, text):
        """Update context label with appropriate styling"""
        self.context_label.setText(text)
        
        # Different colors for different contexts
        if self.current_context == 'google_docs':
            # Blue for Google Docs
            self.context_label.setStyleSheet("""
                QLabel {
                    color: #2196F3;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                    background: rgba(33, 150, 243, 0.1);
                    border-radius: 5px;
                    min-height: 20px;
                }
            """)
        elif self.current_context == 'browser':
            # Green for browser
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
        
        self.context_label.show()
    
    def handle_app_changed(self, app_name):
        """Handle when the active app changes"""
        print(f"Active app: {app_name}")
    
    def handle_context_changed(self, context):
        """Handle when the command context changes"""
        print(f"Command context: {context}")
        self.current_context = context
        # Update quick reference if visible
        if hasattr(self, 'quick_reference') and self.quick_reference and self.quick_reference.isVisible():
            self.quick_reference.update_for_context(context)
        
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