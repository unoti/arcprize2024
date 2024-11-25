import unittest

from arcprize import ArcBuilder


class TestArcRunner(unittest.TestCase):
    diagnostic_output = False
    #diagnostic_output = True

    def setUp(self):
        self.builder = ArcBuilder().with_llm_mock().with_stdout(self.diagnostic_output)
        self.runner = self.builder.build()
        
    def test_runner(self):
        """Verify the basic operation of ArcRunner."""
        self.runner.run()