from unittest import TestCase
from gradescope_utils.autograder_utils.decorators import weight
import subprocess
import os
from weights import TEST_GCC
from test_files import files_submitted


FILES = "C source files" # Change this line
EXEC = "Executable"      # Change this line
GCC = f"gcc -std=c11 -g -Wall -Wshadow --pedantic -Wvla -Werror"
COMMAND = f"{GCC} {FILES} -o {EXEC}"

def compile():
    return subprocess.run(COMMAND, shell=True, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))


class test_gcc(TestCase):
    @weight(TEST_GCC)
    def test_gcc(self):
        """Test GCC"""
        missing_files = files_submitted()
        self.assertEqual(len(missing_files), 0, "Check your submitted files")
        result = compile()
        self.assertEqual(result.returncode, 0, f"{result.stderr}")
