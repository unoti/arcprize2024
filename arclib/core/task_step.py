from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..llm import LlmDriver
from ..models import Session


@dataclass
class TaskContext:
    """Information given to a TaskStep.
    
    This is here so that if we add new information here we don't need to update
    all TaskStep classes that exist.
    """
    session: Session
    llm: LlmDriver


class TaskStep(ABC):
    """Business logic needed to perform part of a task within an agent.
    
    An agent performs one or more steps to complete a task.
    """
    @abstractmethod
    def execute(self, context: TaskContext):
        """Execute the business logic to execute this step."""
    
    def update_app_context(self, section: str, name: str, value: str, schema_description: str):
        """Update the app_context in the session and include metadata describing what the information is."""
        raise NotImplementedError()
    
    # Dynamic plan updates:
    # def set_next_step()... we could have methods here on TaskStep that let us dynamically change the plan.
    # either in terms of a "replace remaining plan" or "take this side trip" kind of way...

