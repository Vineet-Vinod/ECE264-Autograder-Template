# AutoGrader Template: Guide
The autograder may look intimidating at first, but this guide should clear most questions up. 
The files themselves also contain useful comments on how to configure the autograder. The purpose of this README is to give a clear path on which order to complete which files.

## Files you (probably) don't need to modify
- `setup.sh`: This file installs gcc and valgrind, as well as the python libraries in requirements.txt.
- `run_tests.py`: This file runs all the tests and stores them in the expected JSON format.
- `requirements.txt`: Holds python libraries that are pip installed by `setup.sh`.


> ***Note***: If you cloned the repository with `git clone`, it's recommended to remove the `.git` file in order to prevent accidentally pushing changes to the autograder template.

## Steps
### 1. Replace `starter_code` files and update `run_autograder`
`starter_code.c` and `starter_code.h` files are placeholders for any constant files that do not need to be changed at all by the students. This removes the hassle of having students submit them themselves and ensures each student's program is run with the correct supporting files.

In general:
- `starter_code.c` is the file that will run the students' functions if they do not make their own main (typically this is `main.c`)
- `starter_code.h` is the header file that is used by the student file and or main file (ex: `count_words.h` for the count words homework)

Next, ensure that `STUDENT_C_FILE` in `run_autograder` is updated with the student C file name (ex: `STUDENT_C_FILE="count_words.c"`).

### 2. Upload Inputs and Expected Outputs
There are two folders that the tests may use: `expected` and `inputs`. As their names suggest, put the expected files in the expected folder and the input files (if the assignment reads from an input file) in the inputs folder. If you want to add hidden test cases, place them here - students will not have access to these folders. You can remove the `.gitkeep` files.

> Student submissions do not need to write their programs out to file, as the autograder will compare the file with what is written to `stdout`. This behavior can be changed if the student script is expected to produce files.

### 3. Modify `test_files.py`
On line 11, modify the list found in the `check_submitted_files` function call to contain the files the students should submit. For example, if the students were told to submit `count_words.c` and `count_words.h`, then the line would be:
```
for path in (missing_files := check_submitted_files(["count_words.c", "count_words.h"])):
```
These should be the files that the students modified. Don't ask students to submit a file that they will not change at all. Place all constant files in the autograder directory as done in step 1.

No other lines need to be modified in this file.

### 4. Modify `test_gcc.py`
This file contains the gcc command that is run. Modify the corresponding variables accordingly. Below is an example from the count words words homework (hw03):
```
FILES = "count_words.c main.c"
EXEC = "hw03"
GCC = f"gcc -std=c11 -g -Wall -Wshadow --pedantic -Wvla -Werror"
COMMAND = f"{GCC} {FILES} -o {EXEC}"
```
These four lines should be the only ones that need modifying in this file.

### 5. Modify `test_memory.py`
This file runs the memory test with valgrind. Only line 20 needs to be modified. This file runs valgrind on a _single testcase_, so choose one that you think is the best given the context of the assignment. This typically is the largest testcase. Below is an example that will run valgrind on test9 in the inputs folder:
```
MEMORY_CMD = f"./{EXEC} inputs/test9"
```
This is most likely the only line that will need modifying in this file.

### 6. Modify `test_output.py`
This function may not be as straightforward to implement as the rest depending on how you are processing your assignment. Typically, the only thing that will be needed to modify is line 60 (the command_line_arguments list). This is a 2D list, where each list contains the command line arguments in order ***except for the last element of the list***. The last element is the name of the expected output file in the `expected/` folder. You do not need the `expected/` prefix when accessing a file in the expected folder. However, you do need the `inputs/` prefix if accessing a file in the inputs folder.

If you're confused. Consider the following case:
- The expected test case is in `expected/expected_out1.txt`
- The program takes in two commmand line arguments, such as `./prog input_file.txt 15`
- The input file that corresponds to `expected_out1.txt` is found in `inputs/input1.txt`
- Then, command line arguments would be:
```
command_line_arguments = [["inputs/input1.txt", "15", "expected_out1.txt"]]
```

If you're still confused, here is the `command_line_arguments` for hw03 count words:
```
command_line_arguments = [["inputs/test1", "aa", "expected1"], 
                          ["inputs/test2", "abc", "expected2"],
                          ["inputs/test3", "I", "expected3"],
                          ["inputs/test4", "and", "expected4"],
                          ["inputs/test5", "clock", "expected5"],
                          ["inputs/test6", "pink", "expected6"],
                          ["inputs/test7", "noodle", "expected7"],
                          ["inputs/test8", "lucky", "expected8"],
                          ["inputs/test9", "vial", "expected9"]]
```

> ***IMPORTANT***: Within the `test` function, line 41 states:
> ```
> if expected.read() != result.stdout:
> ```
> This may need to be altered if the program output is not being printed to stdout.

### 7. Modify `weights.py`
This file stores the weights of each test. They should add up to 100 (TEST_OUTPUT is already written such that this will be true). Below is a description of each.
- TEST_GCC: If the program compiles, `TEST_GCC` points are awarded. Typically weighted at 10.
- TEST_FILES: If there are no missing files as described in `test_files.py`, `TEST_FILES` points are awarded. Typically weighted at 10.
- TEST_MEMORY: If the memory command found in `test_memory.py` passes with no leaks, `TEST_MEMORY` points are awarded. Typically weighted at 20.
- TEST_OUTPUT: Awards `TEST_OUTPUT * num_tests_passed / num_tests` points. Typically weighted at 60.

> ***Note***: This is your assignment, choose weights that make the most sense given how you want them to be graded.

> Also, Be aware that a student can submit a file with no logic implemented and it will pass TEST_GCC, TEST_FILES, and TEST_MEMORY. With the typical values above, this gives them 40 points for no work!

### 8. Upload the Autograder to Gradescope
Gradescope expects the autograder to be given as a zip file. This can be done by, within the autograder directory, running:
```
zip -r hw##-autograder.zip .
```
This zips all files in the current directory. To upload the zip file, navigate to the 264 Gradescope -> click on the assignment you want to upload the autograder to -> click Configure Autograder on the left side -> Upload Autograder. 

The autograder may take a second (or minute) (or two) to build.

## Updates
### April 29, 2025
- Replace `subprocess.run(...)` calls, which are synchronous, with their async counterparts in the asyncio library. This gives us more fine-grained control over program timeout (better than Gradescope's 10 minute minimum).
### April 30, 2025
- Add logic in `test_memory.py` to catch memory errors and deduct points (previously, if there were memory errors but no memory leaks, the submission would be awarded full points).