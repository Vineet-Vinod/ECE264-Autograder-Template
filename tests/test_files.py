from unittest import TestCase
from gradescope_utils.autograder_utils.decorators import weight
from gradescope_utils.autograder_utils.files import check_submitted_files
from weights import TEST_FILES


def files_submitted():
    """
    Only modify this function - change line 11 and include all the files students are expected to submit
    """
    for path in (missing_files := check_submitted_files(["Expected student files"])):
        print(f"Missing {path}")
    
    return missing_files


class test_files(TestCase):
    @weight(TEST_FILES)
    def test_files(self):
        """Test Files"""
        missing_files = files_submitted()
        self.assertEqual(len(missing_files), 0, "Check your submitted files")
