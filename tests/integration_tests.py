from arclib.builders import ArcApplication, get_app
from arclib.llm import LlmDriver


def test_llm(llm: LlmDriver):
    print('--llm')
    result = llm.chat('Hi, just checking if we are connected properly. Briefly, can you read this?')
    print(result)

def main():
    print('Arclib integration tests')
    app = get_app()
    test_llm(app.get_llm())
    print('--Tests concluded.')


if __name__ == '__main__':
    main()