from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


from ..models import Session
from .task_step import TaskStep
from .task_source import TaskAssignment


class AgentSystemEventType(Enum):
    TASK_STARTED = 'task_started'
    TASK_FINISHED = 'task_finished'
    STEP_STARTED = 'step_started'
    STEP_FINISHED = 'step_finished'
    STEP_SKIPPED = 'step_skipped' # When the condition on the step returns false.


@dataclass
class AgentSystemEvent:
    event_type: AgentSystemEventType
    session: Session
    task_assignment: TaskAssignment
    step: Optional[TaskStep] = None

