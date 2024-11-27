"""ARC Prize 2024 application
"""
import argparse
from typing import Optional

from arclib.infra.time import timestamp_string
from arcprize import ArcBuilder, ArcRunner


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--llm', '-l', default='gpt4o', choices=['gpt4o', 'mock'],
                        help='LLM model to use. Mock provider can be used for testing.')
    parser.add_argument('--firstn', '-fn', type=int, help='Only process the first N problems')
    parser.add_argument('--outdir', '-od', help='Output directory. By default we use local/out/s-{timestamp}')
    parser.add_argument('--seq', '-s', nargs='+', type=int, help='Execute cases given their sequence numbers')
    parser.add_argument('--cases', '-c', nargs='+', help='Execute one or more case ids')
    args = parser.parse_args()
    return args


def make_runner(args: argparse.Namespace) -> ArcRunner:
    builder = ArcBuilder()
    if args.llm:
        if args.llm == 'mock':
            print('Using mock LLM')
            builder.with_llm_mock()
        elif args.llm == 'gpt4o':
            pass
        else:
            raise ValueError(f'Unsupported llm {args.llm}')
    if args.firstn is not None:
        print(f'Processing the first {args.firstn} items')
        builder.with_first_n(args.firstn)
    if args.seq:
        print(f'Processing sequence ids {args.seq}')
        builder.with_sequence_ids(args.seq)
    if args.cases:
        print(f'Processing case ids {args.cases}')
        builder.with_case_ids(args.cases)
    if args.outdir is not None:
        dir_prefix = args.outdir
    else:        
        dir_prefix = f'local/out/s-{timestamp_string()}/'
    builder.with_session_dir(dir_prefix)
    return builder.build()


def main():
    print('Arcprize cli')
    arc_runner = make_runner(parse_arguments())
    arc_runner.run()


if __name__ == '__main__':
    main()
