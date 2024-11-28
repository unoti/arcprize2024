from typing import Type, List, Dict

from openai import OpenAI
from pydantic import BaseModel

from .llm_driver import LlmDriver
from ..models import Dialog, DialogRole, DialogRow, DialogMetaData


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

    def _get_messages(self, dialog: Dialog) -> List[Dict[str, str]]:
        return [{'role': role, 'content': text} for role, text in dialog.as_tuples()]
    
    def chat_dialog(self, dialog: Dialog) -> DialogRow:
        messages = self._get_messages(dialog)
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            **self._optional_config,
        )
        row = DialogRow(role=DialogRole.ASSISTANT, text=completion.choices[0].message.content)
        return row

    def chat_structured(self, dialog: Dialog, response_class: Type[BaseModel]):
        # See https://openai.com/index/introducing-structured-outputs-in-the-api/
        messages = self._get_messages(dialog)
        completion = self._client.beta.chat.completions.parse(
            model=self._model,
            messages=messages,
            response_format=response_class,
            **self._optional_config,
        )
        message = completion.choices[0].message
        if message.parsed:
            result_dict = message.parsed
            meta = DialogMetaData(structured_result_class=response_class.__name__,
                                  structured_result=result_dict)
            row = DialogRow(role=DialogRole.ASSISTANT,
                            text='',
                            metadata=meta)
        else:
            text = message.refusal
            row = DialogRow(role=DialogRole.ASSISTANT, text=text)
        return row