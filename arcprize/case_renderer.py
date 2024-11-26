from typing import List

from arclib.models import ArcCase, CasePair
from arclib.infra.string import spaces, make_comma


DataRow = List[int]
space_per_indent = 4

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

def case_to_str(case: ArcCase) -> str:
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
    print(out)
    return '\n'.join(out)
