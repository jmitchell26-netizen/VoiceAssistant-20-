# Browser Power User Feature - Testing Guide

## Overview
This guide will help you test the new browser control features that allow voice commands for Safari and Chrome.

## Prerequisites
1. Python 3.8+ installed
2. All dependencies installed (`pip3 install -r requirements.txt`)
3. macOS Accessibility permissions granted (see below)

## Granting Permissions

### First Run
When you first run the app with these new features, you may see a permission request. Follow these steps:

1. **System Settings > Privacy & Security > Accessibility**
2. Click the lock icon to make changes
3. Add Python (or Terminal/iTerm if running from terminal) to the allowed list
4. Restart the application

If you don't grant permissions, you'll see a warning message in the console telling you what to do.

## Testing Checklist

### Phase 1: Window Detection (5 minutes)

1. **Start the Voice Assistant**
   ```bash
   cd "/Users/joeymitchell/Voice assistant"
   python3 src/main.py
   ```

2. **Test App Detection**
   - Open Safari
   - Look for the green banner at the top: "🌐 Browser Mode: Safari"
   - Switch to another app (like Finder)
   - The banner should disappear
   - Switch back to Safari
   - The banner should reappear

3. **Test Chrome Detection**
   - Open Google Chrome
   - Look for: "🌐 Browser Mode: Google Chrome"
   - Switch between Safari and Chrome
   - The banner should update with the correct browser name

**Expected Console Output:**
```
Starting active window detection...
Active app changed to: Safari
🌐 Browser mode activated: Safari
Context changed to: browser (Safari)
```

### Phase 2: Browser Commands (15 minutes)

#### Setup for Command Testing
1. Open Safari or Chrome
2. In the Voice Assistant, click "Command Mode" button
3. The Quick Reference panel should show browser commands

#### Tab Management Commands
Test each of these commands:

| Command | Expected Result |
|---------|----------------|
| "new tab" | Opens a new blank tab |
| "close tab" | Closes the current tab |
| "close all tabs" | Closes all tabs in window (BE CAREFUL!) |

#### Navigation Commands

1. **Test "go to" command:**
   - Say: "go to apple.com"
   - Browser should navigate to https://apple.com

2. **Test "search for" command:**
   - Say: "search for python tutorials"
   - Browser should open Google search results

3. **Test history navigation:**
   - Navigate to a few pages
   - Say: "go back"
   - Say: "go forward"
   - Say: "refresh"

#### Page Control Commands

1. **Test scrolling:**
   - Open a long webpage
   - Say: "scroll down"
   - Say: "scroll up"
   - Say: "scroll to top"
   - Say: "scroll to bottom"

2. **Test zoom:**
   - Say: "zoom in" (repeat a few times)
   - Say: "zoom out" (to return to normal)

3. **Test find:**
   - Say: "find hello on page"
   - Browser's find dialog should open with "hello" typed

4. **Test bookmark:**
   - Navigate to a page
   - Say: "bookmark this"
   - Browser's bookmark dialog should appear

### Phase 3: Context Switching (10 minutes)

1. **Browser to General Commands**
   - Start in Safari with Command Mode active
   - Quick Reference should show browser commands
   - Switch to Finder
   - Quick Reference should update to show general commands
   - Banner should disappear

2. **Typing Mode in Browser**
   - Open Safari
   - Switch to "Start Typing" mode
   - Type some text with voice
   - Browser mode banner should still be visible
   - Switch to Command Mode
   - Browser commands should be available

3. **Rapid Switching**
   - Quickly switch between Safari, Chrome, and other apps
   - Ensure the banner updates correctly each time
   - No crashes or errors

### Phase 4: Error Handling (5 minutes)

1. **Test invalid commands in browser:**
   - Say: "invalid command"
   - Should see: "Unknown command: invalid command (Try browser commands like 'close tab', 'go back', etc.)"

2. **Test browser commands outside browser:**
   - Switch to Finder
   - Try: "close tab"
   - Should see: "Unknown command: close tab" (without browser hint)

3. **Test with no browser open:**
   - Close all browsers
   - App should continue working normally
   - General commands should work

## Known Issues & Troubleshooting

### Permission Denied
**Symptom:** Commands don't work, console shows "not allowed" or "permission" errors
**Solution:** Grant Accessibility permissions (see above)

### Commands Not Recognized
**Symptom:** Voice recognition works but commands say "unknown"
**Solution:** 
- Check if banner shows "Browser Mode"
- Try Command Mode (not Typing Mode)
- Speak clearly: "close tab" (not "close the tab")

### Browser Detection Not Working
**Symptom:** Banner never appears when switching to browser
**Solution:**
- Check console for errors
- Ensure window_detector.start() was called
- Try restarting the app

### AppleScript Timeout
**Symptom:** Commands are slow or timeout
**Solution:**
- Close unnecessary browser tabs
- Restart the browser
- Check Activity Monitor for high CPU usage

## Success Criteria

✅ Banner appears/disappears when switching to/from browsers  
✅ All tab management commands work  
✅ Navigation commands work (go to, search, back, forward)  
✅ Page control commands work (scroll, zoom, find, bookmark)  
✅ Quick Reference updates based on context  
✅ Command suggestions show browser commands in browser context  
✅ No crashes when switching contexts  
✅ Graceful error messages for invalid commands  

## Testing Complete!

If all tests pass, the feature is working correctly. Report any issues with:
- What command you said
- What you expected to happen
- What actually happened
- Console error messages (if any)

## Next Steps

Once testing is complete:
1. Test with real workflows (browsing while dictating notes, etc.)
2. Identify any commands you wish were added
3. Report any bugs or unexpected behavior
4. Consider Phase 2 features (tab history, advanced bookmarks, etc.)

