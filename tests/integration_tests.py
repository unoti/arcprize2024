from arclib.core import StructuredPromptStep, TaskContext
from arclib.llm import LlmDriver
from arclib.models import Dialog, Matrix, Session
from arcprize.builders import ArcBuilder


class MatrixStep(StructuredPromptStep):
    """Can you make a 4x4 identity matrix for me?
    """
    def response_class(self):
        return Matrix


def test_structured_response(llm: LlmDriver):
    """LLM should be able to respond using structured JSON based on a Pydantic model."""
    print('--structured_response')
    dialog = Dialog()
    session = Session(dialog=dialog)
    step = MatrixStep()
    context = TaskContext(session, llm)
    step.execute(context)
    response_row = step.send_llm(llm, dialog)
    print(response_row)
    result_object = response_row.metadata.structured_result
    assert(result_object.__class__ == Matrix)
    assert(response_row.metadata.structured_result_class == 'Matrix')


def test_llm(llm: LlmDriver):
    """Verifies basic connectivity of the LLM."""
    print('--llm')
    result = llm.chat('Hi, just checking if we are connected properly. Briefly, can you read this?')
    print(result)


def main():
    print('Arclib integration tests')
    builder = ArcBuilder()
    llm = builder.get_llm()

    #test_llm(llm)
    test_structured_response(llm)

    print('--Tests concluded.')


if __name__ == '__main__':
    main()