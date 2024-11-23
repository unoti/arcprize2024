from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel

# Define the DialogRole Enum
class DialogRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# Define the DialogRow model
class DialogRow(BaseModel):
    role: DialogRole
    text: str

    # Additional methods or properties can be added here later

# Define the Dialog model
class Dialog(BaseModel):
    started_at: datetime
    rows: List[DialogRow]

    # Additional methods or properties can be added here later

# Define the Session model
class Session(BaseModel):
    dialog: Dialog

    # Additional methods or properties can be added here later

# Example Usage
if __name__ == "__main__":
    # Create an example dialog
    example_dialog = Dialog(
        started_at=datetime.now(),
        rows=[
            DialogRow(role=DialogRole.USER, text="Hello!"),
            DialogRow(role=DialogRole.ASSISTANT, text="Hi there! How can I assist you today?"),
        ]
    )

    # Create a session with the dialog
    example_session = Session(dialog=example_dialog)

    # Serialize the session to JSON string
    session_json = example_session.json()
    print("Serialized JSON (string):", session_json)

    # Deserialize from JSON string back to a Session object
    deserialized_session = Session.parse_raw(session_json)
    print("Deserialized Session from JSON string:", deserialized_session)

    # Serialize the session to Python dict
    session_dict = example_session.dict()
    print("Serialized Python dict:", session_dict)

    # Deserialize from Python dict back to a Session object
    deserialized_session_from_dict = Session(**session_dict)
    print("Deserialized Session from Python dict:", deserialized_session_from_dict)
