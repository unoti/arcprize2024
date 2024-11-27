from enum import Enum
from pydantic import BaseModel
from typing import List, Tuple

class ArcDataSet(str, Enum):
    """Data sets in the arc challenge."""
    TRAINING = 'training'
    EVALUATION = 'evaluation'

DataRow = List[int]

class CasePair(BaseModel):
    input: List[DataRow]
    output: List[DataRow]

class ArcCase(BaseModel):
    id: str
    dataset: ArcDataSet
    train: List[CasePair]
    test: List[CasePair]

def rows_size_tuple(rows: List[DataRow]) -> Tuple[int, int]:
    """Calculate the size of a list of rows."""
    x = len(rows[0])
    y = len(rows)
    return (x, y)

class Matrix(BaseModel):
    """This is used for structuring OpenAI responses for the output matrix."""
    rows: List[DataRow]
