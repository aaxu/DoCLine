import os
import re
import sys
import subprocess
from reppy.robots import Robots

USER_AGENT = 'DoCLine Parser (http://github.com/aaxu/docline)'
INDENTATION = " " * 4
ROWS, COLUMNS = [int(dim) for dim in
                 (os.popen('stty size', 'r').read().split())]

def check_website_policy(url):
    """
    Args:
        url: The URL of the website you are trying to check.

    Returns:
        True if the website's policy allows you to scrape. Otherwise False.
    """
    robot_url = Robots.robots_url(url)
    robot = Robots.fetch(robot_url)
    return robot.allowed(url, USER_AGENT)

def format_line(line, line_indentation):
    """
    Takes in a string and returns a list of strings such that they
    fit nicely on the terminal screen.
    Args:
        line: The line you want to format.
        line_indentation: The string indentation that a line should
                          take when the line wraps around the screen.

    Returns:
        A list of strings that you can print consecutively to output
        a nicely formatted text.
    """
    output = []
    margin_right = 3
    # Don't strip the first line, since it may be already formatted.
    if line_indentation:
        line = line.strip()
    if not line:
        return []
    line = line_indentation + line
    if len(line) <= COLUMNS - margin_right:
        return [line]
    break_line_at_index = COLUMNS - margin_right
    while (not line[break_line_at_index].isspace() and
           break_line_at_index >= len(line_indentation)):
        break_line_at_index -= 1
    # Case for one really long word
    if break_line_at_index < len(line_indentation):
        break_line_at_index = COLUMNS - margin_right
    output.append(line[:break_line_at_index])
    leftover_string = line[break_line_at_index:]
    output.extend(format_line(leftover_string, INDENTATION))
    return output



def main():
    """
    Main logic of the program.

    Returns:
        None.
    """
    command = sys.argv
    sys.argv[0] = 'pydoc'
    output = subprocess.check_output(command).split('\n')
    formatted_text = []
    for line in output:
        formatted_text.extend(format_line(line, ""))

    output = "\n".join(formatted_text)
    output = re.sub(r'[|]', '  ', formatted_text)
    print output

if __name__ == '__main__':
    main()
