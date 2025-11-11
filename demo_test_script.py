#!/usr/bin/env python3
"""
Demo Test Script - Run this before your presentation!
Tests all commands you'll demo to ensure they work.
"""

import subprocess
import time

class DemoTester:
    def __init__(self):
        self.passed = []
        self.failed = []
    
    def test_command(self, name, script):
        """Test an AppleScript command"""
        print(f"Testing: {name}...", end=" ")
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("✅ PASS")
                self.passed.append(name)
                return True
            else:
                print(f"❌ FAIL: {result.stderr}")
                self.failed.append(name)
                return False
        except Exception as e:
            print(f"❌ ERROR: {e}")
            self.failed.append(name)
            return False
    
    def run_browser_tests(self, browser="Safari"):
        """Test critical browser commands for demo"""
        print(f"\n{'='*50}")
        print(f"Testing {browser} Commands for Demo")
        print(f"{'='*50}\n")
        
        print("⚠️  Make sure Safari is open before running!\n")
        time.sleep(2)
        
        # Test 1: New Tab
        self.test_command(
            "New Tab",
            f'''
            tell application "{browser}"
                tell front window
                    make new tab
                end tell
            end tell
            '''
        )
        time.sleep(1)
        
        # Test 2: Navigation
        self.test_command(
            "Navigate to URL",
            f'''
            tell application "{browser}"
                set URL of current tab of front window to "https://github.com"
            end tell
            '''
        )
        time.sleep(2)
        
        # Test 3: Scroll
        self.test_command(
            "Scroll Down",
            f'''
            tell application "System Events"
                tell process "{browser}"
                    key code 125
                end tell
            end tell
            '''
        )
        time.sleep(1)
        
        # Test 4: Close Tab
        self.test_command(
            "Close Tab",
            f'''
            tell application "{browser}"
                close current tab of front window
            end tell
            '''
        )
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"Test Summary")
        print(f"{'='*50}")
        print(f"✅ Passed: {len(self.passed)}/{len(self.passed) + len(self.failed)}")
        if self.failed:
            print(f"❌ Failed: {', '.join(self.failed)}")
        else:
            print("🎉 All tests passed! You're ready to demo!")
        print(f"{'='*50}\n")
    
    def test_voice_recognition(self):
        """Test voice recognition setup"""
        print(f"\n{'='*50}")
        print("Testing Voice Recognition Dependencies")
        print(f"{'='*50}\n")
        
        try:
            import speech_recognition as sr
            print("✅ speech_recognition imported")
            
            r = sr.Recognizer()
            print("✅ Recognizer initialized")
            
            mic = sr.Microphone()
            print("✅ Microphone detected")
            
            print("\n🎤 Testing microphone access...")
            with mic as source:
                print("   Listening for 1 second...")
                audio = r.listen(source, timeout=1, phrase_time_limit=1)
                print("✅ Audio captured successfully")
            
            print("\n🎉 Voice recognition is ready!")
            
        except Exception as e:
            print(f"❌ Voice recognition issue: {e}")
            print("\nTroubleshooting:")
            print("- Check microphone permissions")
            print("- Ensure internet connection for Google Speech API")
            print("- Run: pip3 install -r requirements.txt")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════╗
    ║  Voice Assistant Demo Pre-Flight Check          ║
    ╚══════════════════════════════════════════════════╝
    
    This script tests the commands you'll use in your demo.
    Run this 5 minutes before presenting!
    """)
    
    tester = DemoTester()
    
    # Test voice recognition first
    tester.test_voice_recognition()
    
    # Test browser commands
    response = input("\n\nTest Safari commands? (y/n): ")
    if response.lower() == 'y':
        tester.run_browser_tests("Safari")
    
    print("\n📝 Pre-Demo Checklist:")
    print("  [ ] Safari is open")
    print("  [ ] Internet connection working")
    print("  [ ] Microphone working")
    print("  [ ] Accessibility permissions granted")
    print("  [ ] Floating button visible")
    print("  [ ] Volume at appropriate level")
    print("\nGood luck with your presentation! 🚀")

