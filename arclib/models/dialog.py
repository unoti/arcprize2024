from datetime import datetime
from enum import Enum
from typing import Optional, List, Tuple
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
    rows: List[DialogRow] = Field(default_factory=list)

    def as_tuples(self, role: Optional[DialogRole] = None) -> List[Tuple[str, str]]:
        """Returns this dialog as a list of tuples of [role, text].
        
        This is a typical mode of input for LLM's.
        :param role: If specified, limit the output to the given role.
        """
        if role is None:
            return [(row.role.value, row.text) for row in self.rows]
        return [(row.role.value, row.text) for row in self.rows if row.role == role]

    def add(self, role: DialogRole, text: str):
        """Add a row of dialog."""
        row = DialogRow(role=role, text=text)
        self.rows.append(row)

    def add_user(self, text: str):
        """Add a row of user content."""
        self.add(role=DialogRole.USER, text=text)
