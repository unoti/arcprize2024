from typing import Optional

from arclib.core import AgentSystem
from arclib.models.config import ArclibConfig
from arclib.llm import LlmDriver, OpenAiLlmDriver, MockLlmDriver
from arcprize import ArcRunner
from .arc_tasks import all_arc_task_classes

class ArcBuilder:
    def __init__(self):
        self.first_n: Optional[int] = None
        self.mock_llm = False
        self.verbose = True
        self.config: ArclibConfig = None

    def llm_mock(self, mock: bool = True) -> 'ArcBuilder':
        """Use a mock llm."""
        self.mock_llm = mock
        return self

    def show_output(self, show: bool = True) -> 'ArcBuilder':
        self.verbose = show
        return self

    def get_llm(self) -> LlmDriver:
        if self.mock_llm:
            return MockLlmDriver()
        cfg = self.get_config().openai
        llm = OpenAiLlmDriver(cfg.model, cfg.api_key, cfg.optional_config)
        return llm

    def get_agent_system(self) -> AgentSystem:
        llm = self.get_llm()

    def get_config(self) -> ArclibConfig:
        if self.config is None:
            with open('local/config/config.json', 'r') as file:
                content = file.read()
            self.config = ArclibConfig.model_validate_json(content)
        return self.config

    def build(self) -> ArcRunner:
        runner = ArcRunner(verbose=self.verbose)
        return runner
