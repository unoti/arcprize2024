from typing import Tuple

from arclib.core import (
    PromptStep,
    StructuredPromptStep,
    SystemPromptStep,
    TaskContext,
    TaskStep,
)
from arclib.models import ArcCase, CasePair, Matrix
from arcprize.case_renderer import case_pair_list_text, matrix_text


def get_case(context: TaskContext) -> ArcCase:
    return ArcCase(**context.session.app_context['case'])


def get_holdout_case(context: TaskContext) -> Tuple[int, CasePair]:
    """Gets the last test case which we initially hide from the agent."""
    case = get_case(context)
    index = len(case.train) - 1
    return (index, case.train[index])


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
        cases_to_show = case.train[:-1] # Hold out one training case to reveal later.
        train_set_str = case_pair_list_text(cases_to_show, 'Training')
        return {'train_set_str': train_set_str}


class RowCount(PromptStep):
    """For problems like these, how many output rows do you think should be present?"""


class InputOutputRows(PromptStep):
    """How many input and output rows do each of the examples have, for the ones that we know about?"""


class ProposeSolution1(PromptStep):
    """Here is a new problem from the same set.  What do you suppose its answer is?

    {input_item_str}

    Consider how to apply your approach on this, then provide your answer for the output for this one.
    """
    def prompt_variables(self, context: TaskContext) -> dict:
        case_seq, case = get_holdout_case(context)
        input_item_str = matrix_text(case.input, case_seq, 'Input', 'Test')
        return {'input_item_str': input_item_str}


class CheckAnswer1(PromptStep):
    """Let's see how you did.  This is the answer for that one, training case {case_seq}:

    {output_item_str}

    How did you do?  If you got it wrong then consider a strategy for getting this right next time.
    What advice would you give yourself, or what insight were you missing, if any?
    """
    def prompt_variables(self, context: TaskContext) -> dict:
        case_seq, case = get_holdout_case(context)
        output_item_str = matrix_text(case.output, case_seq, 'Output', 'Test')
        return {'output_item_str': output_item_str, 'case_seq': case_seq}


# Removed for experiment 3, see notebooks/3*
# class StrategyClarity(PromptStep):
#     """Do you have a solid, unambiguous theory of operation or algorithm that applies to
#     **all** of the cases?  If your hypothesis is not strong, rethink your approach and come
#     up with something that cleanly explains all of the use cases you know about.
#     Experience has taught us that one of the most common ways we end up getting problems
#     wrong is by trying to do these problems with an ambiguous algorithm.
#     Without crystal clarity on the rule we will almost certainly fail.  So this is your
#     chance to think about it if your algorithm does not have sufficient clarity.
#     """

# Added for experiment 3, see notebooks/3*
class StrategiesStep(PromptStep):
    """Here are some common strategies that are sometimes used in these tasks.  We are telling
    you about these to give you a feel for the wide variety of things that can happen in these
    tasks.  The sky is the limit on what these puzzles might do, so hopefully this list will
    give you ideas on how to approach your problem.

    Here are stratgies or explanations of the transforms needed to solve some puzzles we have
    seen:
    1. The input is a small pattern which is expanded in a 3x3 matrix out to the 9x9 matrix
        by replicating it into the corresponding block of the big 9x9 matrix when the cell
        is set within the 3x3 matrix.
    2. We're doing a flood fill, finding fully enclosed spaces in the input and filling it in
        with a color (number).
    3. The output is a fixed height, and we replicate the pattern seen in the input, continuing
        it to a fixed height.
    4. There is a pattern implied in the input in the foreground (non-zero inputs).  Continue that
        pattern into a same-sized output.  The position of that pattern must match the input
        such that the output rows arrive in the same spots of the input, if you were to visualize
        the input and output matrices as being superimposed on each other.
    5. The input can be considered two 3x3 matrices separated by a barrier which is ignored.
        Envision the two input matrices on top of each other, and do a boolean AND operation
        to decide on the output in the output's 3x3 matrix.
    6. There is a fixed square object which will be in the same position in the output, and the other objects
        should be considered mobile objects.  The mobile objects will translate and move up adjacent
        to the fixed object, sticking up against it.

    We mention these strategies so you can get an idea of what a successful strategy explanation
    sounds like, and to show you how widely varied and fiendish these puzzles can be.  In every case
    there's always a definite way to for definitely predict what the output will be.  Often
    it'll seem like the solution is elusive, or that you need to guess.  If you're feeling like
    you need to guess, then that means you haven't figured out how the puzzles work yet.

    Use this opportunity to consider whether you're satisfied with your understanding of how this case
    works, and to refine your strategy before we take a real graded test question.
    """


class ProposeTestAnswer(StructuredPromptStep):
    """Let's try another problem, this one is from the test set, the real exam.
    Here is the input pattern:

    {output_item_str}

    Please output a solution for this one.
    """
    def prompt_variables(self, context: TaskContext) -> dict:
        case = get_case(context)
        output_item_str = matrix_text(case.test[0].input, 0, 'Input', 'Test')
        return {'output_item_str': output_item_str}

    def response_class(self):
        return Matrix


class ScoringStep(SystemPromptStep):
    """
    ## Agent Answer: `{scoring}`

    {agent_answer}

    {correct_answer}
    """
    def prompt_variables(self, context: TaskContext):
        # This puts the score into the session and transcript.
        # Because it's going in a System prompt and not user, this won't get
        # sent to the LLM, because we only send to the LLM when the last dialog row is a User role.
        last_row = context.session.dialog.rows[-1]
        matrix: Matrix = last_row.metadata.structured_result
        agent_answer = matrix_text(matrix.rows, 0, '', 'Agent Answer')
        case = get_case(context)
        success = case.test[0].output == matrix.rows
        context.session.app_context['success'] = success # This will get saved into the session.
        scoring = 'PASS' if success else 'FAIL'
        if success:
            correct_answer = ''
        else:
            correct_answer = matrix_text(case.test[0].output, 'Output', 0, 'Correct Answer')
        return {'scoring': scoring,
                'agent_answer': agent_answer,
                'correct_answer': correct_answer}



# all_arc_task_classes = [
#     ArcSystemPrompt,
#     IntroduceProblem,
#     RowCount,
#     InputOutputRows,
#     ProposeSolution1,
#     CheckAnswer1,
#     StrategiesStep,
#     #StrategyClarity,
#     ProposeTestAnswer,
#     ScoringStep,
# ]

all_arc_task_classes = [
    #ArcSystemPrompt, # (experiment 3)
    IntroduceProblem,
    #RowCount, # (experiment 3)
    #InputOutputRows, # (experiment 3)
    ProposeSolution1,
    CheckAnswer1,
    StrategiesStep, # (experiment 3)
    #StrategyClarity, # Which replaces this step (experiment 3)
    ProposeTestAnswer,
    ScoringStep,
]