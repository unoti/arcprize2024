import json
from pathlib import Path
from typing import List

from ..models import ArcDataSet, ArcCase, CasePair


class ArcCaseProvider:
    """Gets ARC prize cases from the arc repository."""
    def __init__(self):
        self._data_root = Path(__file__).parent.parent.parent / 'data'

    def get_case_ids(self, dataset: ArcDataSet = ArcDataSet.TRAINING) -> List[str]:
        """Gets a list of case ids that exist within the given dataset."""
        directory = self._dataset_dir(dataset)
        filenames = [file.name.split('.')[0] for file in directory.iterdir() if file.is_file()]
        return filenames

    def get_case(self, id: str, dataset: ArcDataSet = ArcDataSet.TRAINING) -> ArcCase:
        directory = self._dataset_dir(dataset)
        path = directory / f'{id}.json'
        with open(path, 'r') as file:
            content = file.read()
        content_dict = json.loads(content)
        train_pairs = self._make_pairs(content_dict['train'])
        test_pairs = self._make_pairs(content_dict['test'])
        case = ArcCase(id=id, dataset=dataset, train=train_pairs, test=test_pairs)
        return case

    def _dataset_dir(self, dataset: ArcDataSet) -> Path:
        return self._data_root / dataset.value

    def _make_pairs(self, case_list: List[dict]) -> List[CasePair]:
        pairs = []
        for rec in case_list:
            case_pair = CasePair(input=rec['input'], output=rec['output'])
            pairs.append(case_pair)
        return pairs