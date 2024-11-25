from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Iterable, Type

from . import TaskStep


@dataclass
class TaskAssignment:
    steps: List[TaskStep]
    app_context: Dict[str, Any] # Structured information describing what we need to do.


class TaskSource(ABC):
    """A place where we get work assignments that need to be done.
    """
    @abstractmethod
    def get_task(self) -> Optional[TaskAssignment]:
        """Returns a task that needs to be done, or None if there is no work to do."""

class SequenceTaskSource(TaskSource):
    """A task source which takes a fixed-size input of app_context dicts.
    
    Example usage:
        ticket_ids = [123, 124, 125]
        app_contexts = [{'ticket_id': ticket_id} for ticket_id in ticket_ids]
        task_source = SequenceTaskSource(app_contexts, [MyTaskStep1, MyTaskStep2])

    See also test_agent_system for an additional usage example.
    """
    def __init__(self,
                 app_context_items: Iterable[Dict[str, Any]],
                 task_step_classes: List[Type[TaskStep]]
                 ):
        self.items = deque(app_context_items) # So we can efficiently pop left, and copies to preserve the input items.
        self.task_step_classes = task_step_classes

    def get_task(self) -> Optional[TaskAssignment]:
        if len(self.items) == 0:
            return None
        app_context = self.items.popleft()
        task_steps = [step_class() for step_class in self.task_step_classes] # Create instances from our classes.
        assignment = TaskAssignment(task_steps, app_context)
        return assignment

