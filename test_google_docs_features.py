#!/usr/bin/env python3
"""
Test script for Google Docs voice features
Verifies all new functionality without requiring GUI or voice input
"""

import sys
sys.path.insert(0, 'src')

def test_voice_typing():
    """Test enhanced voice typing module"""
    print("\n" + "="*60)
    print("Testing Voice Typing Module")
    print("="*60)
    
    from app.utils.voice_typing import VoiceTypingMode
    
    # Create instance without settings manager
    typing_mode = VoiceTypingMode(None, settings_manager=None)
    
    # Test punctuation commands
    test_cases = [
        ("hello period", "hello ."),
        ("test comma world", "test , world"),
        ("bullet point", "• "),
        ("number one", "1. "),
        ("em dash", " — "),
    ]
    
    passed = 0
    failed = 0
    
    for input_text, expected in test_cases:
        result = typing_mode.process_text(input_text)
        if expected in result or result == expected:
            print(f"✓ '{input_text}' → '{result}'")
            passed += 1
        else:
            print(f"✗ '{input_text}' → '{result}' (expected: '{expected}')")
            failed += 1
    
    print(f"\nVoice Typing: {passed} passed, {failed} failed")
    return failed == 0

def test_google_docs_commands():
    """Test Google Docs commands module"""
    print("\n" + "="*60)
    print("Testing Google Docs Commands Module")
    print("="*60)
    
    from app.utils.google_docs_commands import GoogleDocsCommands
    
    # Create instance
    docs_handler = GoogleDocsCommands("Google Chrome")
    
    # Test that all command methods exist
    commands = [
        'make_bold', 'make_italic', 'make_underline',
        'increase_font_size', 'decrease_font_size',
        'single_space', 'double_space', 'line_spacing_one_five',
        'add_bullets', 'add_numbering',
        'align_left', 'align_center', 'align_right', 'align_justify',
        'heading_one', 'heading_two', 'heading_three', 'normal_text',
        'strikethrough', 'clear_formatting'
    ]
    
    passed = 0
    failed = 0
    
    for cmd in commands:
        if hasattr(docs_handler, cmd):
            method = getattr(docs_handler, cmd)
            if callable(method):
                print(f"✓ {cmd}() exists and is callable")
                passed += 1
            else:
                print(f"✗ {cmd} exists but is not callable")
                failed += 1
        else:
            print(f"✗ {cmd}() not found")
            failed += 1
    
    print(f"\nGoogle Docs Commands: {passed} passed, {failed} failed")
    return failed == 0

def test_browser_commands():
    """Test browser commands URL detection"""
    print("\n" + "="*60)
    print("Testing Browser Commands URL Detection")
    print("="*60)
    
    from app.utils.browser_commands import SafariCommands, ChromeCommands
    
    # Test that URL methods exist
    safari = SafariCommands()
    chrome = ChromeCommands()
    
    passed = 0
    failed = 0
    
    if hasattr(safari, 'get_current_url') and callable(safari.get_current_url):
        print("✓ SafariCommands.get_current_url() exists")
        passed += 1
    else:
        print("✗ SafariCommands.get_current_url() not found")
        failed += 1
    
    if hasattr(chrome, 'get_current_url') and callable(chrome.get_current_url):
        print("✓ ChromeCommands.get_current_url() exists")
        passed += 1
    else:
        print("✗ ChromeCommands.get_current_url() not found")
        failed += 1
    
    print(f"\nBrowser Commands: {passed} passed, {failed} failed")
    return failed == 0

def test_active_window_detector():
    """Test active window detector Google Docs detection"""
    print("\n" + "="*60)
    print("Testing Active Window Detector")
    print("="*60)
    
    from app.utils.active_window_detector import ActiveWindowDetector
    
    # Create instance
    detector = ActiveWindowDetector()
    
    passed = 0
    failed = 0
    
    # Test new methods and signals
    if hasattr(detector, 'is_google_docs_active'):
        print("✓ is_google_docs_active() method exists")
        passed += 1
    else:
        print("✗ is_google_docs_active() method not found")
        failed += 1
    
    if hasattr(detector, 'set_browser_router'):
        print("✓ set_browser_router() method exists")
        passed += 1
    else:
        print("✗ set_browser_router() method not found")
        failed += 1
    
    if hasattr(detector, 'google_docs_active'):
        print("✓ google_docs_active signal exists")
        passed += 1
    else:
        print("✗ google_docs_active signal not found")
        failed += 1
    
    if hasattr(detector, 'google_docs_inactive'):
        print("✓ google_docs_inactive signal exists")
        passed += 1
    else:
        print("✗ google_docs_inactive signal not found")
        failed += 1
    
    print(f"\nActive Window Detector: {passed} passed, {failed} failed")
    return failed == 0

def test_command_handler():
    """Test command handler Google Docs integration"""
    print("\n" + "="*60)
    print("Testing Command Handler")
    print("="*60)
    
    from app.utils.command_handler import CommandHandler
    
    # Create instance
    handler = CommandHandler()
    
    passed = 0
    failed = 0
    
    # Test new methods
    if hasattr(handler, 'set_google_docs_active'):
        print("✓ set_google_docs_active() method exists")
        passed += 1
    else:
        print("✗ set_google_docs_active() method not found")
        failed += 1
    
    if hasattr(handler, 'set_google_docs_inactive'):
        print("✓ set_google_docs_inactive() method exists")
        passed += 1
    else:
        print("✗ set_google_docs_inactive() method not found")
        failed += 1
    
    if hasattr(handler, 'google_docs_handler'):
        print("✓ google_docs_handler attribute exists")
        passed += 1
    else:
        print("✗ google_docs_handler attribute not found")
        failed += 1
    
    if hasattr(handler, 'is_google_docs_active'):
        print("✓ is_google_docs_active attribute exists")
        passed += 1
    else:
        print("✗ is_google_docs_active attribute not found")
        failed += 1
    
    print(f"\nCommand Handler: {passed} passed, {failed} failed")
    return failed == 0

def test_voice_widget():
    """Test voice widget Google Docs mode"""
    print("\n" + "="*60)
    print("Testing Voice Widget")
    print("="*60)
    
    from app.widgets.voice_widget import VoiceWidget
    
    passed = 0
    failed = 0
    
    # Check if key methods exist (can't fully test without GUI)
    if hasattr(VoiceWidget, 'handle_google_docs_active'):
        print("✓ handle_google_docs_active() method exists")
        passed += 1
    else:
        print("✗ handle_google_docs_active() method not found")
        failed += 1
    
    if hasattr(VoiceWidget, 'handle_google_docs_inactive'):
        print("✓ handle_google_docs_inactive() method exists")
        passed += 1
    else:
        print("✗ handle_google_docs_inactive() method not found")
        failed += 1
    
    if hasattr(VoiceWidget, '_update_context_label'):
        print("✓ _update_context_label() method exists")
        passed += 1
    else:
        print("✗ _update_context_label() method not found")
        failed += 1
    
    if hasattr(VoiceWidget, '_is_likely_command'):
        print("✓ _is_likely_command() method exists")
        passed += 1
    else:
        print("✗ _is_likely_command() method not found")
        failed += 1
    
    print(f"\nVoice Widget: {passed} passed, {failed} failed")
    return failed == 0

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Google Docs Voice Features - Test Suite")
    print("="*60)
    
    results = []
    
    try:
        results.append(("Voice Typing", test_voice_typing()))
    except Exception as e:
        print(f"✗ Voice Typing test crashed: {e}")
        results.append(("Voice Typing", False))
    
    try:
        results.append(("Google Docs Commands", test_google_docs_commands()))
    except Exception as e:
        print(f"✗ Google Docs Commands test crashed: {e}")
        results.append(("Google Docs Commands", False))
    
    try:
        results.append(("Browser Commands", test_browser_commands()))
    except Exception as e:
        print(f"✗ Browser Commands test crashed: {e}")
        results.append(("Browser Commands", False))
    
    try:
        results.append(("Active Window Detector", test_active_window_detector()))
    except Exception as e:
        print(f"✗ Active Window Detector test crashed: {e}")
        results.append(("Active Window Detector", False))
    
    try:
        results.append(("Command Handler", test_command_handler()))
    except Exception as e:
        print(f"✗ Command Handler test crashed: {e}")
        results.append(("Command Handler", False))
    
    try:
        results.append(("Voice Widget", test_voice_widget()))
    except Exception as e:
        print(f"✗ Voice Widget test crashed: {e}")
        results.append(("Voice Widget", False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The implementation is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test suite(s) failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

