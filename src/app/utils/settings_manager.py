import json
import os
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.settings_dir = os.path.expanduser("~/.voice_assistant")
        self.settings_file = os.path.join(self.settings_dir, "settings.json")
        self.default_settings = {
            "voice_recognition": {
                "energy_threshold": 150,  # Lower = more sensitive (was 300)
                "dynamic_energy_threshold": True,
                "dynamic_energy_adjustment_damping": 0.15,
                "dynamic_energy_ratio": 1.5,  # Better ambient noise handling
                "pause_threshold": 0.8,  # Faster response time (was 1.2)
                "phrase_threshold": 0.2,  # Quicker detection (was 0.3)
                "non_speaking_duration": 0.5,  # Better end detection
                "audio_threshold": 0.01,
            },
            "theme": {
                "dark_mode": None,  # None means follow system
                "opacity": 1.0
            },
            "interface": {
                "show_floating_button": True,
                "start_minimized": False,
                "onboarding_completed": False,
                "skip_intro": False
            },
            "shortcuts": {
                "start_listening": "Ctrl+Space",
                "show_hide": "Ctrl+Alt+V",
                "quick_commands": "Ctrl+Q",
                "switch_mode": "Ctrl+M"
            }
        }
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from file or create with defaults"""
        try:
            # Create settings directory if it doesn't exist
            os.makedirs(self.settings_dir, exist_ok=True)
            
            # Load existing settings or create new ones
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    # Merge with defaults to ensure all settings exist
                    return self._merge_settings(self.default_settings, saved_settings)
            else:
                self.save_settings(self.default_settings)
                return self.default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings

    def save_settings(self, settings):
        """Save settings to file"""
        try:
            os.makedirs(self.settings_dir, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
            self.settings = settings
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_setting(self, category, key):
        """Get a specific setting value"""
        try:
            return self.settings[category][key]
        except KeyError:
            # Return default if setting doesn't exist
            return self.default_settings.get(category, {}).get(key)

    def update_setting(self, category, key, value):
        """Update a specific setting"""
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value
        return self.save_settings(self.settings)

    def _merge_settings(self, defaults, saved):
        """Merge saved settings with defaults to ensure all settings exist"""
        merged = defaults.copy()
        for category in saved:
            if category in merged:
                merged[category].update(saved[category])
        return merged

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        return self.save_settings(self.default_settings)
