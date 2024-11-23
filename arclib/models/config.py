from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class OpenAiConfig(BaseModel):
    """Options for configuring OpenAI"""
    model: str # Model name, e.g. 'gpt-4o'
    api_key: str
    optional_config: Optional[Dict[str, Any]] # Configuration dict including temperature and other parameters for openai.

class ArclibConfig(BaseModel):
    """Options for configuring this application."""
    openai: OpenAiConfig

