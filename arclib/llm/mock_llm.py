from arclib.llm import LlmDriver
from arclib.models import Dialog, DialogRole, DialogRow

class MockLlmDriver(LlmDriver):
    """An LLM driver running locally suitable for unit tests.
    """
    def chat_dialog(self, dialog: Dialog) -> DialogRow:
        last_row = dialog.rows[-1]
        resp_text = f'response({last_row.text})'
        resp_row = DialogRow(role=DialogRole.ASSISTANT, text=resp_text)
        return resp_row