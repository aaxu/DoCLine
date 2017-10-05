import subprocess
COMMAND_RUN_TESTS = "python -m unittest discover -s tests/ -p unit_test*.py"

if __name__ == '__main__':
    # Runs all test in the test/ directory. The file names must be of the form
    # unit_test_TEST_NAME.py.
    command_list = COMMAND_RUN_TESTS.split(' ')
    subprocess.call(command_list)