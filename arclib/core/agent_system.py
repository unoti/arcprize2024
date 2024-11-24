from typing import List

from . import TaskSource

class AgentSystem:
    def __init__(self, task_sources: List[TaskSource]):
        self.task_sources = task_sources