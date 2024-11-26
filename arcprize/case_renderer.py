from typing import List

from arclib.models import ArcCase, CasePair
from arclib.infra.string import spaces, make_comma


DataRow = List[int]
space_per_indent = 4

def datarow_to_str(row: DataRow, comma: bool) -> str:
    row_strs = ', '.join([str(n) for n in row])
    return f'                [{row_strs}]{make_comma(comma)}'

def _output_section(rows: List[DataRow], section_name: str, comma: bool) -> List[str]:
    out = []
    out.append(f'            "{section_name}": [')
    for index, row in enumerate(rows):
        show_comma = index < len(rows) - 1
        out.append(datarow_to_str(row, show_comma))
    last = f'            ]{make_comma(comma)}'
    out.append(last)
    return out

def _case_pair_to_str(cp: CasePair, comma: bool) -> List[str]:
    out = [ '        {']
    out.extend(_output_section(cp.input, 'input', True))
    out.extend(_output_section(cp.output, 'output', False))
    out.append('        }' + make_comma(comma))
    return out

def case_to_str(case: ArcCase) -> str:
    """Renders the input samples of an ARC case to a string.

    The default JSON format with indent=4 works poorly for arc cases,
    because each int is rendered on its own line. This makes it easier to read.
    """
    out = [ '{']
    out.append('    "train": [')
    for index, case_pair in enumerate(case.train):
        rows = _case_pair_to_str(case_pair, index < len(case.train) - 1)
        out.extend(rows)
    out += ['}']
    print(out)
    return '\n'.join(out)
