#!/usr/bin/env python3
"""
Test if the floating button can be created and shown
"""

import sys
sys.path.insert(0, 'src')

from PyQt6.QtWidgets import QApplication
from app.widgets.floating_button import FloatingButton

print("Testing Floating Button...")
print()

# Create QApplication
app = QApplication(sys.argv)
print("✓ QApplication created")

# Create floating button
try:
    button = FloatingButton()
    print("✓ FloatingButton instance created")
except Exception as e:
    print(f"✗ FloatingButton creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Show the button
try:
    button.show()
    print("✓ FloatingButton.show() called")
    print()
    print("=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print()
    print("🎯 LOOK FOR THE FLOATING BUTTON:")
    print("   - Should appear in the bottom-right corner of your screen")
    print("   - Small circular button with microphone icon")
    print("   - Gray/dark color")
    print()
    print("❓ Do you see it?")
    print()
    print("Press Ctrl+C to exit this test")
    print("=" * 60)
    
    # Run the app
    sys.exit(app.exec())
    
except Exception as e:
    print(f"✗ FloatingButton.show() failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

