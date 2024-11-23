from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, Field

from .dialog import Dialog

class Session(BaseModel):
    """A session with a discussion between a user and assistant, including metadata."""
    created_at: datetime = Field(default_factory=datetime.now)
    dialog: Dialog
    app_context: Dict[str, Any] = Field(default_factory=dict) # Application-specific structured data.

    def to_json(self) -> str:
        """Serialize the session to a JSON string."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str) -> "Session":
        """Deserialize the session from a JSON string to a Session instance."""
        return cls.model_validate_json(json_str)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the session to a Python dict."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        """Deserialize the session from a Python dict to a Session object."""
        return cls(**data)
