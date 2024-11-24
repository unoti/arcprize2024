from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

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
        ...
        #app_context
        #steps
        
