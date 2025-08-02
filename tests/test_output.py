from unittest import TestCase
from gradescope_utils.autograder_utils.decorators import partial_credit
import os
from test_gcc import compile, EXEC
from test_files import files_submitted
from constants import TEST_OUTPUT, TIMEOUT
import asyncio


async def test(args):
    # Only modify this function IF the order of your args is different/you are grading students differently
    missing_files = files_submitted()
    try:
        assert(len(missing_files) == 0)
    except:
        print("Check your submitted files")
        return 0
    
    result = compile()
    try:
        assert(result.returncode == 0)
    except:
        print(f"{result.stderr}")
        return 0

    base_directory = os.path.dirname(os.path.dirname(__file__))
    expected_files = os.path.join(base_directory, "expected")

    command = f"./{EXEC}"
    process = await asyncio.create_subprocess_exec(command, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    try:
        await asyncio.wait_for(process.wait(), TIMEOUT)
        assert(process.returncode == 0)
    except asyncio.TimeoutError:
        print(f"Timed out on {command} {' '.join(args)}")
        process.kill()
        await process.wait()  # Wait till it is dead
        return 0
    except AssertionError:
        stdout, _ = await process.communicate()
        print(f"Returned EXIT_FAILURE for {command}\n{stdout.decode()}")
        return 0

    stdout, _ = await process.communicate()
    with open(os.path.join(expected_files, args[-1]), "r") as expected:
        if expected.read() != stdout.decode():
            return 0
        
    return 1


class test_output(TestCase):
    @partial_credit(TEST_OUTPUT)
    def testall(self, set_score=None):
        """
        Test Output - update to run functions with asyncio to gain more fine-grained control over timeout
        """
        """
        Modify lines 67-69 (add command line args for all tests)
        command_line_arguments is a list which contains lists of command line arguments for each testcase
        the last argument MUST be the expected file name - DO NOT PREFIX WITH expected/
        
        Feel free to change this format but beware that more changes are necessary from your side
        """
        command_line_arguments = [
                                 ["cmd", "line", "args", "1"],
                                 ["cmd", "line", "args", "2"],
                                 ["cmd", "line", "args", "3"]
                                 ]
        
        passed = 0
        for i, argset in enumerate(command_line_arguments):
            res = asyncio.run(test(argset))
            
            if res:
                print(f"Testcase {i+1} passed")
            else:
                print(f"Testcase {i+1} failed")
            
            passed += res

        set_score(round(passed / len(command_line_arguments) * TEST_OUTPUT, 2))
