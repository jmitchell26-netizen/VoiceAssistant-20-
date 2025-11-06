# Global Hotkey Feature - Quick Guide

## 🎉 Problem Solved!

You no longer need to switch between Safari and the Voice Assistant to use voice commands!

## How It Works Now

### **Ctrl+Space = Toggle Voice Listening** (Works from ANY app!)

```
You're in Safari → Press Ctrl+Space → Voice starts listening
Say "new tab" → Tab opens in Safari
Press Ctrl+Space again → Voice stops listening
Safari never loses focus!
```

## Three Ways to Use Voice Commands

### 1. Global Hotkey (FASTEST! ⚡)
- **Stay in Safari** (or any app)
- Press **Ctrl+Space** to start listening
- Say your command: "new tab", "search for python", etc.
- Press **Ctrl+Space** again to stop
- **Safari stays active the whole time!**

### 2. Floating Button (VISUAL 👁️)
- Look for the **circular microphone button** (bottom-right corner)
- **Click it** to toggle listening on/off
- **Gray** = Not listening
- **Blue** = Listening (general commands)
- **Green** = Listening (browser mode active!)
- **Drag** to move it anywhere on screen
- **Double-click** to show main window

### 3. Main Window (TRADITIONAL 🖥️)
- Click "Command Mode" button in the app
- Works like before, but now you can minimize the window
- Voice keeps working in the background!

## Visual Indicators

### Floating Button Colors:
- 🔘 **Gray** = Not listening
- 🔵 **Blue** = Listening (general mode)
- 🟢 **Green** = Listening (browser mode - special browser commands available!)

### Icon Changes:
- 🎤 Microphone = Listening
- 🚫 Microphone with slash = Not listening

## Quick Start (30 seconds)

1. **Open Safari**
2. **Press Ctrl+Space** (from Safari, don't switch apps!)
3. **Look** for the green floating button (means browser mode is active)
4. **Say**: "new tab"
5. **Watch** the magic happen! 🎉
6. **Press Ctrl+Space** again to stop

## Example Workflow

```
Working in Safari, researching Python:

Ctrl+Space                    → Start listening
"search for python decorators" → Opens Google search
Ctrl+Space                    → Stop

(Reading results...)

Ctrl+Space                    → Start listening
"new tab"                     → Opens new tab  
"go to github.com"            → Navigates to GitHub
Ctrl+Space                    → Stop

(Browsing GitHub...)

Ctrl+Space                    → Start listening
"scroll to bottom"            → Scrolls down
"go back"                     → Goes back
Ctrl+Space                    → Stop
```

**Never switched to the Voice Assistant app once!** 🎊

## Requirements

### First Time Setup

1. **Install pynput** (new dependency):
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Grant Accessibility Permissions**:
   - System Settings > Privacy & Security > Accessibility
   - Add Python to allowed apps
   - Required for both hotkeys and browser detection

3. **That's it!** Ready to use.

## Tips for Best Experience

### 1. **Use Ctrl+Space Liberally**
- Press it whenever you want to give a command
- No need to keep it pressed - it's a toggle
- Quick tap: **Ctrl+Space** → speak → **Ctrl+Space**

### 2. **Watch the Floating Button**
- Glance at it to confirm listening state
- Green = browser commands available
- If gray, press Ctrl+Space to activate

### 3. **Position the Floating Button**
- Drag it where you can see it
- Bottom-right works well
- Keep it visible so you know when it's listening

### 4. **Minimize the Main Window**
- You don't need the window open!
- Everything works in the background
- Floating button is all you need

### 5. **Browser Commands Only Work in Browser**
- Make sure browser is the active window
- Look for green floating button
- If blue, browser mode isn't active

## Browser Commands Available

When the floating button is **GREEN** (browser mode):

```
Tab Management:
  "new tab", "close tab", "close all tabs"

Navigation:
  "go to [url]"
  "search for [query]"
  "go back", "go forward"
  "refresh"

Page Control:
  "scroll up/down/to top/to bottom"
  "zoom in/out"
  "find [text] on page"
  "bookmark this"
```

## Troubleshooting

### Ctrl+Space Does Nothing
→ Check Accessibility permissions
→ Make sure pynput is installed
→ Look for console errors

### Floating Button is Gray
→ Press Ctrl+Space or click the button to activate
→ Check if voice recognition is working

### Floating Button is Blue, Not Green
→ Make sure Safari/Chrome is the frontmost window
→ Click on your browser window first
→ Wait a moment for detection

### Commands Don't Work
→ Check if floating button is green (browser mode)
→ Make sure you're in the browser window
→ Press Ctrl+Space to ensure listening is active

## Comparison: Before vs After

### Before (Frustrating 😤):
```
1. In Safari
2. Click Voice Assistant window
3. Browser mode deactivates (Safari not frontmost!)
4. Say "new tab"
5. Get "unrecognized command" error
6. Realize the problem
7. Click back to Safari
8. Repeat...
```

### After (Seamless 😊):
```
1. In Safari
2. Press Ctrl+Space
3. Say "new tab"
4. Done! ✨
```

## Advanced Features

### Multiple Browsers
- Works with Safari, Chrome, Firefox, Arc, Brave, Edge
- Auto-detects which browser is active
- Commands work the same in all browsers

### Background Operation
- Minimize the main window
- Voice assistant keeps running
- Use Ctrl+Space anytime
- No performance impact

### Hotkey Anywhere
- Works system-wide
- Even in full-screen apps
- Even with main window closed
- Always ready!

## What's Next?

Now that voice control is seamless, try:
- **Research workflows**: Search, new tab, navigate, all by voice
- **Tab management**: Close tabs you're done with without touching mouse
- **Reading articles**: Scroll, find text, navigate - hands-free
- **Multi-tasking**: Control browser while hands are busy

---

## Summary

**The Big Win**: You can now control your browser with voice commands **without ever leaving the browser window**!

**How**: Press **Ctrl+Space**, speak your command, press **Ctrl+Space** again.

**Visual Feedback**: Watch the floating button (green = browser mode + listening).

**Result**: Way more usable and natural! 🎉

Enjoy your enhanced voice assistant!

