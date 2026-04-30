"""
Step model for multi-step forms with optional validation.

Step is a question-answer pair with optional validator.
Validator is fully user-owned: framework only executes it.
"""

from typing import Callable, Optional
from .result import ValidationResult


class Step:
    """
    A single step in a multi-step form flow.
    
    Attributes:
        key: Unique identifier for this step (used in session storage)
        question: Prompt text shown to user
        validator: Optional callable that validates user input
        
    Examples:
        # Without validation (input always accepted)
        step = Step(
            key="name",
            question="What is your name?"
        )
        
        # With validation
        def iin_validator(value: str) -> ValidationResult:
            if not value.isdigit() or len(value) != 12:
                return ValidationResult(False, "IIN must be 12 digits", "INVALID_IIN")
            return ValidationResult(True)
        
        step = Step(
            key="iin",
            question="Enter your IIN (12 digits):",
            validator=iin_validator
        )
    """
    
    def __init__(
        self,
        key: str,
        question: str,
        validator: Optional[Callable[[str], ValidationResult]] = None
    ):
        """
        Initialize a step.
        
        Args:
            key: Unique step identifier
            question: Question text to show user
            validator: Optional validation function(value: str) -> ValidationResult
        """
        self.key = key
        self.question = question
        self.validator = validator
    
    def validate(self, value: str) -> ValidationResult:
        """
        Validate input value.
        
        If no validator: always returns ok=True
        If validator exists: executes it and returns result
        """
        if self.validator is None:
            return ValidationResult(ok=True)
        return self.validator(value)
