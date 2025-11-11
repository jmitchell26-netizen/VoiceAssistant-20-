# Voice Assistant

A modern, intelligent voice assistant with **context-aware browser control**, voice typing, and system automation. Built with Python and PyQt6, featuring seamless background operation and global hotkey support.

## 🎉 What Makes This Special?

**Control your browser with voice - without ever leaving the browser window!**

Press **Ctrl+Space** from Safari or Chrome, say "new tab", and watch it happen. No window switching, no clicking around. Just pure voice control.

## ✨ Key Features

### 🌐 **Context-Aware Browser Control** (NEW!)
- **Automatic detection** of Safari, Chrome, Firefox, Arc, Brave, and Edge
- **Browser-specific commands** - "new tab", "close tab", "go to [url]"
- **Smart navigation** - "go back", "search for [query]", "refresh"
- **Page control** - "scroll down", "zoom in", "find [text] on page"
- **Tab management** - "close all tabs", "bookmark this"
- **Works in background** - control browser without switching windows!

### ⚡ **Global Hotkey** (NEW!)
- **Ctrl+Space** works from ANY application
- Toggle voice listening on/off without switching windows
- Stay in Safari/Chrome while giving voice commands
- Browser stays focused the entire time

### 🎤 **Enhanced Floating Button** (NEW!)
- **Color-coded status**:
  - 🔘 Gray = Not listening
  - 🔵 Blue = Listening (general mode)
  - 🟢 Green = Listening + Browser mode active!
- Click to toggle listening
- Drag to reposition anywhere on screen
- Always on top of all windows
- Double-click to show/hide main window

### 📝 Voice Typing
- Real-time speech-to-text conversion
- Natural punctuation commands ("period", "comma", etc.)
- Text formatting commands
- Live preview of transcribed text

### 🖥️ Smart System Control (NEW!)
- **Intelligent app launching** - Say "open vs code" or "open chrome"
- **50+ built-in app aliases** - Works with common app nicknames
- **Fuzzy matching** - Finds apps even if you don't say exact name
- **Smart suggestions** - Helpful hints if app not found
- Application management (open, close, switch)
- Window control (minimize, maximize)
- Web search capabilities
- Custom commands support

### 💫 Modern UI
- Clean, minimalist interface
- Dynamic command suggestions based on context
- Dark/Light theme support
- Quick action panel
- Interactive help center

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/jmitchell26-netizen/VoiceAssistant-20-.git
cd VoiceAssistant-20-
pip3 install -r requirements.txt
```

### 2. Grant Permissions (macOS)

The voice assistant needs **Accessibility permission** to:
- Detect active applications
- Control browsers with voice
- Use global hotkeys (Ctrl+Space)

**How to grant:**
1. Go to: **System Settings > Privacy & Security > Accessibility**
2. Click the 🔒 lock icon to unlock
3. Click **+** and add **Python** (or your Terminal app)
4. Restart the voice assistant

### 3. Run

```bash
python3 src/main.py
```

### 4. Try It Out!

1. **Open Safari or Chrome**
2. **Press Ctrl+Space** (while in the browser!)
3. Look for the **green floating button** (bottom-right)
4. **Say**: "new tab"
5. **Press Ctrl+Space** again to stop
6. **Success!** 🎉

**See [START_HERE.md](START_HERE.md) for detailed getting started guide.**

## 💡 Usage

### Three Ways to Control

1. **Global Hotkey** (⚡ Fastest!)
   - Press **Ctrl+Space** from any app
   - Say your command
   - Press **Ctrl+Space** again to stop
   - No window switching required!

2. **Floating Button** (👁️ Visual)
   - Click the circular microphone button
   - Watch the color for status
   - Drag to reposition
   - Double-click to show main window

3. **Main Window** (📋 Traditional)
   - Click "Command Mode" or "Start Typing"
   - Use buttons in the interface
   - View command suggestions and help

### Browser Commands (When Green Button Shows)

**Tab Management:**
```
"new tab"           → Opens new tab
"close tab"         → Closes current tab
"close all tabs"    → Closes all tabs
```

**Navigation:**
```
"go to github.com"            → Navigate to URL
"search for python tutorials" → Google search
"go back" / "go forward"      → Navigate history
"refresh"                     → Reload page
```

**Page Control:**
```
"scroll down" / "scroll up"      → Scroll page
"scroll to top" / "to bottom"    → Jump to top/bottom
"zoom in" / "zoom out"           → Adjust zoom
"find hello on page"             → Search for text
"bookmark this"                  → Bookmark page
```

### General Commands (Always Available)

**Smart App Launching:**
```
"open chrome"              → Opens Google Chrome
"open vs code"             → Opens Visual Studio Code
"open spotify"             → Opens Spotify
"open terminal"            → Opens Terminal
"open photoshop"           → Opens Adobe Photoshop
"close slack"              → Closes Slack
"switch to chrome"         → Switches to Chrome
```

**Works with 50+ app aliases!** Say common names like:
- "chrome", "firefox", "safari", "brave", "edge"
- "vs code", "pycharm", "xcode", "sublime"
- "slack", "discord", "zoom", "teams"
- "word", "excel", "powerpoint", "keynote"
- "spotify", "music", "vlc"
- And many more! See [APP_LAUNCHER_GUIDE.md](APP_LAUNCHER_GUIDE.md)

**Other System Commands:**
```
"minimize window"          → Minimize window
"maximize window"          → Maximize window
```

### Voice Typing Commands

```
"period" / "comma"         → Add punctuation
"new line"                 → Line break
"new paragraph"            → Paragraph break
"capitalize that"          → Capitalize last phrase
"all caps" / "lowercase"   → Change case
```

## ⌨️ Keyboard Shortcuts

- **Ctrl+Space** - Toggle voice listening (works from ANY app!)
- Double-click floating button - Show/hide main window
- Drag floating button - Reposition
- Click floating button - Toggle listening

## 📋 System Requirements

- **Python 3.8 or higher**
- **macOS 10.14 or higher** (macOS Monterey+ recommended)
- **Microphone access**
- **Accessibility permissions** (for browser control and hotkeys)
- Internet connection (for voice recognition)

### Dependencies
- PyQt6 - Modern UI framework
- SpeechRecognition - Voice recognition
- pyttsx3 - Text-to-speech
- pynput - Global hotkey support
- pyaudio - Audio processing
- See `requirements.txt` for complete list

## 📚 Documentation

### Getting Started
- **[START_HERE.md](START_HERE.md)** - Quick start guide
- **[GLOBAL_HOTKEY_GUIDE.md](GLOBAL_HOTKEY_GUIDE.md)** - Complete hotkey usage guide
- **[APP_LAUNCHER_GUIDE.md](APP_LAUNCHER_GUIDE.md)** - Smart app launching guide
- **[BROWSER_FEATURE_TEST.md](BROWSER_FEATURE_TEST.md)** - Testing checklist

### Technical Documentation
- **[BROWSER_FEATURE_IMPLEMENTATION.md](BROWSER_FEATURE_IMPLEMENTATION.md)** - Technical details
- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** - System architecture and design
- **[USABILITY_IMPROVEMENTS_SUMMARY.md](USABILITY_IMPROVEMENTS_SUMMARY.md)** - Feature summary

### Presentation & Demo Materials
- **[SHOWCASE_PREPARATION_SUMMARY.md](SHOWCASE_PREPARATION_SUMMARY.md)** - Complete 1.5 week presentation prep plan
- **[PRESENTATION_OUTLINE.md](PRESENTATION_OUTLINE.md)** - 5-minute presentation structure with speaking notes
- **[DEMO_SCENARIOS.md](DEMO_SCENARIOS.md)** - Multiple demo scripts with timing and recovery plans
- **[PRESENTATION_QUICK_REFERENCE.md](PRESENTATION_QUICK_REFERENCE.md)** - One-page cheat sheet for presentation day
- **[demo_test_script.py](demo_test_script.py)** - Pre-flight testing tool for demos

## 🐛 Troubleshooting

### Commands show as "unrecognized"
- Check if the **floating button is green** (browser mode active)
- Make sure Safari/Chrome is the **frontmost window**
- Press **Ctrl+Space** to ensure listening is active

### Ctrl+Space doesn't work
- Grant **Accessibility permissions** (see installation step 2)
- Check console for error messages
- Ensure **pynput** is installed

### Browser mode doesn't activate
- Click on the **browser window** to make it frontmost
- Look for the green **"🌐 Browser Mode"** banner
- Check Accessibility permissions

### Floating button stays gray
- Click it or press **Ctrl+Space** to activate
- Gray means not listening (this is normal when idle)

## 🎯 Example Workflows

### Research Workflow
```
(In Safari)
Ctrl+Space                       → Start listening
"search for machine learning"    → Opens search
Ctrl+Space                       → Stop listening

(Review results)
Ctrl+Space                       → Start listening
"new tab"                        → Opens tab
"go to github.com"              → Navigates
Ctrl+Space                       → Stop listening
```

### Tab Management
```
(In Chrome with many tabs)
Ctrl+Space                       → Start listening
"close tab"                      → Closes current
"close tab"                      → Closes another
"new tab"                        → Opens fresh tab
Ctrl+Space                       → Stop listening
```

### Writing & Research
```
(In Safari reading article)
Ctrl+Space                       → Start listening
"scroll to bottom"               → Scrolls down
"find conclusion on page"        → Finds text
"bookmark this"                  → Saves page
Ctrl+Space                       → Stop listening
```

## 🚀 What's New in Latest Version

### v2.0 - Context-Aware Intelligence
- ✅ **Browser Power User** - Context-aware browser control
- ✅ **Global Hotkey** - Ctrl+Space works from any app
- ✅ **Enhanced Floating Button** - Color-coded status
- ✅ **Background Operation** - Works while window is hidden
- ✅ **Smart Detection** - Auto-detects browsers
- ✅ **15+ Browser Commands** - Full browser automation
- ✅ **Zero Window Switching** - Seamless workflow

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for Future Enhancements
- Windows/Linux support
- Customizable hotkeys
- Additional context modes (IDE, file manager, etc.)
- Voice training for better accuracy
- Command history and replay
- Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with **PyQt6** for the modern UI
- **SpeechRecognition** for voice processing
- **pynput** for global hotkey support
- **AppleScript** for browser automation on macOS
- Integrates with macOS system services

## 📧 Support

Having issues? Check these resources:
1. [START_HERE.md](START_HERE.md) - Quick start guide
2. [GLOBAL_HOTKEY_GUIDE.md](GLOBAL_HOTKEY_GUIDE.md) - Detailed usage
3. [Troubleshooting section](#-troubleshooting) above
4. Open an issue on GitHub

---

**Made with ❤️ for seamless voice control**