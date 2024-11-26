from arclib.core import PromptStep, SystemPromptStep, TaskContext
from arclib.models import ArcCase
from arcprize.case_renderer import case_pair_list_text, row_group_text


def get_case(context: TaskContext) -> ArcCase:
    return ArcCase(**context.session.app_context['case'])


class ArcSystemPrompt(SystemPromptStep):
    """You are an expert puzzle solver and an expert software engineer here
    to do everything you can to help the user.
    You are in a quiet environment where you can think carefully, and focus to do an exam.
    """


class IntroduceProblem(PromptStep):
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


class ProposeSolution1(PromptStep):
    """Now let's move on to the first "Test" item, the first one that we need to think through
    and solve ourselves. This is a Test case like an Exam, one that we must think very hard about.
    We can also think of it as a Test in the sense that all the above cases are Training cases.
    Given this input, consider what you think the output should be:

    {input_item_str}

    Given that input item, what do you suppose the output should be?
    """
    def prompt_variables(self, context: TaskContext) -> dict:
        case = get_case(context)
        input_item_str = row_group_text(case.test[0].input, 0, 'Input', 'Test')
        return {'input_item_str': input_item_str}


class RowCount(PromptStep):
    """How many output rows do you think should be present?"""


class InputOutputRows(PromptStep):
    """How many input and output rows do each of the examples have, for the ones that we know about?"""


class OutputAnswer(PromptStep):
    """Please output for me what you think the output section should look like for this
    problem given what you have observed.
    """


all_arc_task_classes = [
    ArcSystemPrompt,
    IntroduceProblem,
    ProposeSolution1,
    RowCount,
    InputOutputRows,
    OutputAnswer,
]