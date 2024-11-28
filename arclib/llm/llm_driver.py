from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from ..models import Dialog, DialogRow, DialogRole


class LlmDriver(ABC):
    """Abstract class for talking with an LLM.
    
    This is the lowest level driver, designed to be easy to implement
    if you want to interface to a new LLM.
    Although there are two methods here, to implement your own driver
    you only need to override chat_dialog().  The chat() method has
    default behavior defined here in terms of the required chat_dialog().
    """
    class InvalidRequestError(Exception):
        pass
    class RateLimitError(Exception):
        pass

    def chat(self, prompt: str) -> str:
        """Given an input prompt, respond.
        
        You can use this method when you don't need to continue a previous conversation
        and don't need fine-grained control over system role vs assistant role in the conversation.
        :param prompt: Text to start the conversation.
        :returns: The LLM's response that continues the conversation.
        """
        rows = [DialogRow(role=DialogRole.USER, text=prompt)]
        dialog = Dialog(rows=rows)
        result_row = self.chat_dialog(dialog)
        return result_row.text

    @abstractmethod
    def chat_dialog(self, dialog: Dialog) -> DialogRow:
        """Given a starting dialog, respond.

        Allows for continuation of conversations and fine-grained control of roles (system, user, agent).
        Note: The response DialogRow must not be added to the dialog within this method and must be done
        externally if desired.  We made the design decision that llm_driver does *not* append to the
        dialog but llm_provider *does*, because we want llm_driver to be as easy as possible to
        correctly implement.  Llm_driver does use Dialog and DialogRow as its inputs and outputs
        to make it possible to correctly structure inputs by who said what, and to enable it to
        reflect correct token counts in and out in the DialogRows.

        :param dialog: The discussion up to this point.
        :returns: The LLM's response that continues the conversation, as a DialogRow.
            Note that the LLM driver must also set the token counts on the dialog rows.
        """

    def chat_structured(self, dialog: Dialog, response_class: Type[BaseModel]) -> DialogRow:
        """Start a chat and expect a structure response in JSON

        The response will be placed in the output DialogRow in row.metadata.structured_response.
        """
        raise NotImplementedError('Structured chat output is not implemented in this LLM Driver.')