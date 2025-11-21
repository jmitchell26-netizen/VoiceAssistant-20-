# Troubleshooting: Voice Typing Not Working in Google Docs

## 🔍 Quick Diagnostic Checklist

### Problem: Nothing types into Google Docs when I speak

Run through these checks in order:

---

## 1️⃣ **Accessibility Permissions** (MOST COMMON ISSUE)

### What is this?
macOS requires explicit permission for apps to simulate keyboard input.

### How to fix:
```
1. Open System Settings
2. Go to: Privacy & Security → Accessibility
3. Look for "Python" or "Terminal" in the list
4. Make sure it's ENABLED (checkbox ticked)
5. If not there, click the + button and add it
6. **IMPORTANT**: Restart the voice assistant after granting permission!
```

### How to test:
```bash
# Run this diagnostic script:
cd "/Users/joeymitchell/Voice assistant"
python3 test_typing_diagnostics.py

# Follow the on-screen instructions
# It will test if keyboard typing works at all
```

**If typing works in the test but not in Google Docs, continue to step 2.**

---

## 2️⃣ **Google Docs Not Focused**

### What is this?
The cursor must be actively blinking inside Google Docs for typing to work.

### How to fix:
```
1. Open Google Docs in Safari or Chrome
2. CLICK INSIDE THE DOCUMENT
   → You should see a blinking cursor
3. Keep Google Docs in the foreground
4. Now try speaking (Ctrl+Space)
```

### Visual check:
- ✅ Cursor is blinking in the document
- ✅ Document is in edit mode (not comment mode)
- ✅ Google Docs tab is active (not background tab)

---

## 3️⃣ **Google Docs Mode Not Active**

### What is this?
The app needs to detect that you're in Google Docs.

### How to verify:
Look at the floating button window - you should see:
```
📝 Google Docs Mode: Chrome
```
or
```
📝 Google Docs Mode: Safari
```

### If you DON'T see this:
```
1. Make sure you're at a docs.google.com URL
2. Wait 2-3 seconds for detection
3. Click inside the document again
4. Check if the blue "Google Docs Mode" banner appears
```

### If still not detected:
```bash
# Check console output when you open Google Docs
# You should see:
📝 Google Docs mode activated in Chrome

# If you don't see this, the URL detection might not be working
```

---

## 4️⃣ **Voice Recognition Not Working**

### What is this?
The app might not be hearing you or processing speech correctly.

### How to test:
```
1. Press Ctrl+Space to start listening
2. Say something simple: "hello world"
3. Check the console/terminal output
```

### What you should see:
```
Starting voice recognition...
Listening started successfully
📝 Typing: hello world
✓ Typed into Google Docs: hello world
```

### If you see errors:
```
✗ Typing failed: [error message]
```
→ Copy the error message and check below

---

## 🐛 Common Errors & Solutions

### Error: "Operation not permitted"
**Cause**: No accessibility permissions  
**Fix**: Go to step 1 above and grant permissions

### Error: "No active application"
**Cause**: Google Docs window not focused  
**Fix**: Click inside Google Docs document

### Error: "KeyboardTyper object has no attribute..."
**Cause**: Code issue (shouldn't happen)  
**Fix**: Run `git pull` to get latest version

### No error, but nothing types
**Causes**:
1. Google Docs in read-only mode
2. Cursor in comment/suggestion mode
3. Google Docs page frozen/crashed

**Fix**:
- Refresh the Google Docs page (Cmd+R)
- Create a new document and test there
- Try a different browser (Chrome vs Safari)

---

## 🧪 Step-by-Step Diagnostic Process

### Test 1: Verify Keyboard Typing Works
```bash
python3 test_typing_diagnostics.py
```
- If this fails → Accessibility permissions issue
- If this works → Continue to Test 2

### Test 2: Verify Google Docs Detection
```bash
python3 src/main.py
```
1. Open Google Docs in browser
2. Look for blue "📝 Google Docs Mode" indicator
3. Check terminal for "📝 Google Docs mode activated"

- If not detected → URL detection issue
- If detected → Continue to Test 3

### Test 3: Verify Voice Recognition
1. With app running and Google Docs open
2. Press Ctrl+Space
3. Say: "test"
4. Check terminal output

**Expected output:**
```
Listening started successfully
📝 Typing: test
✓ Typed into Google Docs: test
```

**If you see this but text doesn't appear:**
- Click inside Google Docs (cursor must be blinking)
- Try typing manually first to confirm doc is editable

---

## 💡 Additional Tips

### Make Sure:
- ✅ Using **Safari** or **Chrome** (Firefox/Edge may have issues)
- ✅ On **docs.google.com** (not Microsoft Word or other editors)
- ✅ Document is **editable** (not view-only)
- ✅ **Clicked inside** the document body (not header/footer)
- ✅ **Not in comment mode** (blue comment box)

### Performance Tips:
- Close other heavy applications
- Use a simple document (not 100+ pages)
- Speak clearly and at normal pace
- Wait for "Listening started" before speaking

---

## 🔧 Advanced Debugging

### Check Console Output
When the app is running, watch the terminal for:

```
✓ Typed into Google Docs: [your text]
```

If you see this but text doesn't appear:
- The typing code is working
- The issue is with focus/permissions

If you DON'T see this:
- Voice recognition might not be triggering typing
- Check if you're in command mode vs typing mode

### Enable Debug Mode
Add this to see more details:

```python
# In src/app/widgets/voice_widget.py, find handle_text_received()
# Add print statements to trace execution
```

---

## 📞 Still Not Working?

If you've tried everything above, gather this info:

1. **macOS Version**: 
   ```bash
   sw_vers
   ```

2. **Accessibility Permissions Status**:
   - System Settings → Privacy & Security → Accessibility
   - Is Python/Terminal listed and enabled?

3. **Console Output**:
   - Copy the last 20 lines from terminal when you try to speak

4. **What You See**:
   - Does "📝 Google Docs Mode" appear?
   - Does text preview show in the app?
   - Any error messages?

5. **Diagnostic Test Result**:
   ```bash
   python3 test_typing_diagnostics.py
   ```
   - Did the test typing work?

---

## ✅ Success Checklist

Once typing works, you should see:

1. ✓ Accessibility permissions granted
2. ✓ "📝 Google Docs Mode: Chrome" indicator visible
3. ✓ Terminal shows: "📝 Google Docs mode activated"
4. ✓ Cursor blinking in Google Docs
5. ✓ Press Ctrl+Space → "Listening started"
6. ✓ Speak → Terminal shows "✓ Typed into Google Docs: ..."
7. ✓ Text appears in document!

**Once you see all these, you're good to go!** 🎉

