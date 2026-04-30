"""
Form workflow manager for multi-step interactions.

Handles progression through steps with validation.
Fully agnostic to business logic — only executes user-provided validators.
"""

from typing import Optional
from .step import Step


class FormWorkflow:
    """
    Manages a sequence of steps with validation.
    
    Handles:
    - Step progression
    - Validation execution
    - Session state management
    
    Example:
        workflow = FormWorkflow([
            Step("name", "Your name?"),
            Step("email", "Email?", validator=email_validator),
            Step("age", "Age?", validator=age_validator),
        ])
        
        # Get current step
        step = workflow.get_step(chat_id, session)
        
        # Validate and advance
        result = workflow.validate_and_advance(
            chat_id, session, user_input
        )
    """
    
    def __init__(self, steps: list[Step]):
        """
        Initialize workflow with steps.
        
        Args:
            steps: List of Step objects in order
        """
        self.steps = steps
        self._step_map = {step.key: i for i, step in enumerate(steps)}
    
    def get_current_step_index(self, chat_id: int, session) -> Optional[int]:
        """Get index of current step from session."""
        key = f"_form_step_{chat_id}"
        try:
            return session.get(chat_id, key) or 0
        except:
            return 0
    
    async def get_current_step_index_async(self, chat_id: int, session) -> Optional[int]:
        """Get index of current step from session (async version)."""
        key = f"_form_step_{chat_id}"
        try:
            result = await session.get(chat_id, key)
            return result or 0
        except:
            return 0
    
    def get_step(self, chat_id: int, session) -> Optional[Step]:
        """Get current step for user."""
        index = self.get_current_step_index(chat_id, session)
        if index is None or index >= len(self.steps):
            return None
        return self.steps[index]
    
    async def get_step_async(self, chat_id: int, session) -> Optional[Step]:
        """Get current step for user (async version)."""
        index = await self.get_current_step_index_async(chat_id, session)
        if index is None or index >= len(self.steps):
            return None
        return self.steps[index]
    
    def is_complete(self, chat_id: int, session) -> bool:
        """Check if workflow is complete."""
        index = self.get_current_step_index(chat_id, session)
        return index >= len(self.steps)
    
    async def is_complete_async(self, chat_id: int, session) -> bool:
        """Check if workflow is complete (async version)."""
        index = await self.get_current_step_index_async(chat_id, session)
        return index >= len(self.steps)
    
    async def validate_and_advance(self, chat_id: int, session, value: str):
        """
        Validate input and advance if valid.
        
        Returns: ValidationResult
        
        If result.ok:
        - Saves value in session
        - Advances to next step
        - Returns ValidationResult(ok=True)
        
        If not result.ok:
        - Does NOT save value
        - Stays on current step
        - Returns ValidationResult(ok=False, error=...)
        """
        step = await self.get_step_async(chat_id, session)
        if step is None:
            return None
        
        # Execute validation
        result = step.validate(value)
        
        if result.ok:
            # Save value
            await session.set(chat_id, step.key, value)
            
            # Advance step counter
            current_index = await self.get_current_step_index_async(chat_id, session)
            await session.set(chat_id, f"_form_step_{chat_id}", current_index + 1)
        
        return result
    
    async def reset(self, chat_id: int, session):
        """Reset workflow to first step."""
        # Delete all step data
        for step in self.steps:
            try:
                await session.delete(chat_id, step.key)
            except:
                pass
        
        # Reset step counter
        await session.set(chat_id, f"_form_step_{chat_id}", 0)
    
    async def get_collected_data(self, chat_id: int, session) -> dict:
        """Get all collected data from completed steps."""
        data = {}
        for step in self.steps:
            try:
                value = await session.get(chat_id, step.key)
                if value is not None:
                    data[step.key] = value
            except:
                pass
        return data
