from typing import Dict
import unittest

from arcprize import ArcBuilder
from arclib.infra.blob import BlobProvider
from arclib.models import Session


class TestArcRunner(unittest.TestCase):
    case_count = 2
    diagnostic_output = False
    #diagnostic_output = True

    def setUp(self):
        self.builder = ArcBuilder()\
            .with_llm_mock()\
            .with_stdout(self.diagnostic_output)\
            .with_session_dir('')\
            .with_first_n(self.case_count)
        self.runner = self.builder.build()
        self.session_storage = self.runner.agent_system._session_storage
        self.session_blob: BlobProvider = self.session_storage.blob_provider  
        
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
            session = sessions_by_id
            if self.diagnostic_output:
                print(transcript_md)
                print('---')
