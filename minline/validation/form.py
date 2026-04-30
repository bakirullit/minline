"""Form - optional orchestration layer for multi-step Questions."""

from typing import List, Optional
from minline.core import Question
from minline.session import SessionManager
import json


class Form:
    """
    Multi-step form orchestrator.
    
    NOT core - just chains Questions together.
    Questions are the primitives. Forms coordinate them.
    """
    
    def __init__(self, id: str, questions: List[Question]):
        """
        Initialize Form.
        
        Args:
            id: Form identifier
            questions: Ordered list of Questions
        """
        self.id = id
        self.questions = questions
        self.question_map = {q.id: q for q in questions}
    
    async def get_current_question_async(self, chat_id: int, session: SessionManager) -> Optional[Question]:
        """Get current question for user."""
        step = await session.get(chat_id, f"form:{self.id}:step")
        if step is None:
            # First question
            return self.questions[0] if self.questions else None
        
        try:
            step_idx = int(step)
            if 0 <= step_idx < len(self.questions):
                return self.questions[step_idx]
        except (ValueError, IndexError):
            pass
        
        return None
    
    async def next_question_async(self, chat_id: int, session: SessionManager) -> Optional[Question]:
        """Get next question (advance step counter)."""
        current_step = await session.get(chat_id, f"form:{self.id}:step")
        
        if current_step is None:
            step_idx = 1
        else:
            step_idx = int(current_step) + 1
        
        if step_idx < len(self.questions):
            await session.set(chat_id, f"form:{self.id}:step", str(step_idx))
            return self.questions[step_idx]
        
        return None
    
    async def answer_question_async(
        self, chat_id: int, session: SessionManager, question_id: str, value: any
    ):
        """Store answer for question."""
        if question_id not in self.question_map:
            raise ValueError(f"Unknown question: {question_id}")
        
        answers_json = await session.get(chat_id, f"form:{self.id}:answers")
        answers = json.loads(answers_json) if answers_json else {}
        
        answers[question_id] = value
        await session.set(chat_id, f"form:{self.id}:answers", json.dumps(answers))
    
    async def is_complete_async(self, chat_id: int, session: SessionManager) -> bool:
        """Check if all questions answered."""
        step = await session.get(chat_id, f"form:{self.id}:step")
        
        if step is None:
            return False
        
        try:
            step_idx = int(step)
            return step_idx >= len(self.questions)
        except ValueError:
            return False
    
    async def get_answers_async(self, chat_id: int, session: SessionManager) -> dict:
        """Get all collected answers."""
        answers_json = await session.get(chat_id, f"form:{self.id}:answers")
        return json.loads(answers_json) if answers_json else {}
    
    async def reset_async(self, chat_id: int, session: SessionManager):
        """Reset form state."""
        await session.delete(chat_id, f"form:{self.id}:step")
        await session.delete(chat_id, f"form:{self.id}:answers")
