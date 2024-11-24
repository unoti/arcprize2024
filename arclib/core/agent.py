from dataclasses import dataclass
from typing import Dict, Any, List

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
                 ):
        self.task_assignment = task_assignment
        self.llm = llm
        self.session_storage = session_storage
        self.steps = task_assignment.steps
        dialog = Dialog(rows=[])
        self.session = Session(dialog=dialog, app_context=task_assignment.app_context)

    def run(self):
        """Run the task to completion."""
        task_context = TaskContext(session=self.session, llm=self.llm)
        for step in self.steps:
            step.execute(task_context)
            self.session_storage.save_session(self.session)
