from .models.config import ArclibConfig
from .llm import LlmDriver, OpenAiLlmDriver

class ArcApplication:
    def __init__(self, config: ArclibConfig):
        self.config = config
        self._llm: LlmDriver = None

    def get_llm(self):
        if not self._llm:
            openai_cfg = self.config.openai
            self._llm = OpenAiLlmDriver(openai_cfg.model, openai_cfg.api_key, openai_cfg.optional_config)
        return self._llm

_app_singleton: ArcApplication = None

def get_app() -> ArcApplication:
    global _app_singleton
    if not _app_singleton:
        _app_singleton = ArcApplication(get_config())
    return _app_singleton

def get_config() -> ArclibConfig:
    with open('local/config/config.json', 'r') as file:
        content = file.read()
    config = ArclibConfig.model_validate_json(content)
    return config
