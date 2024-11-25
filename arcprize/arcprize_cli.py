"""ARC Prize 2024 application
"""
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--llm', '-l', default='gpt4o', choices=['gpt4o', 'mock'],
                        help='LLM model to use. Mock provider can be used for testing.')
    parser.add_argument('--count', '-c', type=int, help='How many items to process')
    args = parser.parse_args()
    return args


def main():
    print('Arcprize cli')
    args = parse_arguments()
    count = args.count
    print(count, type(count))


if __name__ == '__main__':
    main()
