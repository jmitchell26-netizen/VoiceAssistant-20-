#!/usr/bin/env python3
"""
Simple test script to verify browser detection and command routing
Run this to test the browser feature independently
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add src to path
sys.path.insert(0, 'src')

from app.utils.active_window_detector import ActiveWindowDetector
from app.utils.browser_commands import BrowserCommandRouter
from app.utils.command_handler import CommandHandler


def test_window_detection():
    """Test 1: Window detection works"""
    print("\n" + "="*60)
    print("TEST 1: Active Window Detection")
    print("="*60)
    
    print("\n[INFO] Creating window detector...")
    detector = ActiveWindowDetector()
    
    # Track detected apps
    detected_apps = []
    browser_activations = []
    
    def on_app_changed(app_name):
        detected_apps.append(app_name)
        print(f"[DETECTED] Active app: {app_name}")
    
    def on_browser_active(browser_name):
        browser_activations.append(browser_name)
        print(f"[BROWSER] Browser activated: {browser_name}")
    
    def on_browser_inactive():
        print(f"[BROWSER] Browser deactivated")
    
    # Connect signals
    detector.active_app_changed.connect(on_app_changed)
    detector.browser_active.connect(on_browser_active)
    detector.browser_inactive.connect(on_browser_inactive)
    
    print("[INFO] Starting detection...")
    detector.start()
    
    print("\n[ACTION REQUIRED] Please switch between applications:")
    print("  1. Switch to Safari or Chrome")
    print("  2. Switch to another app (Finder, Terminal, etc.)")
    print("  3. Switch back to browser")
    print("  4. Wait for test to complete (10 seconds)...\n")
    
    # Run for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:
        app.processEvents()
        time.sleep(0.1)
    
    detector.stop()
    
    # Results
    print("\n[RESULTS]")
    print(f"  Apps detected: {len(detected_apps)}")
    print(f"  Browser activations: {len(browser_activations)}")
    
    if len(detected_apps) > 0:
        print("  ✅ Window detection working")
    else:
        print("  ❌ No apps detected - check permissions!")
        return False
    
    if len(browser_activations) > 0:
        print(f"  ✅ Browser detection working ({browser_activations[0]})")
    else:
        print("  ⚠️  No browsers detected - did you switch to Safari/Chrome?")
    
    return len(detected_apps) > 0


def test_command_routing():
    """Test 2: Command routing with context"""
    print("\n" + "="*60)
    print("TEST 2: Command Routing")
    print("="*60)
    
    print("\n[INFO] Creating command handler...")
    handler = CommandHandler()
    
    # Track executed commands
    executed_commands = []
    failed_commands = []
    
    def on_command_executed(msg):
        executed_commands.append(msg)
        print(f"[SUCCESS] {msg}")
    
    def on_command_failed(msg):
        failed_commands.append(msg)
        print(f"[FAILED] {msg}")
    
    handler.command_executed.connect(on_command_executed)
    handler.command_failed.connect(on_command_failed)
    
    # Test 2a: General commands
    print("\n[TEST 2a] Testing general commands...")
    handler.process_command("minimize window")
    app.processEvents()
    
    # Test 2b: Activate browser context
    print("\n[TEST 2b] Activating browser context...")
    handler.set_browser_active("Safari")
    
    # Test 2c: Browser commands
    print("\n[TEST 2c] Testing browser commands (should fail if no browser open)...")
    print("  Note: These will fail unless Safari is actually open and active")
    handler.process_command("new tab")
    app.processEvents()
    
    handler.process_command("go to example.com")
    app.processEvents()
    
    # Test 2d: Deactivate browser context
    print("\n[TEST 2d] Deactivating browser context...")
    handler.set_browser_inactive()
    
    # Results
    print("\n[RESULTS]")
    print(f"  Commands executed: {len(executed_commands)}")
    print(f"  Commands failed: {len(failed_commands)}")
    
    if len(executed_commands) + len(failed_commands) > 0:
        print("  ✅ Command routing working")
        return True
    else:
        print("  ❌ No commands processed")
        return False


def test_browser_commands():
    """Test 3: Browser command execution"""
    print("\n" + "="*60)
    print("TEST 3: Browser Command Execution")
    print("="*60)
    
    print("\n[INFO] Creating browser command router...")
    router = BrowserCommandRouter()
    
    # Track results
    successes = []
    failures = []
    
    def on_success(msg):
        successes.append(msg)
        print(f"[SUCCESS] {msg}")
    
    def on_failure(msg):
        failures.append(msg)
        print(f"[FAILED] {msg}")
    
    router.command_executed.connect(on_success)
    router.command_failed.connect(on_failure)
    
    print("\n[ACTION REQUIRED] Open Safari or Chrome before continuing")
    input("Press Enter when browser is open...")
    
    print("\n[TEST 3a] Setting active browser to Safari...")
    router.set_active_browser("Safari")
    
    print("\n[TEST 3b] Testing 'new_tab' command...")
    print("  This should open a new tab in Safari")
    router.execute_command('new_tab')
    app.processEvents()
    time.sleep(1)
    
    print("\n[TEST 3c] Testing 'go_to_url' command...")
    print("  This should navigate to example.com")
    router.execute_command('go_to_url', 'example.com')
    app.processEvents()
    time.sleep(2)
    
    print("\n[TEST 3d] Testing 'close_tab' command...")
    print("  This should close the current tab")
    router.execute_command('close_tab')
    app.processEvents()
    
    # Results
    print("\n[RESULTS]")
    print(f"  Successful commands: {len(successes)}")
    print(f"  Failed commands: {len(failures)}")
    
    if len(successes) > 0:
        print("  ✅ Browser commands working")
        return True
    else:
        print("  ❌ No successful commands - check browser is open and permissions granted")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("BROWSER POWER USER FEATURE - TEST SUITE")
    print("="*60)
    print("\nThis script will test:")
    print("  1. Active window detection")
    print("  2. Command routing with context")
    print("  3. Browser command execution")
    print("\nNOTE: You'll need to interact during tests.")
    print("="*60)
    
    input("\nPress Enter to start tests...")
    
    # Run tests
    test1_passed = test_window_detection()
    test2_passed = test_command_routing()
    test3_passed = test_browser_commands()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"  Window Detection: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Command Routing: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"  Browser Commands: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests passed! Feature is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        print("     Common issues:")
        print("     - Accessibility permissions not granted")
        print("     - Browser not open during browser command tests")
        print("     - AppleScript blocked by security settings")
    
    print("="*60)


if __name__ == '__main__':
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Run tests
    QTimer.singleShot(100, main)
    
    # Keep app running
    sys.exit(app.exec())

