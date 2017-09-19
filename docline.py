import sys
import subprocess
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
    process = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    print process.communicate()

if __name__ == '__main__':
    main()
