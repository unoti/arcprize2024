from arclib.models.config import ArclibConfig
from arclib.llm import LlmDriver, OpenAiLlmDriver


def get_config() -> ArclibConfig:
    with open('local/config/config.json', 'r') as file:
        content = file.read()
    config = ArclibConfig.model_validate_json(content)
    return config

def get_llm() -> LlmDriver:
    cfg = get_config().openai
    llm = OpenAiLlmDriver(cfg.model, cfg.api_key, cfg.optional_config)
    return llm