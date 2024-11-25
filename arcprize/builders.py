from typing import Optional
from arclib.models.config import ArclibConfig
from arclib.llm import LlmDriver, OpenAiLlmDriver
from arcprize import ArcRunner
from .arc_tasks import all_arc_task_classes


class ArcBuilder:
    def __init__(self):
        self.first_n: Optional[int] = None
        self.mock_llm = False
        self.verbose = True

    def llm_mock(self, mock: bool = True) -> 'ArcBuilder':
        """Use a mock llm."""
        self.mock_llm = mock
        return self

    def show_output(self, show: bool = True) -> 'ArcBuilder':
        self.verbose = show
        return self

    def build(self) -> ArcRunner:
        runner = ArcRunner(verbose=self.verbose)
        return runner


def get_config() -> ArclibConfig:
    with open('local/config/config.json', 'r') as file:
        content = file.read()
    config = ArclibConfig.model_validate_json(content)
    return config


def get_llm() -> LlmDriver:
    cfg = get_config().openai
    llm = OpenAiLlmDriver(cfg.model, cfg.api_key, cfg.optional_config)
    return llm