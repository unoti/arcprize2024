from dataclasses import dataclass
from typing import Dict, Any, List, Callable

from ..dataproviders import SessionStorageProvider
from ..llm import LlmDriver
from ..models import Session, Dialog, DialogRow, DialogRole
from . import TaskContext, TaskAssignment

class Agent:
    """Completes an input task using language models, code, and tools.
    """
    def __init__(self,
                 task_assignment: TaskAssignment, # Instructions about what we must do. Steps, app_context.
                 llm: LlmDriver, # For talking with an LLM.
                 session_storage: SessionStorageProvider, # Saves sessions.
                 on_started: Callable[[Session, TaskAssignment], None], # We call this when we start work.
                 on_finished: Callable[[Session, TaskAssignment], None], # We call this when we finish work.
                 ):
        self.task_assignment = task_assignment
        self.llm = llm
        self.session_storage = session_storage
        self.steps = task_assignment.steps
        dialog = Dialog(rows=[])
        self.session = Session(dialog=dialog, app_context=task_assignment.app_context)
        self._on_started = on_started
        self._on_finished = on_finished

    def run(self):
        """Run the task to completion."""
        self._on_started(self.session, self.task_assignment)
        task_context = TaskContext(session=self.session, llm=self.llm)
        for step in self.steps:
            step.execute(task_context)

            # If the last thing said from the dialog was from a user then invoke to LLM to get it to respond to that.
            if self.session.dialog.rows:
                last_row = self.session.dialog.rows[-1]
                if last_row.role == DialogRole.USER:
                    row = self.llm.chat_dialog(self.session.dialog)
                    self.session.dialog.rows.append(row)

            self.session_storage.save_session(self.session)
        self._on_finished(self.session, self.task_assignment)
