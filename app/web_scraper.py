import urllib
from reppy.robots import Robots
USER_AGENT = 'DoCLine Parser (http://github.com/aaxu/docline)'
GOOGLE_SEARCH_URL = "http://www.google.com/search?q=site:"

def website_allows_scraping(url):
    """
    Args:
        url: The URL of the website you are trying to check.

    Returns:
        True if the website's policy allows you to scrape. Otherwise False.
    """
    robot_url = Robots.robots_url(url)
    robot = Robots.fetch(robot_url)
    return robot.allowed(url, USER_AGENT)

def query_to_google_url(query, website=''):
    """
    Args:
        query (list of strings): The query you want to search for on google.

    Returns:
        The associated google URL that searches for the query.
    """
    return GOOGLE_SEARCH_URL + website + '+' + urllib.quote_plus(query)
