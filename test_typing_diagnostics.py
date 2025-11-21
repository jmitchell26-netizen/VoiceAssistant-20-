#!/usr/bin/env python3
"""
Diagnostic Script for Voice Typing Feature
Tests keyboard typing and helps identify issues
"""

import sys
import time
sys.path.insert(0, 'src')

print("=" * 60)
print("Voice Typing Diagnostics")
print("=" * 60)
print()

# Test 1: Import modules
print("1️⃣  Testing imports...")
try:
    from app.utils.keyboard_typing import KeyboardTyper
    print("   ✓ keyboard_typing module imports successfully")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Create typer instance
print()
print("2️⃣  Testing KeyboardTyper creation...")
try:
    typer = KeyboardTyper()
    print("   ✓ KeyboardTyper instance created")
except Exception as e:
    print(f"   ✗ Creation failed: {e}")
    sys.exit(1)

# Test 3: Interactive typing test
print()
print("3️⃣  Interactive Typing Test")
print("=" * 60)
print()
print("INSTRUCTIONS:")
print("1. Open any text application (TextEdit, Notes, Google Docs)")
print("2. Click inside a text field")
print("3. Come back to this terminal")
print()

input("Press ENTER when you're ready with a text field focused...")

print()
print("🎯 Test typing will start in 3 seconds...")
print("   Make sure your cursor is in the text field!")
time.sleep(1)
print("   3...")
time.sleep(1)
print("   2...")
time.sleep(1)
print("   1...")
time.sleep(1)

# Test 4: Type test text
print()
print("4️⃣  Attempting to type: 'Hello from voice assistant!'")
print()

try:
    test_text = "Hello from voice assistant!"
    typer.type_text(test_text)
    print("   ✓ Typing command executed successfully")
    print()
    print("❓ Did the text appear in your text field?")
    print()
    result = input("   Type 'yes' if text appeared, 'no' if not: ").strip().lower()
    
    if result == 'yes':
        print()
        print("   ✅ SUCCESS! Typing is working correctly!")
        print()
        print("   If typing works here but not in Google Docs:")
        print("   - Make sure you CLICK inside the Google Docs document")
        print("   - Check that Google Docs mode is active (blue indicator)")
        print("   - Try refreshing the Google Docs page")
    else:
        print()
        print("   ⚠️  Typing did not work. Possible causes:")
        print()
        print("   1. ACCESSIBILITY PERMISSIONS:")
        print("      → Go to: System Settings > Privacy & Security > Accessibility")
        print("      → Make sure Python (or Terminal) is enabled")
        print("      → You may need to RESTART the app after granting permission")
        print()
        print("   2. TEXT FIELD NOT FOCUSED:")
        print("      → Make sure you clicked inside the text field")
        print("      → Cursor should be blinking")
        print()
        print("   3. TIMING ISSUE:")
        print("      → Wait longer (5-10 seconds) before pressing Enter")
        print("      → Give yourself time to click in the text field")
        
except Exception as e:
    print(f"   ✗ Typing failed with error: {e}")
    print()
    print("   This likely means:")
    print("   - Accessibility permissions not granted")
    print("   - Python not authorized to control keyboard")

print()
print("=" * 60)
print("Diagnostics Complete")
print("=" * 60)
print()
print("📋 SUMMARY:")
print()
print("For typing to work, you need:")
print("✓ Accessibility permissions granted")
print("✓ Text field actively focused (cursor blinking)")
print("✓ Google Docs mode active (for Google Docs typing)")
print()

