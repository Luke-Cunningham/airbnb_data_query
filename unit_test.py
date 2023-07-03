import unittest
import FinalAssignment as Final


class TestFA(unittest.TestCase):

    def test_loaded_data(self):
        self.assertEqual(48895, Final.DataSet.load_file(Final.DataSet()))
