import json
import os
from typing import Dict, List, Optional

class CommandDatabase:
    def __init__(self):
        self.commands = {}
        self.load_commands()
        
    def load_commands(self):
        """Load commands from the JSON file"""
        try:
            file_path = os.path.join(os.path.dirname(__file__), 
                                   '..', 'data', 'commands.json')
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.commands = data['categories']
        except Exception as e:
            print(f"Error loading commands: {str(e)}")
            self.commands = {}
            
    def get_all_categories(self) -> List[str]:
        """Get all command categories"""
        return list(self.commands.keys())
    
    def get_category_info(self, category: str) -> Dict:
        """Get information about a specific category"""
        return self.commands.get(category, {})
    
    def get_command_info(self, category: str, command: str) -> Dict:
        """Get information about a specific command"""
        category_data = self.commands.get(category, {})
        commands = category_data.get('commands', {})
        return commands.get(command, {})
    
    def search_commands(self, query: str) -> List[Dict]:
        """Search for commands matching the query"""
        results = []
        query = query.lower()
        
        for category_id, category in self.commands.items():
            for cmd_id, cmd in category['commands'].items():
                # Search in phrase
                if query in cmd['phrase'].lower():
                    results.append({
                        'category': category_id,
                        'command': cmd_id,
                        'info': cmd
                    })
                    continue
                
                # Search in examples
                for example in cmd['examples']:
                    if query in example.lower():
                        results.append({
                            'category': category_id,
                            'command': cmd_id,
                            'info': cmd
                        })
                        break
                        
        return results
    
    def get_command_by_phrase(self, phrase: str) -> Optional[Dict]:
        """Find a command by its exact phrase"""
        phrase = phrase.lower()
        
        for category_id, category in self.commands.items():
            for cmd_id, cmd in category['commands'].items():
                if cmd['phrase'].lower() == phrase:
                    return {
                        'category': category_id,
                        'command': cmd_id,
                        'info': cmd
                    }
                    
                # Check examples too
                if phrase in [ex.lower() for ex in cmd['examples']]:
                    return {
                        'category': category_id,
                        'command': cmd_id,
                        'info': cmd
                    }
                    
        return None
    
    def get_quick_reference(self) -> List[Dict]:
        """Get a list of commonly used commands for quick reference"""
        common_commands = []
        
        # Add essential commands from each category
        essential_commands = {
            'voice_typing': ['start_typing', 'stop_typing'],
            'punctuation': ['period', 'comma'],
            'app_control': ['open_app'],
            'system_control': ['volume', 'mute'],
            'assistant_control': ['help']
        }
        
        for category, commands in essential_commands.items():
            if category in self.commands:
                for cmd in commands:
                    if cmd in self.commands[category]['commands']:
                        common_commands.append({
                            'category': category,
                            'command': cmd,
                            'info': self.commands[category]['commands'][cmd]
                        })
                        
        return common_commands
    
    def get_contextual_suggestions(self, context: str) -> List[Dict]:
        """Get command suggestions based on context"""
        context = context.lower()
        suggestions = []
        
        # Context-based filtering
        context_mapping = {
            'typing': ['voice_typing', 'punctuation'],
            'browser': ['web_commands'],
            'volume': ['system_control'],
            'app': ['app_control'],
            'help': ['assistant_control']
        }
        
        relevant_categories = []
        for key, categories in context_mapping.items():
            if key in context:
                relevant_categories.extend(categories)
                
        if not relevant_categories:  # If no specific context, return common commands
            return self.get_quick_reference()
            
        # Get commands from relevant categories
        for category in relevant_categories:
            if category in self.commands:
                for cmd_id, cmd in self.commands[category]['commands'].items():
                    suggestions.append({
                        'category': category,
                        'command': cmd_id,
                        'info': cmd
                    })
                    
        return suggestions
