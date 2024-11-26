import unittest


class TestCaseRender(unittest.TestCase):
    def test_render_case_pair(self):
        """We can render a case pair in a readable way with sizes."""
        pair = {
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
