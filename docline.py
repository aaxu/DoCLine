import sys
import subprocess
import colorama
import text
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

def get_doc():
    """
    Returns:
        The requested documentation as a string.
    """
    sys.argv[0] = 'pydoc'
    return subprocess.check_output(sys.argv)

def print_doc(doc):
    """
    Args:
        doc: A string representation of documentation.

    Returns:
        None. Prints out the documentation in a readable and colored format.
    """
    doc_text = text.Text(doc)
    print doc_text

def main():
    """
    Main logic of the program.

    Returns:
        None.
    """
    doc = get_doc()
    print_doc(doc)

if __name__ == '__main__':
    colorama.init()
    main()
