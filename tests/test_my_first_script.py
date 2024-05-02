import unittest

from common.my_first_script import _my_first_script


class My_first_scriptTest(unittest.TestCase):
    def setUp(self):
        # self.task = Task("Dummy task", False)
        pass

    def tearDown(self):
        # To be implemented if required
        pass

    def test_my_first_script(self):
        self.assertEqual(
            _my_first_script("green", "blue"), {"argA": "green", "argB": "blue"}
        )
