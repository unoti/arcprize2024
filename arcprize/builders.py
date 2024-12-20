from typing import List, Optional

from arclib.core import AgentSystem, TaskSource, SequenceTaskSource
from arclib.models.config import ArclibConfig
from arclib.infra.blob import BlobProvider, MemoryBlobProvider, FileSystemBlobProvider
from arclib.llm import LlmDriver, OpenAiLlmDriver, MockLlmDriver
from arclib.dataproviders import ArcCaseProvider, SessionStorageProvider, BlobSessionStorageProvider
from arcprize import ArcRunner
from arcprize.arc_tasks import all_arc_task_classes
from .arc_tasks import all_arc_task_classes


class ArcBuilder:
    def __init__(self):
        self.first_n: Optional[int] = None
        self.mock_llm = False
        self.verbose = True
        self.config: ArclibConfig = None
        self.session_dir:str = None # Relative directory prefix for outputting sessions and transcripts.
        self.filesystem_mock = False
        self.case_sequence_ids = None # When None, process all cases.
        self.case_ids = None # Only process the given case ids.

    def with_llm_mock(self, mock: bool = True) -> 'ArcBuilder':
        """Use a mock llm."""
        self.mock_llm = mock
        return self

    def with_stdout(self, show: bool = True) -> 'ArcBuilder':
        """Set whether we want to output to stdout while running."""
        self.verbose = show
        return self

    def with_first_n(self, count: int) -> 'ArcBuilder':
        """Limit our input to a certain number of cases."""
        self.first_n = count
        return self

    def with_session_dir(self, dir: str) -> 'ArcBuilder':
        self.session_dir = dir
        return self

    def with_filesystem_mock(self, filesystem_mock: bool = True) -> 'ArcBuilder':
        """Use an in-memory filesystem instead of the real filesystem."""
        self.filesystem_mock = filesystem_mock
        return self

    def with_sequence_ids(self, sequence_ids: List[int]) -> 'ArcBuilder':
        """Process only the cases given by the list of 1-based integers."""
        self.case_sequence_ids = sequence_ids
        return self

    def with_case_ids(self, case_ids: List[str]) -> 'ArcBuilder':
        self.case_ids = case_ids
        return self

    def get_llm(self) -> LlmDriver:
        if self.mock_llm:
            return MockLlmDriver()
        cfg = self.get_config().openai
        llm = OpenAiLlmDriver(cfg.model, cfg.api_key, cfg.optional_config)
        return llm

    def get_agent_system(self) -> AgentSystem:
        llm = self.get_llm()
        task_sources = self.get_task_sources()
        session_storage = self.get_session_storage()
        agent_system = AgentSystem(task_sources, llm, session_storage)
        return agent_system

    def get_session_blob_provider(self) -> BlobProvider:
        if self.filesystem_mock:
            blob = MemoryBlobProvider()
        else:
            blob = FileSystemBlobProvider('./')
        return blob

    def get_session_storage(self) -> SessionStorageProvider:
        blob = self.get_session_blob_provider()
        storage = BlobSessionStorageProvider(blob, dir_prefix=self.session_dir)
        return storage

    def get_case_provider(self) -> ArcCaseProvider:
        return ArcCaseProvider()

    def get_task_sources(self) -> List[TaskSource]:
        case_provider = self.get_case_provider()
        case_ids = case_provider.get_case_ids()
        if self.first_n:
            case_ids = case_ids[:self.first_n]
        if self.case_sequence_ids:
            all_case_ids = case_ids
            case_ids = [all_case_ids[i-1] for i in self.case_sequence_ids]
        if self.case_ids:
            case_ids = self.case_ids
        context_items = case_provider.get_app_contexts(case_ids)
        source = SequenceTaskSource(context_items, all_arc_task_classes)
        all_sources = [source]
        return all_sources

    def get_config(self) -> ArclibConfig:
        if self.config is None:
            with open('local/config/config.json', 'r') as file:
                content = file.read()
            self.config = ArclibConfig.model_validate_json(content)
        return self.config

    def build(self) -> ArcRunner:
        agent_system = self.get_agent_system()
        runner = ArcRunner(agent_system, verbose=self.verbose)
        return runner
