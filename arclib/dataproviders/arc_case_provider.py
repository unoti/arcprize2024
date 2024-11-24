from pathlib import Path
from typing import List

from ..models import ArcDataSet, ArcCase


class ArcCaseProvider:
    """Gets ARC prize cases from the arc repository."""
    def __init__(self):
        self._data_root = Path(__file__).parent.parent.parent / 'data'

    def get_case_ids(self, dataset: ArcDataSet = ArcDataSet.TRAINING) -> List[str]:
        """Gets a list of case ids that exist within the given dataset."""
        directory = self._dataset_dir(dataset)
        filenames = [file.name for file in directory.iterdir() if file.is_file()]
        return filenames

    def get_case(self, id: str, dataset: ArcDataSet = ArcDataSet.TRAINING) -> ArcCase:
        ...

    def _dataset_dir(self, dataset: ArcDataSet) -> Path:
        return self._data_root / dataset.value