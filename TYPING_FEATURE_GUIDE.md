# Voice Typing into Google Docs - User Guide

## 🎉 New Feature: Actual Typing!

Your voice assistant can now **actually type text into Google Docs** using keyboard simulation!

---

## 🚀 How to Use

### Step 1: Start the App
```bash
python3 src/main.py
```

### Step 2: Open Google Docs
1. Open **Safari** or **Chrome**
2. Go to **docs.google.com**
3. Open or create a document
4. **Click in the document** to place your cursor where you want to type

**You'll see:**
- Blue indicator: `📝 Google Docs Mode: Chrome`
- Console: `📝 Google Docs mode activated in Chrome`

### Step 3: Activate Voice Listening
Press **Ctrl+Space**

**You'll see:**
- "Starting voice recognition..."
- "Listening started successfully"

### Step 4: Start Speaking!

**Just speak naturally:**
```
You say: "hello world comma this is a test period"
→ Types: "hello world, this is a test."
```

```
You say: "this is bullet point amazing"
→ Types: "this is • amazing"
```

```
You say: "number one first item"
→ Types: "1. first item"
```

---

## 📝 Dictation Commands

### Basic Punctuation
```
"period" → .
"comma" → ,
"question mark" → ?
"exclamation point" → !
"semicolon" → ;
"colon" → :
```

### Quotes & Brackets
```
"quote" → "
"apostrophe" → '
"open parenthesis" → (
"close parenthesis" → )
"open bracket" → [
"close bracket" → ]
```

### Special Characters
```
"hyphen" → -
"dash" → –
"em dash" → —
"underscore" → _
"ellipsis" → ...
```

### Line Breaks
```
"new line" → (line break)
"new paragraph" → (double line break)
```

### Bullets & Lists
```
"bullet" or "bullet point" → •
"star" → *
"dash bullet" → -
"number one" → 1.
"number two" → 2.
(continues to "number five")
```

---

## 🎨 Formatting Commands

While dictating, you can also use formatting commands:

### Text Formatting
```
"make bold" → Toggles bold
"make italic" → Toggles italic
"underline this" → Adds underline
```

### Font Size
```
"increase font size" → Makes text bigger
"decrease font size" → Makes text smaller
```

### Line Spacing
```
"single space" → Single spacing
"double space" → Double spacing
"1.5 spacing" → 1.5 spacing
```

### Lists
```
"add bullets" → Creates bullet list
"add numbering" → Creates numbered list
```

### Headings
```
"heading one" → Heading 1 style
"heading two" → Heading 2 style
"normal text" → Normal paragraph
```

---

## 💡 Tips for Best Results

### 1. **Speak Clearly**
- Use a normal speaking pace (not too fast)
- Pronounce punctuation explicitly
- Pause briefly between sentences

### 2. **Click in Google Docs First**
- Make sure your cursor is in the document
- The text field must be focused for typing to work

### 3. **Mix Speech and Commands**
```
You: "hello world period"
→ Types: "hello world."

You: "make bold"
→ Makes "hello world." bold

You: "new line this is great"
→ Types new line: "this is great"
```

### 4. **Use Stop/Start**
- Press **Ctrl+Space** to stop listening
- Press **Ctrl+Space** again to resume
- Prevents accidental typing from background noise

---

## ⚙️ How It Works

1. **Voice Recognition** → Google's Speech API converts speech to text
2. **Text Processing** → Replaces punctuation commands with actual punctuation
3. **Keyboard Simulation** → Uses `pynput` to simulate typing
4. **Appears in Google Docs** → Text appears as if you typed it!

---

## 🔍 Troubleshooting

### Problem: Nothing types into Google Docs
**Solutions:**
- ✅ Make sure you **clicked inside the Google Docs document**
- ✅ Check that Google Docs mode is active (blue indicator)
- ✅ Verify cursor is blinking in the document
- ✅ Try clicking in the doc again

### Problem: Text appears in wrong place
**Solution:**
- Click exactly where you want text to appear before speaking

### Problem: Punctuation not working
**Example:** Says "period" but types "period" instead of "."

**Solution:**
- Make sure to say punctuation as separate words
- Pause slightly before and after punctuation words

### Problem: Text types too fast/slow
**Solution:**
Currently set to optimal speed. Can be adjusted in the code if needed.

---

## 🎯 Example Workflow

### Writing a Document
```
1. Open Google Docs
2. Click in document
3. Press Ctrl+Space

4. Say: "heading one"
5. Say: "my document title"
6. Say: "new paragraph"
7. Say: "normal text"
8. Say: "this is the first paragraph comma 
        and it has multiple sentences period"

9. Say: "new line bullet point first item"
10. Say: "new line bullet point second item"

11. Press Ctrl+Space to stop
```

**Result:**
```
# My Document Title

This is the first paragraph, and it has multiple sentences.
• first item
• second item
```

---

## 🚀 What's Next?

### Current Features
✅ Types text directly into Google Docs
✅ Processes punctuation commands
✅ Handles bullets and lists
✅ Works with formatting commands
✅ Auto-detects Google Docs

### Future Enhancements
- 🔮 Auto-punctuation (AI-based)
- 🔮 Voice selection ("select last sentence")
- 🔮 Dictation mode toggle (no command words)
- 🔮 Custom dictation shortcuts

---

## 📋 Quick Reference Card

**Navigation:**
- `Ctrl+Space` → Toggle listening on/off

**Dictation:**
- Just speak naturally
- Say punctuation out loud
- Use "new line" for line breaks

**Formatting:**
- "make bold/italic" → Format text
- "heading one/two" → Apply headings
- "add bullets" → Create lists

**Best Practice:**
1. Click in Google Docs
2. Press Ctrl+Space
3. Speak your text with punctuation
4. Press Ctrl+Space to stop

---

**Happy Dictating!** 🎤✨

