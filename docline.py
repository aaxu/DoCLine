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

def format_line(line):
    """
    Takes in a string and returns a list of strings such that they
    fit nicely on the terminal screen.
    Args:
        line: The line you want to format.

    Returns:
        A list of strings that you can print consecutively to output
        a nicely formatted text.
    """
    output = []
    formatted_line = line.strip()
    if len(formatted_line) <= COLUMNS:
        return [formatted_line]
    break_line_at_index = COLUMNS
    while not (formatted_line[break_line_at_index].isspace() and
                       break_line_at_index > 0):
        break_line_at_index -= 1
    if break_line_at_index > 0:
        output.append(formatted_line[0:break_line_at_index])
        leftover_string = INDENTATION + formatted_line[break_line_at_index:]
        output.extend(format_line(leftover_string))
    return output



def main():
    command = sys.argv
    sys.argv[0] = 'pydoc'
    text_wrapper = textwrap.TextWrapper(replace_whitespace=False,
                                        width=COLUMNS)
    output = text_wrapper.fill(subprocess.check_output(command)).split("\n")
    formatted_text = []
    for line in output:
        formatted_text.extend(format_line(line))

    # output = re.sub(r'[|]', ' ', output)
    print "\n".join(formatted_text)

if __name__ == '__main__':
    main()
