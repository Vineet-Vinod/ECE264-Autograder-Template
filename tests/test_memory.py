from unittest import TestCase
from gradescope_utils.autograder_utils.decorators import weight
from test_gcc import compile, EXEC
from test_files import files_submitted
from constants import TEST_MEMORY, TIMEOUT
import asyncio


class test_memory(TestCase):
    MEMORY_ERROR = 2
    @weight(TEST_MEMORY)
    def test_valgrind(self):
        """
        Test Memory - update to run functions with asyncio to gain more fine-grained control over timeout
        """
        """
        Only modify this function - change line 25 to execute the binary with the required command line args
        """
        missing_files = files_submitted()
        self.assertEqual(len(missing_files), 0, "Check your submitted files")
        result = compile()
        self.assertEqual(result.returncode, 0, f"{result.stderr}")

        MEMORY_CMD = f"valgrind"
        args = ["-s", "--errors-for-leak-kinds=all", "--leak-check=full", "--show-leak-kinds=all", f"--error-exitcode={test_memory.MEMORY_ERROR}", f"./{EXEC}", "add", "cmd", "line", "args"]

        async def memory_check():
            nonlocal MEMORY_CMD, args
            process = await asyncio.create_subprocess_exec(MEMORY_CMD, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            # process = await asyncio.create_subprocess_exec(MEMORY_CMD, *args, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE) # Alternate if inputs are passed in through stdin

            try:
                # Inputs through stdin alternative
                # process.stdin.write(f"stdin_inputs".encode())
                # await process.stdin.drain()
                # process.stdin.close()

                await asyncio.wait_for(process.wait(), 2*TIMEOUT)
            except asyncio.TimeoutError:
                print("Program Timed Out!")
                process.kill()
                await process.wait()  # Wait till it is dead
                return test_memory.MEMORY_ERROR

            print("VALGRIND OUTPUT:")
            _, stderr = await process.communicate()
            NOLEAKS = "All heap blocks were freed -- no leaks are possible"
            stderr = stderr.decode()
            print(stderr)

            if NOLEAKS in stderr:
                last_line = stderr.split("\n")[-2]
                SUBSTR = "ERROR SUMMARY: "
                if last_line[last_line.find(SUBSTR) + len(SUBSTR):][0] != '0':
                    return test_memory.MEMORY_ERROR
                return 0
            
            return test_memory.MEMORY_ERROR

        retcode = asyncio.run(memory_check())
        display_command = f"{MEMORY_CMD} {' '.join(args)}"
        self.assertFalse(retcode == test_memory.MEMORY_ERROR, f"There are memory leaks in your program for valgrind command '{display_command}'!")
        print("No leaks or errors!")