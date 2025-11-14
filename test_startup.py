#!/usr/bin/env python3
"""
Test script to verify the application can start without errors
"""

import sys
sys.path.insert(0, 'src')

print("Testing application startup...")
print("="*60)

try:
    # Test all critical imports
    print("\n1. Testing imports...")
    from PyQt6.QtWidgets import QApplication
    from app.main_window import MainWindow
    print("   ✓ Main imports successful")
    
    # Test that MainWindow can be instantiated
    print("\n2. Testing MainWindow instantiation...")
    app = QApplication(sys.argv)
    window = MainWindow()
    print("   ✓ MainWindow created successfully")
    
    # Check that voice widget has necessary attributes
    print("\n3. Testing VoiceWidget integration...")
    if hasattr(window, 'voice_widget'):
        print("   ✓ voice_widget attribute exists")
        
        voice_widget = window.voice_widget
        
        # Check for Google Docs methods
        if hasattr(voice_widget, 'handle_google_docs_active'):
            print("   ✓ Google Docs active handler exists")
        if hasattr(voice_widget, 'handle_google_docs_inactive'):
            print("   ✓ Google Docs inactive handler exists")
        if hasattr(voice_widget, 'current_context'):
            print(f"   ✓ Current context: {voice_widget.current_context}")
        
        # Check command handler
        if hasattr(voice_widget, 'command_handler'):
            cmd_handler = voice_widget.command_handler
            if hasattr(cmd_handler, 'google_docs_handler'):
                print("   ✓ Google Docs command handler exists")
            if hasattr(cmd_handler, 'is_google_docs_active'):
                print("   ✓ Google Docs active flag exists")
        
        # Check window detector
        if hasattr(voice_widget, 'window_detector'):
            detector = voice_widget.window_detector
            if hasattr(detector, 'google_docs_active'):
                print("   ✓ Google Docs active signal exists")
            if hasattr(detector, 'is_google_docs_active'):
                print("   ✓ Google Docs active check method exists")
    
    print("\n" + "="*60)
    print("✅ Application startup test PASSED")
    print("="*60)
    print("\nThe application is ready to run!")
    print("Start it with: python3 src/main.py")
    
    # Clean up
    app.quit()
    sys.exit(0)
    
except Exception as e:
    print("\n" + "="*60)
    print("❌ Application startup test FAILED")
    print("="*60)
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

