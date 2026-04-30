"""
Tests for validation layer.

Tests that validators are executed correctly and results are handled properly.
"""

import pytest
from minline.validation import ValidationResult, Step, FormWorkflow


class TestValidationResult:
    """Test ValidationResult contract."""
    
    def test_valid_result(self):
        result = ValidationResult(ok=True)
        assert result.ok is True
        assert result.error is None
        assert result.code is None
    
    def test_invalid_result_with_error(self):
        result = ValidationResult(
            ok=False,
            error="Invalid email",
            code="INVALID_EMAIL"
        )
        assert result.ok is False
        assert result.error == "Invalid email"
        assert result.code == "INVALID_EMAIL"


class TestStep:
    """Test Step model."""
    
    def test_step_without_validator(self):
        step = Step("email", "Your email?")
        assert step.key == "email"
        assert step.question == "Your email?"
        assert step.validator is None
        
        # Always accepts
        result = step.validate("anything")
        assert result.ok is True
    
    def test_step_with_validator(self):
        def email_validator(value: str) -> ValidationResult:
            if "@" in value:
                return ValidationResult(ok=True)
            return ValidationResult(ok=False, error="No @ sign")
        
        step = Step("email", "Email?", validator=email_validator)
        
        # Valid input
        result = step.validate("test@example.com")
        assert result.ok is True
        
        # Invalid input
        result = step.validate("invalid")
        assert result.ok is False
        assert result.error == "No @ sign"


class MockSessionManager:
    """Mock session manager for testing."""
    
    def __init__(self):
        self.data = {}
    
    async def get(self, chat_id: int, key: str):
        return self.data.get((chat_id, key))
    
    async def set(self, chat_id: int, key: str, value):
        self.data[(chat_id, key)] = value
    
    async def delete(self, chat_id: int, key: str):
        self.data.pop((chat_id, key), None)


class TestFormWorkflow:
    """Test FormWorkflow."""
    
    @pytest.mark.asyncio
    async def test_workflow_progression(self):
        steps = [
            Step("name", "Name?"),
            Step("email", "Email?"),
            Step("age", "Age?"),
        ]
        
        workflow = FormWorkflow(steps)
        session = MockSessionManager()
        chat_id = 123
        
        # Start at step 0
        step = await workflow.get_step_async(chat_id, session)
        assert step.key == "name"
        
        # Advance to step 1
        result = await workflow.validate_and_advance(chat_id, session, "John")
        assert result.ok is True
        
        step = await workflow.get_step_async(chat_id, session)
        assert step.key == "email"
        
        # Advance to step 2
        result = await workflow.validate_and_advance(chat_id, session, "john@example.com")
        assert result.ok is True
        
        step = await workflow.get_step_async(chat_id, session)
        assert step.key == "age"
        
        # Complete workflow
        result = await workflow.validate_and_advance(chat_id, session, "25")
        assert result.ok is True
        
        # No more steps
        step = await workflow.get_step_async(chat_id, session)
        assert step is None
        
        # Form is complete
        assert await workflow.is_complete_async(chat_id, session) is True
    
    @pytest.mark.asyncio
    async def test_validation_failure_doesnt_advance(self):
        def age_validator(value: str) -> ValidationResult:
            try:
                age = int(value)
                if age < 18:
                    return ValidationResult(ok=False, error="Must be 18+")
                return ValidationResult(ok=True)
            except ValueError:
                return ValidationResult(ok=False, error="Must be a number")
        
        steps = [
            Step("name", "Name?"),
            Step("age", "Age?", validator=age_validator),
        ]
        
        workflow = FormWorkflow(steps)
        session = MockSessionManager()
        chat_id = 123
        
        # Complete first step
        result = await workflow.validate_and_advance(chat_id, session, "John")
        assert result.ok is True
        
        # Try invalid age
        step = await workflow.get_step_async(chat_id, session)
        assert step.key == "age"
        
        result = await workflow.validate_and_advance(chat_id, session, "15")
        assert result.ok is False
        assert result.error == "Must be 18+"
        
        # Still on age step
        step = await workflow.get_step_async(chat_id, session)
        assert step.key == "age"
        
        # Try valid age
        result = await workflow.validate_and_advance(chat_id, session, "25")
        assert result.ok is True
        
        # Workflow complete
        assert await workflow.is_complete_async(chat_id, session) is True
    
    @pytest.mark.asyncio
    async def test_collect_data(self):
        steps = [
            Step("name", "Name?"),
            Step("email", "Email?"),
        ]
        
        workflow = FormWorkflow(steps)
        session = MockSessionManager()
        chat_id = 123
        
        # Complete workflow
        await workflow.validate_and_advance(chat_id, session, "John")
        await workflow.validate_and_advance(chat_id, session, "john@example.com")
        
        # Collect data
        data = await workflow.get_collected_data(chat_id, session)
        
        assert data["name"] == "John"
        assert data["email"] == "john@example.com"
    
    @pytest.mark.asyncio
    async def test_reset_workflow(self):
        steps = [
            Step("name", "Name?"),
            Step("email", "Email?"),
        ]
        
        workflow = FormWorkflow(steps)
        session = MockSessionManager()
        chat_id = 123
        
        # Complete workflow
        await workflow.validate_and_advance(chat_id, session, "John")
        await workflow.validate_and_advance(chat_id, session, "john@example.com")
        
        # Check complete
        assert await workflow.is_complete_async(chat_id, session) is True
        
        # Reset
        await workflow.reset(chat_id, session)
        
        # Back to first step
        step = await workflow.get_step_async(chat_id, session)
        assert step.key == "name"
        
        # Data is cleared
        data = await workflow.get_collected_data(chat_id, session)
        assert len(data) == 0
