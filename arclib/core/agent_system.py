from typing import Callable, Dict, Optional, List

from . import Agent, TaskAssignment, TaskSource, TaskStep
from ..dataproviders import SessionStorageProvider
from ..llm import LlmDriver
from ..models import Session
from .agent_events import AgentSystemEventType, AgentSystemEvent


EventCallback = Callable[[AgentSystemEvent], None]

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
        self._callbacks_by_type: Dict[List[EventCallback]] = {}

    def add_event(self, event_type: AgentSystemEventType, callback: EventCallback):
        """Register a callback to notify us as work is started or concluded.
        """
        callback_list = self._callbacks_by_type.get(event_type)
        if not callback_list:
            callback_list = []
            self._callbacks_by_type[event_type] = callback_list
        callback_list.append(callback)

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

    def _fire_event(self, event: AgentSystemEvent):
        for callback in self._callbacks_by_type.get(event.event_type, []):
            callback(event)

    def _run_task(self, task_assignment: TaskAssignment):
        agent = Agent(
            task_assignment=task_assignment,
            llm=self._llm,
            session_storage=self._session_storage,
            on_event=self._fire_event
            )
        agent.run()
