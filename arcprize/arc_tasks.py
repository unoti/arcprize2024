import json

from arclib.core import DocstringPromptStep, TaskContext


class IntroduceProblem(DocstringPromptStep):
    """We are working on a problem from the ARC Prize, and you are a smart and
    creative agent working on one of the problems from the challenge.
    This involves looking at a pattern of several sample input cases, determining what is happening
    in them, and then applying the same approach to a test item.

    Let's look at the first case.  Given this input, consider what you think the output
    should be.

    Input item:
    ```json
    {input_item_str}
    ```
    """
    def prompt_variables(self, context: TaskContext):
        input_item_json = {
            'test': [123, 0, 0]
        }
        input_item_str = json.dumps(input_item_json, indent=4)
        return {'input_item_str': input_item_str}

all_arc_task_classes = [IntroduceProblem]