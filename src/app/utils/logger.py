"""Centralized logging utility for the Voice Assistant application"""
import logging
import sys
from pathlib import Path
from typing import Optional

class VoiceAssistantLogger:
    """Centralized logger for the Voice Assistant application"""
    
    _instance: Optional['VoiceAssistantLogger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the logger configuration"""
        if self._logger is None:
            self._logger = logging.getLogger('VoiceAssistant')
            self._logger.setLevel(logging.DEBUG)
            
            # Prevent duplicate handlers
            if not self._logger.handlers:
                # Console handler
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(logging.INFO)
                
                # File handler (optional - creates log file in user directory)
                try:
                    log_dir = Path.home() / '.voice_assistant'
                    log_dir.mkdir(exist_ok=True)
                    log_file = log_dir / 'voice_assistant.log'
                    
                    file_handler = logging.FileHandler(log_file)
                    file_handler.setLevel(logging.DEBUG)
                    file_formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
                    file_handler.setFormatter(file_formatter)
                    self._logger.addHandler(file_handler)
                except Exception:
                    # If file logging fails, continue without it
                    pass
                
                # Console formatter
                console_formatter = logging.Formatter(
                    '%(levelname)s - %(message)s'
                )
                console_handler.setFormatter(console_formatter)
                self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the logger instance"""
        return self._logger
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Class method to get logger instance"""
        instance = cls()
        return instance._logger

# Convenience function to get logger
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance, optionally with a specific name"""
    if name:
        return logging.getLogger(f'VoiceAssistant.{name}')
    return VoiceAssistantLogger.get_logger()



