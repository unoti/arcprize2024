import unittest

from arclib.infra.string import dedent
from arclib.models import CasePair
from arcprize.case_renderer import case_pair_text

class TestCaseRender(unittest.TestCase):
    def test_render_case_pair(self):
        """We can render a case pair in a readable way with sizes."""
        # Arrange.
        pair_dict = {
            "input": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 3, 0, 0, 0],
                [0, 3, 0, 3, 0, 0],
                [0, 0, 3, 0, 3, 0],
                [0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 3, 0, 0, 0],
                [0, 3, 4, 3, 0, 0],
                [0, 0, 3, 4, 3, 0],
                [0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ]
        }
        case_pair = CasePair(input=pair_dict['input'], output=pair_dict['output'])

        # Act.
        rendered = case_pair_text(case_pair, 0, 'Sample')

        # Assert.
        expected = dedent("""## Sample Case 0
            ### Sample Case 0 Input: size 6x6
            ```
            0 0 0 0 0 0
            0 0 3 0 0 0
            0 3 0 3 0 0
            0 0 3 0 3 0
            0 0 0 3 0 0
            0 0 0 0 0 0
            ```
            ### Sample Case 0 Output: size 6x6
            ```
            0 0 0 0 0 0
            0 0 3 0 0 0
            0 3 4 3 0 0
            0 0 3 4 3 0
            0 0 0 3 0 0
            0 0 0 0 0 0
            ```
            """)
        # We're replacing newlines so that the single-line diff in the error output is more helpful.
        a = expected.replace('\n','*')
        b = expected.replace('\n','*')
        self.assertEqual(a, b, 'This is how the output should look (newlines have been replaced)')