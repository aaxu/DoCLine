import os
import re
import sys
import subprocess
import textwrap
from reppy.robots import Robots

USER_AGENT = 'DoCLine Parser (http://github.com/aaxu/docline)'
INDENTATION = " " * 4
_, columns = os.popen('stty size', 'r').read().split()
COLUMNS = int(columns)

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
    formatted_line = line.strip()
    if formatted_line == '' or formatted_line == None:
        return []
    formatted_line = line_indentation + formatted_line
    if len(formatted_line) <= COLUMNS - margin_right:
        return [formatted_line]
    break_line_at_index = COLUMNS - margin_right
    while (not formatted_line[break_line_at_index].isspace() and
           break_line_at_index >= len(line_indentation)):
        break_line_at_index -= 1
    # Case for one really long word
    if break_line_at_index < len(line_indentation):
        break_line_at_index = COLUMNS - margin_right
    output.append(formatted_line[:break_line_at_index])
    leftover_string = formatted_line[break_line_at_index:]
    output.extend(format_line(leftover_string, INDENTATION))
    return output



def main():
    command = sys.argv
    sys.argv[0] = 'pydoc'
    output = subprocess.check_output(command).split('\n')
    formatted_text = []
    for line in output:
        formatted_text.extend(format_line(line, ""))

    formatted_text = "\n".join(formatted_text)
    formatted_text = re.sub(r'[|]', '  ', formatted_text)
    print formatted_text

if __name__ == '__main__':
    main()
