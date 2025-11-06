#!/usr/bin/env python3
"""
Quick diagnostic to check if browser detection is working
"""

import sys
sys.path.insert(0, 'src')

from app.utils.command_handler import CommandHandler

print("\n" + "="*60)
print("DIAGNOSTIC: Testing 'new tab' command")
print("="*60)

# Create handler
handler = CommandHandler()

# Track results
executed = []
failed = []

def on_executed(msg):
    executed.append(msg)
    print(f"✅ SUCCESS: {msg}")

def on_failed(msg):
    failed.append(msg)
    print(f"❌ FAILED: {msg}")

handler.command_executed.connect(on_executed)
handler.command_failed.connect(on_failed)

print("\n1. Testing WITHOUT browser mode (should fail):")
print("   Simulating: 'new tab' command")
handler.process_command("new tab")

print("\n2. Testing WITH browser mode activated:")
print("   Setting browser to Safari...")
handler.set_browser_active("Safari")
print(f"   Browser active: {handler.is_browser_active}")
print(f"   Context: {handler.current_context}")

print("\n   Simulating: 'new tab' command")
handler.process_command("new tab")

print("\n" + "="*60)
print("RESULTS:")
print("="*60)
if len(executed) > 0:
    print(f"✅ Commands executed: {len(executed)}")
    print("   The command routing is working!")
    print("\n   If this works but the app doesn't, the issue is:")
    print("   → Browser detection not activating (no green banner)")
    print("   → Or you're in Typing Mode instead of Command Mode")
else:
    print("❌ No commands executed")
    print("   This suggests a deeper issue with command routing")

if len(failed) > 0:
    print(f"\n⚠️  Commands failed: {len(failed)}")
    for f in failed:
        print(f"   - {f}")

print("\n" + "="*60)
print("\nNEXT STEPS:")
print("1. Run the voice assistant")
print("2. Open Safari or Chrome")
print("3. Look for: 🌐 Browser Mode: Safari")
print("4. Click 'Command Mode' button")
print("5. Say 'new tab'")
print("\nIf you DON'T see the browser mode banner:")
print("→ Check System Settings > Privacy > Accessibility")
print("→ Make sure Python is in the allowed list")
print("="*60)

