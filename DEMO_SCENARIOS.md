# Demo Scenarios for Presentation

## 🎯 Primary Demo: "Research Workflow"
**Time: 90 seconds**  
**Difficulty: Easy**  
**Wow Factor: ⭐⭐⭐⭐⭐**

### Setup:
- Safari open to Google homepage
- Floating button visible (bottom-right)
- Volume at 70%
- Internet connected

### Step-by-Step Script:

| Step | Your Action | Say/Do | Expected Result | If It Fails |
|------|------------|---------|-----------------|-------------|
| 1 | Setup | "Let me show you my voice assistant in action." | --- | --- |
| 2 | Activate | Press **Ctrl+Space** | Floating button turns **GREEN** | Point it out verbally |
| 3 | Search | Say clearly: **"search for artificial intelligence"** | Google search executes | Say "Let me try that again" |
| 4 | Deactivate | Press **Ctrl+Space** | Button turns gray | --- |
| 5 | Wait | Let results load (2 seconds) | --- | --- |
| 6 | Activate | Press **Ctrl+Space** | Button turns **GREEN** | --- |
| 7 | New Tab | Say: **"new tab"** | New blank tab opens | Try "open new tab" |
| 8 | Navigate | Say: **"go to github dot com"** | GitHub homepage loads | Try again with pause: "go to... github.com" |
| 9 | Scroll | Say: **"scroll down"** | Page scrolls down | Say "scroll down" again |
| 10 | Close | Press **Ctrl+Space** | Button turns gray | --- |
| 11 | Finish | "And I never left Safari once!" | **Audience impressed** | Smile and proceed |

### Narration Script:
```
"I'm in Safari, doing research. Instead of clicking around, 
I press Ctrl+Space [PRESS IT] and the button turns green, 
indicating browser mode is active.

Now I can just say 'search for artificial intelligence' [SAY IT]
and it searches. Notice Safari never lost focus.

Let me open a new tab [Ctrl+Space] 'new tab' [SAY IT]

Now navigate: 'go to github.com' [SAY IT]

And scroll: 'scroll down' [SAY IT]

All without ever clicking back to the assistant. This is what 
makes it different from other voice assistants."
```

---

## 🎯 Backup Demo 1: "Tab Management"
**Time: 60 seconds**  
**Difficulty: Very Easy**  
**Wow Factor: ⭐⭐⭐**

### When to Use:
- Primary demo fails
- Running short on time
- Audience seems confused

### Script:
```
Setup: Safari with 2-3 tabs open

1. Press Ctrl+Space
2. Say "close tab"        → Tab closes
3. Say "new tab"          → New tab opens
4. Say "close tab"        → Tab closes
5. Press Ctrl+Space       → Stop

"These basic commands make browsing so much faster."
```

---

## 🎯 Backup Demo 2: "Show the Code"
**Time: 90 seconds**  
**Difficulty: N/A**  
**Wow Factor: ⭐⭐⭐⭐**

### When to Use:
- Live demo completely fails
- Voice recognition not working
- Internet down
- More technical audience

### Script:
```
"Let me show you how this works under the hood."

[Open: src/app/utils/active_window_detector.py]

"Every 500 milliseconds, the system checks which app is active.

[Show _check_browser_status method]

When it detects Safari or Chrome, it emits a Qt signal to 
activate browser mode. This is what makes the button turn green.

[Open: src/app/utils/command_handler.py]

The command handler receives voice text and routes it based 
on context. If browser mode is active, it sends commands to 
the browser router instead of general system commands.

[Open: src/app/utils/browser_commands.py]

And here's where the magic happens - we use AppleScript to 
actually control Safari. Python subprocess executes this 
AppleScript, which Safari understands natively.

This architecture is extensible - I could add more contexts 
like IDEs, file managers, or other apps using the same pattern."
```

---

## 🎯 Advanced Demo: "Full Workflow"
**Time: 2 minutes**  
**Difficulty: Hard**  
**Wow Factor: ⭐⭐⭐⭐⭐**

### Only Use If:
- You're confident
- Everything is working perfectly
- You want to show off
- Audience is engaged

### Script:
```
"Let me show you a realistic workflow."

[Safari on Google]

Ctrl+Space
"search for python decorators tutorial"
[Results load]

"scroll down"
"scroll down"

[Find interesting result]

"new tab"
"go to real python dot com"

[Page loads]

"bookmark this"
[Bookmark dialog appears - Press Escape]

"find example on page"
[Find dialog opens with "example" typed]

"scroll to bottom"

"new tab"
"search for decorator examples github"

[Multiple tabs now open]

"That's a full research session - zero clicking!"
```

---

## 🎯 "Wow" Moments to Highlight

### 1. **The Green Button**
**When**: First activation in browser
**Say**: "Notice the button turned green - that means browser mode detected Safari automatically"
**Why it's cool**: Shows context awareness

### 2. **No Window Switching**
**When**: After executing 3+ commands
**Say**: "I've executed multiple commands and Safari never lost focus - that's the key innovation"
**Why it's cool**: Solves the original problem

### 3. **URL Recognition**
**When**: Using "go to" command
**Say**: "It automatically adds https:// and handles domain names naturally"
**Why it's cool**: Shows intelligent parsing

### 4. **Multiple Browsers**
**When**: Explaining browser support
**Say**: "It works with Safari, Chrome, Firefox, Arc, Brave, and Edge - automatically detects which one you're using"
**Why it's cool**: Shows extensibility

---

## 🚨 Common Failure Modes & Recovery

### Problem: Voice not recognized
**Symptoms**: Nothing happens after speaking
**Recovery**:
1. Stay calm: "Let me try that again..."
2. Speak more slowly and clearly
3. If fails twice: "Voice recognition can be finicky - let me show you the video"
4. Switch to backup demo or code walkthrough

### Problem: Wrong command executed
**Symptoms**: Different action than intended
**Recovery**:
1. Laugh it off: "That's not quite what I said! Voice recognition is probabilistic..."
2. Try again once
3. If fails: "This is actually a good opportunity to show error handling..."

### Problem: Browser doesn't respond
**Symptoms**: Command acknowledged but nothing happens
**Recovery**:
1. Check if Safari is actually active
2. Try another simpler command (like "new tab")
3. If fails: "This shows why testing is important. Let me show you the backup..."

### Problem: Button stays gray in browser
**Symptoms**: No green button when in Safari
**Recovery**:
1. Click on Safari window to ensure it's active
2. Wait 1 second (polling delay)
3. If still gray: "The detector is polling - usually it's instant but let me continue with the technical explanation..."

### Problem: Accessibility permission error
**Symptoms**: Error message in console
**Recovery**:
1. Expected: "Actually, this is a good teaching moment about system permissions..."
2. Explain why accessibility is needed
3. Show the error handling code
4. Switch to video or code walkthrough

---

## 🎬 Video Recording Script

If you want to record a backup video (highly recommended):

### Recording Setup:
1. Clean desktop (close everything except Safari)
2. Set screen resolution to 1920x1080
3. Use QuickTime or OBS
4. Record system audio + your voice
5. Have script in front of you

### Recording Script (read naturally):
```
"This is a voice assistant with context-aware browser control.

I'm going to show you how it works.

[Open Safari to Google]

I press Ctrl+Space to activate voice listening.
Notice the green floating button - that means browser mode is active.

[Press Ctrl+Space]

Now I can say 'search for machine learning'

[Say it clearly]

The search executes, and Safari never lost focus.

Let me open a new tab.

[Press Ctrl+Space]

'new tab'

[Say it]

Now I'll navigate: 'go to github.com'

[Say it]

And scroll down: 'scroll down'

[Say it]

I can stop listening with Ctrl+Space.

[Press it]

The key innovation is that all of this happens without 
switching windows. The system automatically detects when 
I'm in a browser and enables browser-specific commands.

This solves the fundamental usability problem of voice 
control: maintaining context and focus."

[End recording]
```

### Post-Processing:
1. Trim any mistakes
2. Add subtitles (optional but nice)
3. Export as MP4 H.264
4. Test playback on presentation computer
5. Keep file under 50MB if possible

---

## ✅ Pre-Demo Testing Checklist

Run this 1 hour before presentation:

```bash
python3 demo_test_script.py
```

Manual checks:
- [ ] Floating button visible
- [ ] Button turns green in Safari
- [ ] Button turns gray outside Safari
- [ ] Ctrl+Space toggles on/off
- [ ] "new tab" works
- [ ] "close tab" works
- [ ] "go to github.com" works
- [ ] "search for test" works
- [ ] "scroll down" works
- [ ] Audio level indicator shows activity
- [ ] No Python errors in console

If ANY of these fail, debug NOW, not during presentation!

---

## 💡 Pro Tips

### Before Speaking:
1. **Take a breath**: Pause before each command
2. **Enunciate**: Speak clearly but naturally
3. **Slow down**: Give computer time to process
4. **Project**: Speak loud enough for microphone

### During Demo:
1. **Narrate**: Say what you're doing before you do it
2. **Show**: Point to the green button, the results, etc.
3. **Pause**: Let actions complete before next command
4. **Smile**: If something fails, stay positive

### After Demo:
1. **Summarize**: "That's voice-controlled browsing without window switching"
2. **Invite questions**: "I'd love to answer questions about how it works"
3. **Have backup ready**: If someone says "can you show that again?" have your answer ready

---

## 📊 Timing Guide

For 5-minute presentation:

| Section | Time | Critical? |
|---------|------|-----------|
| Intro + Problem | 30s | Yes |
| Solution Overview | 30s | Yes |
| **LIVE DEMO** | **90s** | **YES** |
| Technical Deep Dive | 90s | Yes |
| Challenges + Learning | 30s | No* |
| Future + Q&A | 60s | No* |

*Can cut these if running long

**The demo is the centerpiece** - don't rush it!

---

## 🎯 Success Indicators

You'll know your demo was successful if:
- ✅ At least 3 commands execute correctly
- ✅ Green button is visible and changes color
- ✅ Audience sees the "no window switching" benefit
- ✅ You stay calm if something fails
- ✅ You can pivot to backup seamlessly

**Remember**: A flawless demo is nice, but a good recovery from failure shows professionalism and deep understanding!

---

Good luck! You've got this! 🚀

