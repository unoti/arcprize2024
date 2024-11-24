from openai import OpenAI

from .llm_driver import LlmDriver
from ..models import Dialog, DialogRole, DialogRow


class OpenAiLlmDriver(LlmDriver):
    """An LlmDriver backed by OpenAI.
    """
    def __init__(self, model: str, api_key: str, optional_config: dict):
        """
        :param model: The name of the model, e.g. 'gpt-4o'
        :param api_key: API key string.
        :param optional_config: Optional settings such as temperature, etc.
        """
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self._optional_config = optional_config

    def chat_dialog(self, dialog: Dialog) -> DialogRow:
        messages = [{'role': role, 'content': text} for role, text in dialog.as_tuples()]
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            **self._optional_config,
        )
        row = DialogRow(role=DialogRole.ASSISTANT, text=completion.choices[0].message.content)
        return row
