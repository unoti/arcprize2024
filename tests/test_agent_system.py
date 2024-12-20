from typing import Dict, List
import unittest

from arclib.core import (
    AgentSystem,
    AgentSystemEvent,
    AgentSystemEventType,
    PromptStep,
    SequenceTaskSource,
    TaskSource,
)
from arclib.dataproviders import BlobSessionStorageProvider
from arclib.infra.blob import MemoryBlobProvider
from arclib.models import DialogRole
from arclib.llm import MockLlmDriver


# The entirety of the "business logic" to do our task is between these lines.
# The example task might be writing essays about an emotion.
input_feelings = ['excited', 'curious']
#---
class BrainstormTask(PromptStep):
    """brainstorm({feeling})""" # This docstring is used as a prompt, and is formatted with app_context values.

class RefineTask(PromptStep):
    """refine""" # This docstring is used as a prompt, sent to the LLM, and the LLM responds.

class WriteTask(PromptStep):
    """write"""

def make_task_source() -> TaskSource:
    app_contexts = [{'feeling': feeling} for feeling in input_feelings]
    return SequenceTaskSource(app_contexts, [BrainstormTask, RefineTask, WriteTask])
#---

class TestAgentSystem(unittest.TestCase):
    diagnostic_output = False
    #diagnostic_output = True

    def setUp(self):
        self.blob = MemoryBlobProvider()
        self.session_storage = BlobSessionStorageProvider(self.blob, dir_prefix='')
        self.llm = MockLlmDriver()
    
    def test_basic_task(self):
        """We can complete a basic task consisting of two steps."""
        # Arrange.
        task_sources = [make_task_source()]
        agent_system = AgentSystem(task_sources, self.llm, self.session_storage)

        events_by_type: Dict[AgentSystemEventType, List[AgentSystemEvent]] = {}

        def on_event_received(event: AgentSystemEvent):
            event_list = events_by_type.get(event.event_type)
            if not event_list:
                event_list = []
                events_by_type[event.event_type] = event_list
            event_list.append(event)
                
        agent_system.add_event(AgentSystemEventType.TASK_STARTED, on_event_received)
        agent_system.add_event(AgentSystemEventType.TASK_FINISHED, on_event_received)
        agent_system.add_event(AgentSystemEventType.STEP_STARTED, on_event_received)
        agent_system.add_event(AgentSystemEventType.STEP_FINISHED, on_event_received)

        # Act.
        agent_system.run()

        # Assert.
        started_events = events_by_type[AgentSystemEventType.TASK_STARTED]
        finished_events = events_by_type[AgentSystemEventType.TASK_FINISHED]
        session_blobs = self.blob.find('sessions/')
        self.assertEqual(len(input_feelings), len(session_blobs), 'Should be one session for each of our tasks')
        self.assertEqual(len(input_feelings), len(started_events), 'We should have received started events for all our tasks.')
        self.assertEqual(len(input_feelings), len(finished_events), 'We should have received finished events for all our tasks.')

        for finished_event, feeling in zip(finished_events, input_feelings):
            session_id = finished_event.session.id
            # Although we can access the session directly from the event, verify we can get it from storage.
            session = self.session_storage.load_session(session_id)

            if self.diagnostic_output:
                print(f'for {feeling}: {session.dialog.as_tuples()}')
                # for excited: [('user', 'brainstorm(excited)'), ('assistant', 'response(brainstorm(excited))'), ('user', 'refine'), ('assistant', 'response(refine)'), ('user', 'write'), ('assistant', 'response(write)')]
                # for curious: [('user', 'brainstorm(curious)'), ('assistant', 'response(brainstorm(curious))'), ('user', 'refine'), ('assistant', 'response(refine)'), ('user', 'write'), ('assistant', 'response(write)')]                
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
            self.assertEqual(f'response(refine)', refine_resp.text, 'LLM should have responded to refine step.')
            self.assertEqual(f'write', write_ask.text, 'discussion from the Write step')
            self.assertEqual(f'response(write)', write_resp.text, 'LLM should have responded to write step.')
            self.assertEqual(DialogRole.USER, brainstorm_ask.role, 'This is something we said, not the LLM')
            self.assertEqual(DialogRole.ASSISTANT, brainstorm_resp.role, 'This is something the LLM said')
