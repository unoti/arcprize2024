from dataclasses import dataclass, asdict
from enum import Enum
from pydantic import BaseModel
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


class ArcCase(BaseModel):
    id: str
    dataset: ArcDataSet
    train: List[CasePair]
    test: List[CasePair]

