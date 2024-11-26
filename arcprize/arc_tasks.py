from arclib.core import DocstringPromptStep, TaskContext
from arclib.models import ArcCase
from arcprize.case_renderer import case_pair_text

def get_case(context: TaskContext) -> ArcCase:
    return ArcCase(**context.session.app_context['case'])


class IntroduceProblem(DocstringPromptStep):
    """We are working on a problem from the ARC Prize, and you are a smart and
    creative agent working on one of the problems from the challenge.
    This involves looking at a pattern of several sample input cases, determining what is happening
    in them, and then applying the same approach to a test item.

    Let's look at the first case.  Given this input, consider what you think the output
    should be.

    {input_item_str}
    """
    # [ ] show all the train questions
    # [ ] show the input side of the test question
    def prompt_variables(self, context: TaskContext):
        case = get_case(context)
        input_item_str = case_pair_text(case.test[0], 0)
        return {'input_item_str': input_item_str,
                'case_id': context.session.app_context['case_id'] # temp
                }

all_arc_task_classes = [IntroduceProblem]