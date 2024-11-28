"""This module formats ARC cases as either readable text, or as JSON.
Internally we use lots of lists of strings instead of strings
because building strings incrementally with concatenation can
be inefficient, and also because it can be useful sometimes
to keep the lines separate until the last moment (to avoid repeatedly joining and splitting).
"""
from typing import List

from arclib.models import ArcCase, CasePair, rows_size_tuple
from arclib.infra.string import spaces, make_comma


DataRow = List[int]
space_per_indent = 4

# This section is about formatting a more readable (non-json) text representation of cases.
def size_str(rows: List[DataRow]) -> str:
    """Returns a string indicating the size of a matrix."""
    width, height = rows_size_tuple(rows)
    return f'{width}x{height}'
    

def matrix_strs(rows: List[DataRow], title: str, seq: int, case_prefix: str='') -> List[str]:
    """Renders a matrix with title and size to a list of strings."""
    if case_prefix:
        case_prefix = case_prefix + ' '
    out = [f'### {case_prefix}Case {seq} {title}: size {size_str(rows)}']
    out.append('```')
    for row in rows:
        out.append(' '.join([str(x) for x in row]))
    out.append('```')
    return out


def matrix_text(rows: List[DataRow], title: str, seq: int, case_prefix: str='') -> str:
    """Outputs a matrix to a string."""
    return '\n'.join(matrix_strs(rows, title, seq, case_prefix))


def case_pair_strs(case_pair: CasePair, seq: int, title_prefix: str) -> List[str]:
    """Renders a single case pair with its size to a list of strings."""
    out = [f'## {title_prefix} Case {seq}']
    out.extend(matrix_strs(case_pair.input, 'Input', seq, title_prefix))
    out.extend(matrix_strs(case_pair.output, 'Output', seq, title_prefix))
    out.append('')
    return out


def case_pair_text(case_pair: CasePair, seq: int, title_prefix: str) -> str:
    """Renders a single case pair with its size.
    
    :param seq: Sequence number for formatting.
    :param title_prefix: Put this before the title for each of the pairs.
    """
    out = case_pair_strs(case_pair, seq, title_prefix)
    return '\n'.join(out)


def case_pair_list_strs(case_pairs: List[CasePair], title: str) -> List[str]:
    """Output a group of case pairs, both their inputs and outputs."""
    out = []
    for seq, pair in enumerate(case_pairs):
        out.extend(case_pair_strs(pair, seq, title))
    return out


def case_pair_list_text(case_pairs: List[CasePair], title: str) -> str:
    return '\n'.join(case_pair_list_strs(case_pairs, title))    



# JSON: this section formats to JSON, but with a sensible indent strategy.
# The default json.dumps(d, indent=4) for a list of ints outputs every integer on its own line
# Which is unreadable.
def datarow_to_str(row: DataRow, indent: int, comma: bool) -> str:
    row_strs = ', '.join([str(n) for n in row])
    return spaces(indent) + f'[{row_strs}]{make_comma(comma)}'

def _output_section(rows: List[DataRow], section_name: str, indent: int, comma: bool) -> List[str]:
    out = []
    out.append(spaces(indent) + f'"{section_name}": [')
    inside_indent = indent + space_per_indent
    for index, row in enumerate(rows):
        show_comma = index < len(rows) - 1
        out.append(datarow_to_str(row, inside_indent, show_comma))
    out.append(spaces(indent) + ']' + make_comma(comma))
    return out

def _case_pair_to_str(cp: CasePair, indent: int, comma: bool) -> List[str]:
    out = [spaces(indent) + '{']
    inside_indent = indent + space_per_indent
    out.extend(_output_section(cp.input, 'input', inside_indent, True))
    out.extend(_output_section(cp.output, 'output', inside_indent, False))
    out.append(spaces(indent) + '}' + make_comma(comma))
    return out

def case_to_json_str(case: ArcCase) -> str:
    """Renders the input samples of an ARC case to a string.

    The default JSON format with indent=4 works poorly for arc cases,
    because each int is rendered on its own line. This makes it easier to read.
    """
    indent = 0
    out = [ '{']
    indent += space_per_indent
    out.append(f'{spaces(indent)}"train": [')
    indent += space_per_indent
    for index, case_pair in enumerate(case.train):
        rows = _case_pair_to_str(case_pair, indent, index < len(case.train) - 1)
        out.extend(rows)
    indent -= space_per_indent
    out += [spaces(indent) + '}']
    return '\n'.join(out)


