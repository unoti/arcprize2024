from dataclasses import dataclass
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

@dataclass
class ArcCase:
    id: str
    dataset: ArcDataSet
    train: List[CasePair]
    test: List[CasePair]
