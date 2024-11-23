from datetime import datetime
from enum import Enum
from typing import List, Tuple
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

    def as_tuples(self) -> List[Tuple[str, str]]:
        """Returns this dialog as a list of tuples of [role, text].
        
        This is a typical mode of input for LLM's.
        """
        return [(row.role.value, row.text) for row in self.rows]
