from typing import Dict, List
import unittest

from arcprize import ArcBuilder
from arclib.infra.blob import BlobProvider
from arclib.models import Session
from arclib.core import AgentSystemEvent, AgentSystemEventType
from arcprize.arc_tasks import all_arc_task_classes


class TestArcRunner(unittest.TestCase):
    case_count = 2
    diagnostic_output = False
    #diagnostic_output = True

    def setUp(self):
        self.builder = ArcBuilder()\
            .with_llm_mock()\
            .with_stdout(self.diagnostic_output)\
            .with_session_dir('')\
            .with_filesystem_mock()\
            .with_first_n(self.case_count)
        self.runner = self.builder.build()
        self.session_storage = self.runner.agent_system._session_storage
        self.session_blob: BlobProvider = self.session_storage.blob_provider
        self.events_by_type: Dict[AgentSystemEventType, List[AgentSystemEvent]] = {}
        self.runner.agent_system.add_all_events(self._on_event)

    def test_runner(self):
        """Verify the basic operation of ArcRunner."""
        # Act.
        self.runner.run()

        # Assert.
        session_filenames = self.session_blob.find('sessions/')
        self.assertEqual(len(session_filenames), self.case_count, 'There should be some sessions!')

        sessions_by_id: Dict[str, Session] = {}
        for filename in session_filenames:
            content = self.session_blob.load(filename)
            session = Session.from_json(content)
            case_id = session.app_context['case_id']
            sessions_by_id[case_id] = session

        transcript_filenames = self.session_blob.find('transcripts/')
        self.assertEqual(len(transcript_filenames), self.case_count, 'There should be one transcript per session')
        for filename in transcript_filenames:
            transcript_md = self.session_blob.load(filename)
            if self.diagnostic_output:
                print(transcript_md)
                print('---')

        # Make sure we got all the events.
        step_count = len(all_arc_task_classes)
        for event_type in [AgentSystemEventType.TASK_STARTED, AgentSystemEventType.TASK_FINISHED]:
            events_received = self.events_by_type[event_type]
            self.assertEqual(self.case_count, len(events_received), f'We should have received one {event_type.value} event per case')
        for event_type in [AgentSystemEventType.STEP_STARTED, AgentSystemEventType.STEP_FINISHED]:
            events_received = self.events_by_type[event_type]
            self.assertEqual(self.case_count * step_count, len(events_received), f'We should have received one {event_type.value} event per step per case')

    def _on_event(self, event: AgentSystemEvent):
        event_list = self.events_by_type.get(event.event_type)
        if event_list is None:
            event_list = []
            self.events_by_type[event.event_type] = event_list
        event_list.append(event)
