import unittest

from arclib.dataproviders import ArcCaseProvider
from arclib.models import ArcDataSet

class TestArcCaseProvider(unittest.TestCase):
    def setUp(self):
        self.arc_provider = ArcCaseProvider()

    def test_case_list(self):
        case_ids = self.arc_provider.get_case_ids(ArcDataSet.TRAINING)
        self.assertEqual(400, len(case_ids), 'There are 400 cases in the training set.')
        eval_case_ids = self.arc_provider.get_case_ids(ArcDataSet.EVALUATION)
        self.assertEqual(400, len(eval_case_ids), 'There are 400 cases in the training set.')

    def test_get_case(self):
        case_id = '0a938d79'
        case = self.arc_provider.get_case(case_id)
        print(case)