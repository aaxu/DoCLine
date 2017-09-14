import robotparser
import requests
from bs4 import BeautifulSoup

def url_to_roboturl(url):
    pass

example_search = requests.get("http://docs.python.org/2/")
my_robot_parser = robotparser.RobotFileParser("https://docs.python.org/2/")
soup = BeautifulSoup(example_search.text, 'html.parser')
print(soup)
