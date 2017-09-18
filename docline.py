import sys
import requests
import urllib
from reppy.robots import Robots
from bs4 import BeautifulSoup

USER_AGENT = "DoCLine Parser (http://github.com/aaxu/docline)"

def check_website_policy(url):
    """
    Args:
        url: The URL of the website you are trying to check.

    Returns:
        True if the website's policy allows you to scrape. Otherwise False.
    """
    robot_url = Robots.robots_url(doc_website)
    robot = Robots.fetch(robot_url)
    return robot.allowed(doc_website, USER_AGENT)

doc_website = "http://docs.python.org/2/"
doc_search_url = "https://docs.python.org/2/search.html?q="
if len(sys.argv) > 1:
    args = sys.argv[1:]
    query = " ".join(args)
    encoded_query = urllib.quote_plus(query)
    search_url = doc_search_url + encoded_query
    search_res = requests.get(search_url)
    soup = BeautifulSoup(search_res.text, 'html.parser')
    print search_url
else:
    exit(0)
