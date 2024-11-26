from dataclasses import dataclass, asdict
from enum import Enum
from typing import List

class ArcDataSet(str, Enum):
    """Data sets in the arc challenge."""
    TRAINING = 'training'
    EVALUATION = 'evaluation'

DataRow = List[int]

@dataclass
class CasePair:
    input: List[DataRow]
    output: List[DataRow]

    def to_dict(self) -> dict:
        """Return this CasePair as a dictionary."""
        return asdict(self)

    def json_str(self) -> str:
        """Render a string of JSON for this CasePair.
        
        The default JSON dumps with indent=4 renders every integer on a new line,
        which is very difficult to read and reason about-- for humans at least.
        """
        rows_strs = ['{',
            '\tinput: [',
        ]
        middle_rows = [self._render_datarow(row) for row in self.input]
        row_strs2 = [
            '\t]',
            '}',
        ]
        all_rows = rows_strs + middle_rows + row_strs2
        return '\n'.join(all_rows)

    def _render_datarow(self, row: List[int]):
        row_strs = ', '.join([str(n) for n in row])
        return f'\t\t[{row_strs}]'


@dataclass
class ArcCase:
    id: str
    dataset: ArcDataSet
    train: List[CasePair]
    test: List[CasePair]

    def to_dict(self):
        return asdict(self)