import os
import sys
import subprocess
import textwrap
from reppy.robots import Robots

USER_AGENT = 'DoCLine Parser (http://github.com/aaxu/docline)'

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

def main():
    command = sys.argv
    sys.argv[0] = 'pydoc'
    text_wrapper = textwrap.TextWrapper(replace_whitespace=False,
                                        width=120)
    output = text_wrapper.fill(subprocess.check_output(command))
    output = output.replace("\n", "\n    ")
    print output
    while 1:
        rows, columns = os.popen('stty size', 'r').read().split()
        print rows, columns

if __name__ == '__main__':
    main()
