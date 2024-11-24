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
        self.assertEqual(case_id, case.id)
        self.assertEqual(ArcDataSet.TRAINING, case.dataset)
        #import pdb;pdb.set_trace()
        self.assertEqual(4, len(case.train))
        self.assertListEqual(case.train[0].input[0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(1, len(case.test))
        self.assertListEqual(case.test[0].input[0],
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertListEqual(case.test[0].output[0],
            [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0])