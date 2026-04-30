"""Base renderer class - all Question renderers inherit from this."""

from abc import ABC, abstractmethod
from aiogram.types import InlineKeyboardMarkup


class BaseRenderer(ABC):
    """
    Abstract renderer for Question types.
    
    Converts a Question + config into Telegram UI components.
    Stateless - only depends on Question definition.
    """
    
    @abstractmethod
    def render(self, question, show_back: bool = False) -> InlineKeyboardMarkup:
        """
        Render question as Telegram InlineKeyboardMarkup.
        
        Args:
            question: Question instance
            show_back: Whether to show back button
            
        Returns:
            InlineKeyboardMarkup for inline buttons, or None for text-only
        """
        pass
    
    @abstractmethod
    def parse_input(self, input_event) -> any:
        """
        Parse InputEvent into question-specific value.
        
        E.g., single_choice parses "1" → items[0]
        """
        pass
