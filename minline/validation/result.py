"""
ValidationResult contract.

Fully opaque to framework — only OK/error_message matter.
Code field is for user to track error types if needed.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """
    Result of user input validation.
    
    Attributes:
        ok: True if input is valid, False otherwise
        error: Human-readable error message (shown to user if ok=False)
        code: Optional machine-readable identifier for error tracking
    
    Examples:
        >>> ValidationResult(ok=True)  # Accept input
        >>> ValidationResult(ok=False, error="Email invalid", code="INVALID_EMAIL")
    """
    ok: bool
    error: Optional[str] = None
    code: Optional[str] = None
