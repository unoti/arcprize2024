"""Provides extra information about cases for analysis.
"""
from typing import Iterable, Optional

_titles_by_case_id = {
'007bbfb7': '3x3 expand to 9x9, replicate when set',
'00d62c1b': 'Flood fill',
'017c7c7b': 'Continue pattern to height',
'025d127b': 'Square up the bottom',
'045e512c': 'Directional color replicator',
'0520fde7': 'Boolean AND on two 3x3s',
'05269061': 'Diagonal pattern expander',
'05f2a901': 'Square sucks in the shape',
'06df4c85': 'Connect same colors in the grid',
'08ed6ac7': 'Size 1-4 histogram classifier',
'09629e4f': 'Find, copy and expand the section without blue',
'0962bcdd': 'Grow crystals',
'0a938d79': 'Expand into stripes and continue',
'0b148d64': 'Find the unique color cluster and output it',
'0ca9ddb6': "Grow crystals 2, don't grow blue",
'0d3d703e': 'Simple color transform',
'0dfd9992': 'Ginormous pattern fill',
'0e206a2e': 'Rotate, translate ships to indicated positions',
'10fcaaa3': 'Grow blue on diagonals and double the pattern',
'11852cab': 'Expand to a square with given color',
}

def get_case_title(case_id: str) -> Optional[str]:
    return _titles_by_case_id.get(case_id)

def get_case_titles(case_ids: Iterable[str]) -> Iterable[Optional[str]]:
    """Given a sequence of case ids, returns a sequence of their titles.
    These titles are a general summary of what the case is about for analysis purposes.
    """
    for case_id in case_ids:
        yield _titles_by_case_id.get(case_id)
