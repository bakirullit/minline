"""Question primitive - atomic interaction unit in Minline."""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from minline.validation import ValidationResult


@dataclass
class Question:
    """
    Atomic user interaction primitive.
    
    Works STANDALONE or inside Form.
    Independent of higher-level orchestration.
    
    Attributes:
        id: Unique question identifier
        type: Renderer type (text, single_choice, multi_choice, date_picker)
        text: Question text shown to user
        validator: Optional validator(InputEvent) → ValidationResult
        renderer: Renderer configuration name
        config: Type-specific configuration (items, range, format, etc)
    """
    
    id: str
    type: str  # text, single_choice, multi_choice, date_picker, custom
    text: str
    validator: Optional[Callable[[Any], ValidationResult]] = None
    renderer: Optional[str] = None
    config: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate question setup."""
        valid_types = {"text", "single_choice", "multi_choice", "date_picker"}
        if self.type not in valid_types:
            raise ValueError(f"Invalid question type: {self.type}. Must be one of {valid_types}")
        
        # Default renderer = type name if not specified
        if self.renderer is None:
            self.renderer = self.type
    
    async def validate_input(self, input_event) -> ValidationResult:
        """
        Validate user input against this question's validator.
        
        If no validator: returns ok=True.
        If validator exists: calls validator(input_event).
        
        Core principle: validator returns ValidationResult opaquely.
        Core never interprets error/code - just passes through.
        """
        if self.validator is None:
            return ValidationResult(ok=True)
        
        # Call user-defined validator
        if callable(self.validator):
            result = self.validator(input_event)
            if isinstance(result, ValidationResult):
                return result
            raise TypeError(f"Validator must return ValidationResult, got {type(result)}")
        
        return ValidationResult(ok=True)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
