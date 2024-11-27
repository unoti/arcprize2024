from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..llm import LlmDriver
from ..models import Session, DialogRole
from ..infra.string import dedent


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

    def condition(self, context: TaskContext) -> bool:
        """Execute this step only if this condition returns True."""
        return True

    # Dynamic plan updates:
    # def set_next_step()... we could have methods here on TaskStep that let us dynamically change the plan.
    # either in terms of a "replace remaining plan" or "take this side trip" kind of way...


class PromptStep(TaskStep):
    """A TaskStep which contains a prompt in its docstring and gives the assistant a chance to respond.

    See test_agent_system.py for example usage.
    """
    role = DialogRole.USER # Subclasses can change this, or you can use SystemPromptStep for brevity.

    def execute(self, context: TaskContext):
        prompt_str = dedent(self.__doc__)
        vars = self.prompt_variables(context)
        if vars:
            prompt_str = prompt_str.format(**vars)
        context.session.dialog.add(self.role, prompt_str)

    def prompt_variables(self, context: TaskContext) -> Optional[dict]:
        """You may override this to return a dict of variables to substitute in the docstring.
        
        By default we use all the variables in app_context. You may override this to change their
        names or to disable templating on the docstring.
        """
        return context.session.app_context

class SystemPromptStep(PromptStep):
    """Like PromptStep, except its output goes to the role SYSTEM instead of USER."""
    role = DialogRole.SYSTEM