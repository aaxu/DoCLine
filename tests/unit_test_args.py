import unittest
import sys
sys.path.append("../")
import docline

class ArgsTestCases(unittest.TestCase):
    def test_get_query(self):
        commands = ["python", "list", "append"]
        expected = ("python", "list append")
        x = docline.get_query(commands)

# This file currently only runs if you are in to root directory of this
# project. It will not work if you are in the docline/tests directory.
# Use the unit_tests.py file instead.
if __name__ == '__main__':
    unittest.main()