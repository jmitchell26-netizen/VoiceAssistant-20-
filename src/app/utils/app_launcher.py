"""
Enhanced Application Launcher
Handles opening applications with smart name matching, aliases, and fuzzy search.
"""

import subprocess
import platform
import os
from difflib import SequenceMatcher
from PyQt6.QtCore import QObject, pyqtSignal


class AppLauncher(QObject):
    """
    Smart application launcher with alias support and fuzzy matching.
    Makes voice commands more flexible by understanding common app names.
    """
    
    app_opened = pyqtSignal(str)  # Emits actual app name that was opened
    app_not_found = pyqtSignal(str, list)  # Emits failed name and suggestions
    
    def __init__(self):
        super().__init__()
        
        # Common application aliases (voice command -> actual app name)
        self.app_aliases = {
            # Browsers
            'chrome': 'Google Chrome',
            'firefox': 'Firefox',
            'safari': 'Safari',
            'brave': 'Brave Browser',
            'edge': 'Microsoft Edge',
            'arc': 'Arc',
            
            # Development
            'vs code': 'Visual Studio Code',
            'vscode': 'Visual Studio Code',
            'code': 'Visual Studio Code',
            'visual studio': 'Visual Studio Code',
            'pycharm': 'PyCharm',
            'xcode': 'Xcode',
            'cursor': 'Cursor',
            'sublime': 'Sublime Text',
            'atom': 'Atom',
            
            # Communication
            'slack': 'Slack',
            'discord': 'Discord',
            'zoom': 'zoom.us',
            'teams': 'Microsoft Teams',
            'skype': 'Skype',
            'messages': 'Messages',
            'mail': 'Mail',
            'facetime': 'FaceTime',
            
            # Productivity
            'word': 'Microsoft Word',
            'excel': 'Microsoft Excel',
            'powerpoint': 'Microsoft PowerPoint',
            'keynote': 'Keynote',
            'pages': 'Pages',
            'numbers': 'Numbers',
            'notes': 'Notes',
            'reminders': 'Reminders',
            'calendar': 'Calendar',
            'notion': 'Notion',
            'obsidian': 'Obsidian',
            
            # Media
            'spotify': 'Spotify',
            'music': 'Music',
            'apple music': 'Music',
            'itunes': 'Music',
            'vlc': 'VLC',
            'photoshop': 'Adobe Photoshop',
            'illustrator': 'Adobe Illustrator',
            'final cut': 'Final Cut Pro',
            'imovie': 'iMovie',
            
            # Utilities
            'terminal': 'Terminal',
            'finder': 'Finder',
            'calculator': 'Calculator',
            'preview': 'Preview',
            'activity monitor': 'Activity Monitor',
            'system preferences': 'System Preferences',
            'system settings': 'System Settings',
            'app store': 'App Store',
            
            # Other
            'docker': 'Docker',
            'postman': 'Postman',
            'github desktop': 'GitHub Desktop',
            'gitkraken': 'GitKraken',
        }
        
        # Cache of installed applications
        self._installed_apps_cache = None
    
    def open_app(self, app_name):
        """
        Open an application with smart matching.
        
        Args:
            app_name: The app name from voice command (case-insensitive)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not app_name:
            return False, "No application name provided"
        
        app_name = app_name.strip().lower()
        
        # Step 1: Check exact alias match
        actual_name = self._resolve_alias(app_name)
        
        # Step 2: Try to open with resolved name
        success, message = self._try_open(actual_name)
        
        if success:
            self.app_opened.emit(actual_name)
            return True, message
        
        # Step 3: Try fuzzy matching with installed apps
        if platform.system() == 'Darwin':
            installed_apps = self._get_installed_apps()
            best_match = self._find_best_match(app_name, installed_apps)
            
            if best_match:
                success, message = self._try_open(best_match)
                if success:
                    self.app_opened.emit(best_match)
                    return True, message
        
        # Step 4: Failed to find/open app
        suggestions = self._get_suggestions(app_name)
        self.app_not_found.emit(app_name, suggestions)
        return False, f"Could not find application: {app_name}"
    
    def _resolve_alias(self, app_name):
        """
        Resolve an app name using the alias dictionary.
        
        Args:
            app_name: App name from voice command (lowercase)
        
        Returns:
            str: Actual app name to use
        """
        # Check exact match in aliases
        if app_name in self.app_aliases:
            return self.app_aliases[app_name]
        
        # Check partial matches (e.g., "visual" -> "Visual Studio Code")
        for alias, actual in self.app_aliases.items():
            if app_name in alias or alias in app_name:
                return actual
        
        # Return original with title case
        return app_name.title()
    
    def _try_open(self, app_name):
        """
        Attempt to open an application.
        
        Args:
            app_name: The actual application name
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            if platform.system() == 'Darwin':  # macOS
                result = subprocess.run(
                    ['open', '-a', app_name],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                
                if result.returncode == 0:
                    return True, f"Opened {app_name}"
                else:
                    return False, f"Failed to open {app_name}"
            else:
                return False, "App launching only supported on macOS currently"
                
        except subprocess.TimeoutExpired:
            return False, f"Timeout opening {app_name}"
        except Exception as e:
            return False, f"Error opening {app_name}: {str(e)}"
    
    def _get_installed_apps(self):
        """
        Get list of installed applications on macOS.
        Uses cached list if available.
        
        Returns:
            list: List of installed application names
        """
        if self._installed_apps_cache is not None:
            return self._installed_apps_cache
        
        apps = []
        
        try:
            # Check /Applications
            if os.path.exists('/Applications'):
                for item in os.listdir('/Applications'):
                    if item.endswith('.app'):
                        app_name = item.replace('.app', '')
                        apps.append(app_name)
            
            # Check ~/Applications
            home_apps = os.path.expanduser('~/Applications')
            if os.path.exists(home_apps):
                for item in os.listdir(home_apps):
                    if item.endswith('.app'):
                        app_name = item.replace('.app', '')
                        apps.append(app_name)
            
            # Cache the result
            self._installed_apps_cache = apps
            
        except Exception as e:
            print(f"Error scanning for applications: {e}")
        
        return apps
    
    def _find_best_match(self, query, candidates, threshold=0.6):
        """
        Find the best matching app name using fuzzy string matching.
        
        Args:
            query: The search query (lowercase)
            candidates: List of candidate app names
            threshold: Minimum similarity score (0.0 to 1.0)
        
        Returns:
            str or None: Best matching app name, or None if no good match
        """
        best_match = None
        best_score = threshold
        
        for candidate in candidates:
            # Compare with lowercase version
            score = SequenceMatcher(None, query, candidate.lower()).ratio()
            
            if score > best_score:
                best_score = score
                best_match = candidate
        
        return best_match
    
    def _get_suggestions(self, app_name):
        """
        Get suggestions for apps that might match the query.
        
        Args:
            app_name: The app name that wasn't found
        
        Returns:
            list: List of suggested app names
        """
        suggestions = []
        
        # Check aliases for partial matches
        for alias, actual in self.app_aliases.items():
            if app_name in alias or alias in app_name:
                if actual not in suggestions:
                    suggestions.append(actual)
        
        # If no suggestions, get from installed apps
        if not suggestions and platform.system() == 'Darwin':
            installed = self._get_installed_apps()
            for app in installed:
                if app_name in app.lower():
                    suggestions.append(app)
                    if len(suggestions) >= 3:
                        break
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def list_installed_apps(self):
        """
        Get a list of all installed applications.
        
        Returns:
            list: Sorted list of installed app names
        """
        apps = self._get_installed_apps()
        return sorted(apps)
    
    def add_alias(self, alias, actual_name):
        """
        Add a custom alias for an application.
        
        Args:
            alias: The voice command name (lowercase)
            actual_name: The actual application name
        """
        self.app_aliases[alias.lower()] = actual_name
        print(f"Added alias: '{alias}' → '{actual_name}'")
    
    def clear_cache(self):
        """Clear the installed applications cache."""
        self._installed_apps_cache = None


# Convenience function for quick app launching
def quick_open(app_name):
    """
    Quick function to open an app without creating a launcher instance.
    
    Args:
        app_name: Application name to open
    
    Returns:
        bool: True if successful, False otherwise
    """
    launcher = AppLauncher()
    success, message = launcher.open_app(app_name)
    print(message)
    return success

