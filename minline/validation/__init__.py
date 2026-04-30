"""
Validation layer for Minline.

Contract-based, user-defined, fully optional validation mechanism.
Framework executes validators but never interprets validation logic.
"""

from .result import ValidationResult
from .step import Step
from .workflow import FormWorkflow
from .form import Form

__all__ = ["ValidationResult", "Step", "FormWorkflow", "Form"]
