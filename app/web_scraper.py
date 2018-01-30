import urllib
import urlparse
import requests
from reppy.robots import Robots
USER_AGENT = 'DoCLine Parser (http://github.com/aaxu/docline)'
GOOGLE_SEARCH_URL = "http://www.google.com/search?q=site:"

def get_website_html(url):
    """
    Args:
        url (str): The URL of the website you want to extract the HTML from.

    Returns:
        A string containing all the HTML from url. If a connection error was
        encountered, it will output a helpful error message and exit the
        program.
    """
    try:
        return requests.get(url).text
    except requests.exceptions.ConnectionError:
        from text import Text
        print(Text.red_text("A connection error was encountered. " +
                            "Please check your internet connection and " +
                            "try again."))
        exit(0)


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

def fix_href_url(url):
    """
    Args:
        url (str): A href url extracted from HTML code.

    Retuerns:
        The URL that can be sent a request to in order to access the site.
    """
    url = urlparse.urlparse(url).query # Removes the URL query header
    return urlparse.parse_qs(url)["q"][0] # Returns the query URL
