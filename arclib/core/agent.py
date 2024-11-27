from typing import Callable, Optional

from ..dataproviders import SessionStorageProvider
from ..llm import LlmDriver
from ..models import Session, Dialog, DialogRole
from . import TaskContext, TaskAssignment, TaskStep, AgentSystemEvent, AgentSystemEventType

class Agent:
    """Completes an input task using language models, code, and tools.
    """
    def __init__(self,
                 task_assignment: TaskAssignment, # Instructions about what we must do. Steps, app_context.
                 llm: LlmDriver, # For talking with an LLM.
                 session_storage: SessionStorageProvider, # Saves sessions.
                 on_event: Callable[[AgentSystemEvent], None], # Agent will send events here.
                 ):
        self.task_assignment = task_assignment
        self.llm = llm
        self.session_storage = session_storage
        self.steps = task_assignment.steps
        dialog = Dialog(rows=[])
        self.session = Session(dialog=dialog, app_context=task_assignment.app_context)
        self._on_event = on_event

    def run(self):
        """Run the task to completion."""
        self._fire_event(AgentSystemEventType.TASK_STARTED)
        task_context = TaskContext(session=self.session, llm=self.llm)
        for step in self.steps:
            if not step.condition(task_context):
                self._fire_event(AgentSystemEventType.STEP_FINISHED, step)
                continue
            self._fire_event(AgentSystemEventType.STEP_STARTED, step)
            step.execute(task_context)

            # If the last thing said from the dialog was from a user then invoke to LLM to get it to respond to that.
            if self.session.dialog.rows:
                last_row = self.session.dialog.rows[-1]
                if last_row.role == DialogRole.USER:
                    row = self.llm.chat_dialog(self.session.dialog)
                    self.session.dialog.rows.append(row)

            self.session_storage.save_session(self.session)
            self._fire_event(AgentSystemEventType.STEP_FINISHED, step)
        self._fire_event(AgentSystemEventType.TASK_FINISHED)

    def _fire_event(self, event_type: AgentSystemEventType, step: Optional[TaskStep]=None):
        event = AgentSystemEvent(event_type, self.session, self.task_assignment, step)
        self._on_event(event)
