from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class DialogRole(str, Enum):
    """Types of text that can be used in DialogRow: who said the text."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class DialogRow(BaseModel):
    """A row of text along with who said it."""
    role: DialogRole
    text: str
    created_at: datetime = Field(default_factory=datetime.now)

class Dialog(BaseModel):
    """A conversation between a user and assistant."""
    rows: List[DialogRow]
