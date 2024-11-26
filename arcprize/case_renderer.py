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
    

def row_group_strs(rows: List[DataRow], title: str, seq: int) -> List[str]:
    """Renders a group of rows (the input or output section of a CasePair) with title and size."""
    out = [f'### Case {seq} {title}: size {size_str(rows)}']
    out.append('```')
    for row in rows:
        out.append(' '.join([str(x) for x in row]))
    out.append('```')
    return out


def case_pair_text(case_pair: CasePair, seq: int) -> str:
    """Renders a single case pair with its size.
    
    :param seq: Sequence number for formatting.
    """
    out = [f'## Case {seq}']
    out.extend(row_group_strs(case_pair.input, 'Input', seq))
    out.extend(row_group_strs(case_pair.output, 'Output', seq))
    out.append('')
    return '\n'.join(out)

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


