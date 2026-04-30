"""InputEvent normalization - all Telegram inputs converted to unified format."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class InputEvent:
    """
    Normalized input event from user.
    
    Core decoupling: Telegram message structure → opaque InputEvent
    Framework never depends on message structure directly.
    """
    
    type: str  # "text", "photo", "audio", "document", "callback", "link", "number"
    value: Any  # The actual input value
    meta: dict = field(default_factory=dict)  # Telegram metadata (user_id, chat_id, etc)
    
    @staticmethod
    def from_text(text: str, chat_id: int, user_id: int) -> "InputEvent":
        """Create InputEvent from text message."""
        return InputEvent(
            type="text",
            value=text,
            meta={"chat_id": chat_id, "user_id": user_id}
        )
    
    @staticmethod
    def from_number(value: int, chat_id: int, user_id: int) -> "InputEvent":
        """Create InputEvent from numeric input (single_choice)."""
        return InputEvent(
            type="number",
            value=value,
            meta={"chat_id": chat_id, "user_id": user_id}
        )
    
    @staticmethod
    def from_callback(data: str, chat_id: int, user_id: int) -> "InputEvent":
        """Create InputEvent from callback button press."""
        return InputEvent(
            type="callback",
            value=data,
            meta={"chat_id": chat_id, "user_id": user_id}
        )
    
    @staticmethod
    def from_photo(file_id: str, chat_id: int, user_id: int, caption: Optional[str] = None) -> "InputEvent":
        """Create InputEvent from photo."""
        return InputEvent(
            type="photo",
            value=file_id,
            meta={"chat_id": chat_id, "user_id": user_id, "caption": caption}
        )
    
    @staticmethod
    def from_document(file_id: str, chat_id: int, user_id: int, filename: Optional[str] = None) -> "InputEvent":
        """Create InputEvent from document."""
        return InputEvent(
            type="document",
            value=file_id,
            meta={"chat_id": chat_id, "user_id": user_id, "filename": filename}
        )
    
    def get_chat_id(self) -> int:
        """Extract chat_id from metadata."""
        return self.meta.get("chat_id")
    
    def get_user_id(self) -> int:
        """Extract user_id from metadata."""
        return self.meta.get("user_id")
