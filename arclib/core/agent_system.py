from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, List

from . import Agent, TaskAssignment, TaskSource
from ..dataproviders import SessionStorageProvider
from ..llm import LlmDriver
from ..models import Session


class AgentSystemEventType(Enum):
    TASK_STARTED = 'task_started'
    TASK_FINISHED = 'task_finished'


@dataclass
class AgentSystemEvent:
    event_type: AgentSystemEventType
    session: Session
    task_assignment: TaskAssignment


class AgentSystem:
    """Works on tasks provided by TaskSources.
    """
    def __init__(self,
                 task_sources: List[TaskSource],
                 llm: LlmDriver,
                 session_storage: SessionStorageProvider):
        self._task_sources = task_sources
        self._llm = llm
        self._session_storage = session_storage
        self._on_started: List[Callable[[AgentSystemEvent], None]] = []
        self._on_finished: List[Callable[[AgentSystemEvent], None]] = []

    def add_event(self, event_type: AgentSystemEventType, callback: Callable[[AgentSystemEvent], None]):
        """Register a callback to notify us as work is started or concluded.
        """
        if event_type == AgentSystemEventType.TASK_STARTED:
            self._on_started.append(callback)
        elif event_type == AgentSystemEventType.TASK_FINISHED:
            self._on_finished.append(callback)
        else:
            raise ValueError(f'Invalid event type {event_type}')

    def run(self):
        """Consume from task sources and work on tasks.
        
        Runs until all task sources are exhausted.
        Later we might change this to indicate that some task sources need to be periodically
        checked even when they indicate that there are no more tasks to do.
        """
        while True:
            task_assignment = self._get_task()
            if not task_assignment:
                break
            self._run_task(task_assignment)

    def _get_task(self) -> Optional[TaskAssignment]:
        for task_source in self._task_sources:
            task_assignment = task_source.get_task()
            if task_assignment:
                return task_assignment
        return None

    def _agent_started(self, session: Session, task_assignment: TaskAssignment):
        """Agent calls this when it starts work."""
        event = AgentSystemEvent(AgentSystemEventType.TASK_STARTED, session, task_assignment)
        self._fire_event(event, self._on_started)

    def _agent_finished(self, session: Session, task_assignment: TaskAssignment):
        """Agent calls this when it finishes work."""
        event = AgentSystemEvent(AgentSystemEventType.TASK_FINISHED, session, task_assignment)
        self._fire_event(event, self._on_finished)

    def _fire_event(self, event: AgentSystemEvent, callbacks: Callable[[AgentSystemEvent], None]):
        for callback in callbacks:
            callback(event)

    def _run_task(self, task_assignment: TaskAssignment):
        agent = Agent(
            task_assignment=task_assignment,
            llm=self._llm,
            session_storage=self._session_storage,
            on_started=self._agent_started,
            on_finished=self._agent_finished,
            )
        agent.run()
