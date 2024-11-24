from collections import deque
from typing import List
import unittest

from arclib.core import (
    AgentSystem,
    AgentSystemEvent,
    AgentSystemEventType,
    TaskAssignment,
    TaskContext,
    TaskSource,
    TaskStep
)
from arclib.dataproviders import BlobSessionStorageProvider
from arclib.infra.blob import MemoryBlobProvider
from arclib.models import DialogRole
from .mocks.mock_llm import MockLlmDriver


# The entirety of the "business logic" to do our task is between these lines.
#---
class BrainstormTask(TaskStep):
    def execute(self, context: TaskContext):
        emotion = context.session.app_context['feeling']
        context.session.dialog.add_user(f'brainstorm({emotion})')
        context.llm.chat_dialog(context.session.dialog)

class RefineTask(TaskStep):
    def execute(self, context: TaskContext):
        context.session.dialog.add_user('refine')

class WriteTask(TaskStep):
    def execute(self, context: TaskContext):
        context.session.dialog.add_user('write')

class EncouragementTaskSource(TaskSource):
    """Creates tasks to provide encouragement given a state of mind.
    """
    def __init__(self, states_of_mind: List[str]):
        self.states_of_mind = deque(states_of_mind) # We can pop off the left, and this keeps states_of_mind intact.

    def get_task(self):
        if not self.states_of_mind: # Stop if there is nothing left to do.
            return None
        state_of_mind = self.states_of_mind.popleft()
        assignment = TaskAssignment(
            app_context={'feeling': state_of_mind},
            steps=[
                BrainstormTask(),
                RefineTask(),
                WriteTask(),
            ]
        )
        return assignment
#---

class TestAgentSystem(unittest.TestCase):
    diagnostic_output = False
    diagnostic_output = True

    def setUp(self):
        self.blob = MemoryBlobProvider()
        self.session_storage = BlobSessionStorageProvider(self.blob)
        self.llm = MockLlmDriver()
    
    def test_basic_task(self):
        """We can complete a basic task consisting of two steps."""
        # Arrange.
        input_feelings = ['apathetic', 'discouraged']
        task_sources = [EncouragementTaskSource(input_feelings)]
        agent_system = AgentSystem(task_sources, self.llm, self.session_storage)

        started_events: List[AgentSystemEvent] = [] # These are to make sure we saw the events we expected.
        finished_events: List[AgentSystemEvent] = []

        def on_started(event: AgentSystemEvent):
            started_events.append(event)

        def on_finished(event: AgentSystemEvent):
            finished_events.append(event)

        agent_system.add_event(AgentSystemEventType.TASK_STARTED, on_started)
        agent_system.add_event(AgentSystemEventType.TASK_FINISHED, on_finished)

        # Act.
        agent_system.run()

        # Assert.
        session_blobs = self.blob.find()
        self.assertEqual(len(input_feelings), len(session_blobs), 'Should be one session for each of our tasks')
        self.assertEqual(len(input_feelings), len(started_events), 'We should have received started events for all our tasks.')
        self.assertEqual(len(input_feelings), len(finished_events), 'We should have received finished events for all our tasks.')

        for finished_event, feeling in zip(finished_events, input_feelings):
            session_id = finished_event.session.id
            # Although we can access the session directly from the event, verify we can get it from storage.
            session = self.session_storage.load_session(session_id)

            if self.diagnostic_output:
                print(f'for {feeling}: {session.dialog.as_tuples()}')
                # for apathetic: [('user', 'brainstorm(apathetic)'), ('assistant', 'response(brainstorm(apathetic))'), ('user', 'refine'), ('assistant', 'response(refine)'), ('user', 'write'), ('assistant', 'response(write)')]
                # for discouraged: [('user', 'brainstorm(discouraged)'), ('assistant', 'response(brainstorm(discouraged))'), ('user', 'refine'), ('assistant', 'response(refine)'), ('user', 'write'), ('assistant', 'response(write)')]                
            self.assertEqual(feeling, session.app_context['feeling'], f'This should be the session to discuss {feeling}')
            brainstorm_ask = session.dialog.rows[0]
            brainstorm_resp = session.dialog.rows[1]
            refine_ask = session.dialog.rows[2]
            refine_resp = session.dialog.rows[3]
            write_ask = session.dialog.rows[4]
            write_resp = session.dialog.rows[5]
            self.assertEqual(f'brainstorm({feeling})', brainstorm_ask.text, 'discussion from the Brainstorm step')
            self.assertEqual(f'response(brainstorm({feeling}))', brainstorm_resp.text, 'Response to brainstorm step')
            self.assertEqual(f'refine', refine_ask.text, 'discussion from the Refine step')
            self.assertEqual(f'write', write_ask.text, 'discussion from the Write step')
            self.assertEqual(DialogRole.USER, brainstorm_ask.role, 'This is something we said, not the LLM')
            self.assertEqual(DialogRole.ASSISTANT, brainstorm_resp.role, 'This is something the LLM said')
