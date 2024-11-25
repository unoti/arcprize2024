"""ARC Prize 2024 application
"""
import argparse
from typing import Optional

from arcprize import ArcBuilder, ArcRunner


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--llm', '-l', default='gpt4o', choices=['gpt4o', 'mock'],
                        help='LLM model to use. Mock provider can be used for testing.')
    parser.add_argument('--firstn', '-fn', type=int, help='Only process the first N problems')
    args = parser.parse_args()
    return args


def make_runner(llm_mock: bool, first_n: Optional[int]) -> ArcRunner:
    if llm_mock:
        print('Using mock LLM')
    if first_n:
        print(f'Processing the first {first_n} items')
    builder = ArcBuilder()
    return builder.build()


def main():
    print('Arcprize cli')
    args = parse_arguments()

    if args.llm == 'mock':
        llm_mock = True
    elif args.llm == 'gpt4o':
        llm_mock = False
    else:
        raise ValueError(f'Unsupported llm model {args.llm}')
    
    arc_runner = make_runner(llm_mock=llm_mock, first_n=args.firstn)
    arc_runner.run()


if __name__ == '__main__':
    main()
