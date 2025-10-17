# Voice Assistant

A modern, user-friendly voice assistant with voice typing and system control capabilities. Built with Python and PyQt6, featuring a clean interface and extensive voice command support.

## Features

### 🎤 Voice Typing
- Real-time speech-to-text conversion
- Natural punctuation commands ("period", "comma", etc.)
- Text formatting commands
- Live preview of transcribed text

### 🎯 Voice Commands
- System control (volume, brightness)
- Application management (open, close, switch)
- Web search capabilities
- Custom commands support

### 💫 Modern UI
- Clean, minimalist interface
- Floating microphone button
- Dark/Light theme support
- Quick action panel
- Navigation controls (back/home)

### 🔍 Help & Documentation
- Interactive help center
- Command suggestions
- Quick reference cards
- Contextual help system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jmitchell26-netizen/VoiceAssistant-20-.git
cd VoiceAssistant-20-
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Run the application:
```bash
python3 src/main.py
```

## Usage

### Voice Typing
1. Click "Start Typing" or use the floating microphone button
2. Speak naturally
3. Use commands like:
   - "period" for .
   - "new line" for line break
   - "delete that" to remove last word

### Voice Commands
- "open [app]" - Launch applications
- "volume [0-100]" - Control system volume
- "search for [query]" - Web search
- "help" - Show available commands

### Navigation
- Use the back button (←) to return to previous screens
- Home button (🏠) returns to main interface
- Quick actions panel (⚡) for common commands

## Keyboard Shortcuts
- Start/Stop Listening: Ctrl+Space
- Show/Hide Window: Ctrl+Alt+V
- Quick Commands: Ctrl+Q
- Switch Mode: Ctrl+M

## System Requirements
- Python 3.8 or higher
- macOS 10.14 or higher
- Microphone access
- Internet connection (for web features)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with PyQt6 for the modern UI
- Uses SpeechRecognition for voice processing
- Integrates with system services for enhanced functionality
