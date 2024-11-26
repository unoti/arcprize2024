from typing import List

from arclib.models import ArcCase, CasePair


DataRow = List[int]

def datarow_to_str(row: DataRow, comma: bool) -> str:
    row_strs = ', '.join([str(n) for n in row])
    if comma:
        comma_str = ','
    else:
        comma_str = ''
    return f'        [{row_strs}]{comma_str}'

def _output_section(rows: List[DataRow], section_name: str, comma: bool) -> List[str]:
    out = []
    out.append(f'    "{section_name}": [')
    for row in rows:
        out.append(datarow_to_str(row, True))
    last = '    ]'
    if comma:
        last += ','
    out.append(last)
    return out

def _case_pair_to_str(cp: CasePair) -> List[str]:
    out = _output_section(cp.input, 'input', True)
    out.extend(_output_section(cp.output, 'output', False))
    return out

def case_to_str(case: ArcCase) -> str:
    """Renders the input samples of an ARC case to a string.

    The default JSON format with indent=4 works poorly for arc cases,
    because each int is rendered on its own line. This makes it easier to read.
    """
    out = [ '{']
    out.append('    "train": [')
    for case_pair in case.train:
        for rows in _case_pair_to_str(case_pair):
            print('extending with ',rows)
            out.append(rows)
    out += ['}']
    print(out)
    return '\n'.join(out)
