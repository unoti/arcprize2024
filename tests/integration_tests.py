from arcprize.builders import get_llm
from arclib.llm import LlmDriver


def test_llm(llm: LlmDriver):
    print('--llm')
    result = llm.chat('Hi, just checking if we are connected properly. Briefly, can you read this?')
    print(result)

def main():
    print('Arclib integration tests')
    test_llm(get_llm())
    print('--Tests concluded.')


if __name__ == '__main__':
    main()