from typing import List, Dict
from .command_database import CommandDatabase

class ContextualHelp:
    def __init__(self):
        self.command_db = CommandDatabase()
        self.context_history = []
        self.setup_context_triggers()
        
    def setup_context_triggers(self):
        """Set up context triggers and their associated categories"""
        self.context_triggers = {
            # Voice typing contexts
            'typing': ['voice_typing', 'punctuation'],
            'dictation': ['voice_typing', 'punctuation'],
            'write': ['voice_typing', 'punctuation'],
            'text': ['voice_typing', 'punctuation'],
            
            # App control contexts
            'open': ['app_control'],
            'close': ['app_control'],
            'switch': ['app_control'],
            'app': ['app_control'],
            'application': ['app_control'],
            
            # System control contexts
            'volume': ['system_control'],
            'sound': ['system_control'],
            'mute': ['system_control'],
            'system': ['system_control'],
            
            # Web contexts
            'search': ['web_commands'],
            'browser': ['web_commands'],
            'website': ['web_commands'],
            'internet': ['web_commands'],
            
            # Help contexts
            'help': ['assistant_control'],
            'assist': ['assistant_control'],
            'guide': ['assistant_control']
        }
        
    def analyze_context(self, text: str) -> List[str]:
        """Analyze text to determine relevant context categories"""
        text = text.lower()
        relevant_categories = set()
        
        # Check for trigger words
        for trigger, categories in self.context_triggers.items():
            if trigger in text:
                relevant_categories.update(categories)
                
        return list(relevant_categories)
        
    def get_contextual_suggestions(self, text: str) -> List[Dict]:
        """Get command suggestions based on current context"""
        # Analyze current context
        current_categories = self.analyze_context(text)
        
        # If no specific context found, use recent history
        if not current_categories and self.context_history:
            current_categories = self.context_history[-1]
            
        # If still no context, return common commands
        if not current_categories:
            return self.command_db.get_quick_reference()
            
        # Get relevant commands
        suggestions = []
        for category in current_categories:
            category_info = self.command_db.get_category_info(category)
            if category_info and 'commands' in category_info:
                for cmd_id, cmd_info in category_info['commands'].items():
                    suggestions.append({
                        'category': category,
                        'command': cmd_id,
                        'info': cmd_info
                    })
                    
        # Update context history
        if current_categories:
            self.context_history.append(current_categories)
            # Keep history manageable
            if len(self.context_history) > 5:
                self.context_history.pop(0)
                
        return suggestions
        
    def get_contextual_help(self, text: str) -> Dict:
        """Get help information based on current context"""
        categories = self.analyze_context(text)
        
        help_info = {
            'title': 'Contextual Help',
            'categories': [],
            'suggestions': []
        }
        
        if categories:
            for category in categories:
                category_info = self.command_db.get_category_info(category)
                if category_info:
                    help_info['categories'].append({
                        'name': category_info['name'],
                        'description': category_info['description']
                    })
                    
            # Add relevant command suggestions
            help_info['suggestions'] = self.get_contextual_suggestions(text)
            
        return help_info
        
    def get_quick_tip(self, context: str) -> str:
        """Get a quick tip based on current context"""
        categories = self.analyze_context(context)
        
        tips = {
            'voice_typing': [
                "Say 'period' to add punctuation",
                "Use 'new line' to start a new line",
                "Say 'delete that' to remove the last word"
            ],
            'app_control': [
                "Say 'open' followed by any app name",
                "Use 'switch to' to change between apps",
                "Say 'close' to quit an application"
            ],
            'system_control': [
                "Control volume with 'volume' followed by a number",
                "Quick mute with just saying 'mute'",
                "Adjust system settings easily with voice commands"
            ],
            'web_commands': [
                "Search the web by saying 'search for' followed by your query",
                "Open websites with 'go to' followed by the URL",
                "Quick searches work with natural language"
            ]
        }
        
        # Get relevant tips
        relevant_tips = []
        for category in categories:
            if category in tips:
                relevant_tips.extend(tips[category])
                
        if relevant_tips:
            # Return a random tip from the relevant ones
            from random import choice
            return choice(relevant_tips)
            
        return "Say 'help' at any time to see available commands"
