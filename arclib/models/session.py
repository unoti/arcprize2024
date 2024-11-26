from datetime import datetime
import json
from pydantic import BaseModel, Field
from typing import Dict, Any, List

from .dialog import Dialog
from ..infra.string import random_string
    

class Session(BaseModel):
    """A session with a discussion between a user and assistant, including metadata."""
    id: str = Field(default_factory=random_string)
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

    def get_transcript(self) -> str:
        """Create a markdown-formatted transcript of this session.
        """
        out: List[str] = [f'# Transcript: Session {self.id}']
        if self.app_context:
            out.append('## app_context\n```json\n')
            # Not using indent because the formatting is bad for ARC cases.
            #out.append(json.dumps(self.app_context, indent=4))
            out.append(json.dumps(self.app_context))
            out.append('```\n')

        for row in self.dialog.rows:
            out.append(f'\n# {row.role.value.title}')
            out.append(row.text)
            out.append('')
        return '\n'.join(out)
