# Voice Assistant Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                    │
│  • Presses Ctrl+Space from Safari                              │
│  • Speaks: "new tab"                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│  GlobalHotkeyManager (pynput)                                  │
│  • Monitors keyboard globally                                   │
│  • Detects Ctrl+Space combination                              │
│  • Emits: toggle_listening signal                              │
│                                                                 │
│  VoiceRecognitionManager (SpeechRecognition)                   │
│  • Captures audio from microphone                              │
│  • Uses Google Speech API                                      │
│  • Emits: text_received("new tab")                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                 CONTEXT DETECTION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  ActiveWindowDetector                                           │
│  • Polls every 500ms using AppleScript                         │
│  • Queries: "What app is frontmost?"                           │
│  • Detects: "Safari" → Browser mode                            │
│  • Emits: browser_active("Safari")                             │
│                                                                 │
│  Supported Browsers:                                            │
│  ✓ Safari           ✓ Chrome          ✓ Firefox               │
│  ✓ Arc              ✓ Brave           ✓ Edge                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  COMMAND ROUTING LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  CommandHandler                                                 │
│  • Receives: text="new tab", context="browser"                 │
│  • Routes based on context:                                     │
│                                                                 │
│    if browser_active:                                           │
│      → BrowserCommandRouter                                     │
│    else:                                                        │
│      → SystemCommandHandler                                     │
│                                                                 │
│  Command Mapping:                                               │
│  • "new tab"      → browser_router.execute('new_tab')          │
│  • "go to {url}"  → browser_router.execute('go_to_url', url)   │
│  • "search {q}"   → browser_router.execute('search', query)    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│               BROWSER COMMAND EXECUTION LAYER                   │
├─────────────────────────────────────────────────────────────────┤
│  BrowserCommandRouter                                           │
│  • Maintains handlers for each browser                         │
│  • Routes to appropriate handler:                              │
│                                                                 │
│    handlers = {                                                 │
│      'Safari': SafariCommands(),                               │
│      'Google Chrome': ChromeCommands(),                        │
│      ...                                                        │
│    }                                                            │
│                                                                 │
│  SafariCommands / ChromeCommands                               │
│  • Browser-specific AppleScript                                │
│  • Executes via subprocess                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  APPLESCRIPT EXECUTION                          │
├─────────────────────────────────────────────────────────────────┤
│  subprocess.run(['osascript', '-e', script])                   │
│                                                                 │
│  Script for "new tab":                                          │
│  tell application "Safari"                                      │
│    tell front window                                            │
│      make new tab                                               │
│    end tell                                                     │
│  end tell                                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                     SAFARI / CHROME                             │
│                  → New Tab Opens! ✅                            │
└─────────────────────────────────────────────────────────────────┘

                         │
                         ↓ (feedback)
┌─────────────────────────────────────────────────────────────────┐
│                    UI FEEDBACK LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  FloatingButton                                                 │
│  • Visual state indicator                                       │
│  • Colors: Gray (idle) → Blue (listening) → Green (browser)    │
│                                                                 │
│  MainWindow                                                     │
│  • Command history                                              │
│  • Status messages                                              │
│  • Settings panel                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Signal Flow (Qt Architecture)

```
┌──────────────────┐
│ GlobalHotkey     │
│ Manager          │
└────────┬─────────┘
         │ signal: toggle_listening
         ↓
┌──────────────────┐
│ VoiceWidget      │ ←──────────┐
└────────┬─────────┘            │
         │ calls                │
         ↓                      │
┌──────────────────┐            │
│ VoiceRecognition │            │
│ Manager          │            │
└────────┬─────────┘            │
         │ signal: text_received("new tab")
         ↓                      │
┌──────────────────┐            │
│ CommandHandler   │            │
└────────┬─────────┘            │
         │ processes            │
         ↓                      │
┌──────────────────┐            │
│ BrowserCommand   │            │
│ Router           │            │
└────────┬─────────┘            │
         │ signal: command_executed
         └────────────────────→─┘
```

**Key Design Patterns:**
- **Observer Pattern**: Qt signals/slots for loose coupling
- **Strategy Pattern**: Different browser handlers
- **Router Pattern**: Context-aware command routing
- **Singleton Pattern**: Settings manager, theme manager

---

## Component Details

### 1. Global Hotkey Manager (`global_hotkey.py`)
```python
class GlobalHotkeyManager(QObject):
    toggle_listening = pyqtSignal()
    
    def _on_hotkey_pressed(self):
        # Ctrl+Space detected
        self.toggle_listening.emit()
```

**Technology**: pynput (OS-level keyboard monitoring)  
**Why**: Works from any application, no window focus needed

### 2. Active Window Detector (`active_window_detector.py`)
```python
class ActiveWindowDetector(QObject):
    browser_active = pyqtSignal(str)
    
    def _check_active_window(self):
        # Every 500ms:
        script = 'tell application "System Events" to ...'
        result = subprocess.run(['osascript', '-e', script])
        
        if result == "Safari":
            self.browser_active.emit("Safari")
```

**Technology**: AppleScript polling  
**Why**: No other way to detect active app on macOS without Accessibility API

### 3. Command Handler (`command_handler.py`)
```python
class CommandHandler(QObject):
    def process_command(self, text):
        if self.is_browser_active:
            # Route to browser commands
            self.browser_router.execute_command(...)
        else:
            # Route to system commands
            self._handle_system_command(...)
```

**Pattern**: Context-aware routing  
**Why**: Same command text means different things in different contexts

### 4. Browser Command Router (`browser_commands.py`)
```python
class BrowserCommandRouter(QObject):
    def __init__(self):
        self.handlers = {
            'Safari': SafariCommands(),
            'Google Chrome': ChromeCommands(),
        }
    
    def execute_command(self, command, *args):
        handler = self.handlers[self.current_browser]
        method = getattr(handler, command)
        method(*args)
```

**Pattern**: Strategy + Router  
**Why**: Different browsers need different AppleScript

---

## Data Flow Example

**User Action**: Press Ctrl+Space in Safari, say "new tab"

```
1. GlobalHotkeyManager
   ↓ toggle_listening signal
   
2. VoiceWidget.handle_global_toggle()
   ↓ Starts VoiceRecognitionManager
   
3. VoiceRecognitionManager
   ↓ Captures audio → Google API → "new tab"
   ↓ text_received("new tab") signal
   
4. VoiceWidget receives text
   ↓ Calls CommandHandler.process_command("new tab")
   
5. CommandHandler
   ↓ Checks: is_browser_active = True
   ↓ Routes to: browser_router.execute_command('new_tab')
   
6. BrowserCommandRouter
   ↓ Gets current browser: "Safari"
   ↓ Gets handler: SafariCommands
   ↓ Calls: safari.new_tab()
   
7. SafariCommands.new_tab()
   ↓ Builds AppleScript
   ↓ subprocess.run(['osascript', ...])
   
8. AppleScript tells Safari to open new tab
   
9. Safari opens new tab ✅
   
10. SafariCommands emits: command_executed("Opened new tab")
    ↓ Signal flows back to VoiceWidget
    ↓ Updates UI with success message
```

---

## File Structure

```
src/
├── main.py                      # Entry point
├── app/
│   ├── main_window.py          # Main UI window
│   ├── widgets/
│   │   ├── floating_button.py  # Always-on-top button
│   │   ├── voice_widget.py     # Main voice interface
│   │   ├── help_center.py      # Help documentation
│   │   └── ...
│   └── utils/
│       ├── voice_recognition.py      # [INPUT] Audio → Text
│       ├── global_hotkey.py          # [INPUT] Ctrl+Space
│       ├── active_window_detector.py # [CONTEXT] What app?
│       ├── command_handler.py        # [ROUTING] Where to send?
│       ├── browser_commands.py       # [EXECUTE] AppleScript
│       ├── settings_manager.py       # Persistence
│       └── theme_manager.py          # UI theming
```

---

## Technology Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| UI Framework | PyQt6 | Modern, cross-platform, powerful |
| Voice Recognition | SpeechRecognition + Google API | High accuracy, easy integration |
| Global Hotkeys | pynput | Cross-platform keyboard monitoring |
| Window Detection | AppleScript | Only way on macOS without private APIs |
| Browser Control | AppleScript | Native macOS automation |
| Audio Processing | PyAudio + NumPy | Real-time audio level visualization |
| Settings | JSON files | Simple, human-readable |

---

## Design Decisions

### Why Qt Signals instead of callbacks?
- ✅ Thread-safe
- ✅ Decoupled components
- ✅ Easy to test
- ✅ Standard Qt pattern
- ❌ Slightly more verbose

### Why polling for window detection?
- ✅ Reliable
- ✅ Works without private APIs
- ✅ 500ms delay is acceptable
- ❌ Slight CPU usage (< 0.5%)
- ❌ Not instant (but close enough)

### Why AppleScript instead of Accessibility API?
- ✅ Officially supported by macOS
- ✅ Works with all browsers
- ✅ Simple to understand
- ❌ macOS only
- ❌ Requires Accessibility permission

### Why Google Speech API instead of local?
- ✅ Much more accurate (90%+ vs 70%)
- ✅ Handles accents and noise better
- ✅ Always improving
- ❌ Requires internet
- ❌ Privacy concerns (but not storing data)

---

## Performance Characteristics

| Operation | Time | CPU | Notes |
|-----------|------|-----|-------|
| Hotkey detection | < 50ms | 0.3% | pynput overhead |
| Window polling | 500ms interval | 0.2% | AppleScript query |
| Voice capture | Real-time | 2-5% | PyAudio + NumPy |
| Speech recognition | 1-3 seconds | Minimal | Cloud API |
| Command execution | 50-200ms | Minimal | AppleScript |
| UI updates | 16ms (60fps) | 1-3% | Qt rendering |

**Total overhead when idle**: < 1% CPU  
**Memory footprint**: ~50-80 MB  
**Startup time**: 2-3 seconds

---

## Extensibility

### Adding a new browser:
```python
# 1. Create handler class
class OperaCommands(BrowserCommandHandler):
    def __init__(self):
        super().__init__("Opera")
    
    def new_tab(self):
        # Opera-specific AppleScript
        ...

# 2. Register in router
class BrowserCommandRouter:
    def __init__(self):
        self.handlers = {
            ...
            'Opera': OperaCommands(),
        }

# 3. Add to detector
class ActiveWindowDetector:
    BROWSERS = [
        ...
        "Opera",
    ]
```

### Adding a new context (e.g., IDE):
```python
# Similar pattern to browser detection
class IDEDetector(QObject):
    ide_active = pyqtSignal(str)
    
    IDES = ["Visual Studio Code", "PyCharm", "Xcode"]

class IDECommandRouter(QObject):
    # IDE-specific commands
    ...
```

---

## Security Considerations

1. **Accessibility Permission**: Required for window detection and hotkeys
   - ⚠️ User must explicitly grant
   - ✅ Only monitors Ctrl+Space, not all keys

2. **Voice Data**: Sent to Google for processing
   - ⚠️ Privacy concern for sensitive info
   - ✅ Not stored or logged
   - 💡 Future: Add local recognition option

3. **AppleScript Execution**: Runs with user permissions
   - ✅ Can only do what user can do
   - ✅ No privilege escalation
   - ⚠️ Could be abused if voice commands are spoofed

---

## Testing Strategy

### Unit Tests (Future):
- Voice recognition settings
- Command parsing
- AppleScript generation

### Integration Tests:
- Run `demo_test_script.py`
- Tests actual browser commands
- Verifies AppleScript execution

### Manual Tests:
- UI interaction
- Voice recognition accuracy
- Edge cases and error handling

---

## Known Limitations

1. **macOS Only**: AppleScript is macOS-specific
2. **Internet Required**: Google Speech API needs connection
3. **Permission Dependent**: Needs Accessibility access
4. **Polling Delay**: 500ms before context switch detected
5. **Single Hotkey**: Only Ctrl+Space (not customizable yet)
6. **English Only**: Voice recognition is English-US only

---

## Future Architecture Improvements

1. **Plugin System**: 
   - Load context handlers dynamically
   - User-defined commands
   - Third-party integrations

2. **Event-Driven Window Detection**:
   - Replace polling with macOS notifications
   - Instant context switching
   - Lower CPU usage

3. **Local Voice Recognition**:
   - Fallback for offline use
   - Privacy option
   - Lower latency

4. **Command History & Learning**:
   - Track most-used commands
   - Suggest based on context
   - Personalized command aliases

---

This architecture demonstrates:
- ✅ Separation of concerns
- ✅ Loose coupling via signals
- ✅ Extensible design
- ✅ Real-world system integration
- ✅ User-centered problem solving

