import unittest

from arclib.core import DocstringPromptStep, TaskContext
from arclib.models import Session, Dialog
from arclib.llm import MockLlmDriver


class TestTaskStep(unittest.TestCase):
    def setUp(self):
        self.llm = MockLlmDriver()

    def test_task_multiline(self):
        """When formatting a prompt with a docstring we properly handle indentation."""
        # Arrange.
        class MyTask(DocstringPromptStep):
            """Line 1
            Line 2
                Line 3 indent
            """
        
        session = Session(dialog=Dialog(rows=[]))
        context = TaskContext(session, self.llm)
        task = MyTask()

        # Act.
        task.execute(context)

        # Assert.
        created_text = session.dialog.rows[0].text
        self.assertEqual('Line 1\nLine 2\n    Line 3 indent\n', created_text, 'Indentation should be removed.')
