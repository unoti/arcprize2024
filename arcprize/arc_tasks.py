from arclib.core import DocstringPromptStep, TaskContext
from arclib.models import ArcCase
from arcprize.case_renderer import case_pair_text, case_pair_list_text, row_group_text

def get_case(context: TaskContext) -> ArcCase:
    return ArcCase(**context.session.app_context['case'])

#*TODO: add system prompt step
# class ArcSystemPrompt(SystemPromptStep):
#     """You are an expert puzzle solver and an expert software engineer,
#     in a quiet environment where you can think carefully, focus and think to do an exam.
#     """
#     role = DialogRole.SYSTEM # This line won't actually be needed because of how we subclassed



class IntroduceProblem(DocstringPromptStep):
    """We are working on a problem from the ARC Prize, and you are a smart and
    creative agent working on one of the problems from the challenge.
    This involves looking at a pattern of several sample input cases, determining what is happening
    in them, and then applying the same approach to a test item.

    Let's look at the input and output pairs from the training set for this particular problem.
    There is some kind of transformation rule that goes from the input items to the the output items.
    Let's look at all the items from the training set where they gave us pairs of inputs with their answers.
   
    {train_set_str}

    Take some time to look at the patterns here and consider what rule or pattern is being used
    to get from the inputs to the outputs.  You can think of a 0 as being blank or black, usually.
    The other values you can think of as corresponding to different colors, and the full matrix
    creating an image.  Often various kinds of patterns emerge in doing the transformation to
    the output.
    """
    def prompt_variables(self, context: TaskContext) -> dict:
        case = get_case(context)
        train_set_str = case_pair_list_text(case.train, 'Training')
        return {'train_set_str': train_set_str}


class ProposeSolution1(DocstringPromptStep):
    """Now let's move on to the first "Test" item, the first one that we need to think through
    and solve ourselves. This is a Test case like an Exam, one that we must think very hard about.
    We can also think of it as a Test in the sense that all the above cases are Training cases.
    Given this input, consider what you think the output should be:

    {input_item_str}
    """
    def prompt_variables(self, context: TaskContext) -> dict:
        case = get_case(context)
        input_item_str = row_group_text(case.test[0].input, 0, 'Input', 'Test')
        return {'input_item_str': input_item_str}


all_arc_task_classes = [
    IntroduceProblem,
    ProposeSolution1,
]