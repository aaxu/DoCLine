import subprocess
import sys
import colorama
from bs4 import BeautifulSoup
import app.doc_websites
import app.web_scraper
from app.text import Text

def check_args():
    """
    Checks the arguments passed into the program from terminal. It will exit
    the program and display the appropriate message if not enough arguments
    were passed in or an unsupported language name was queried.

    Returns:
        None.
    """
    error_msg = ""
    if len(sys.argv) < 3:
        error_msg = ("WRONG FORMAT. You should pass in the programming" +
                     " langauge name as the first argument, a class as" +
                     " the second argument, and an optional method name" +
                     " in the third argument.")
    else:
        language, _ = get_query(sys.argv)
        if language not in app.doc_websites.websites:
            error_msg = ("Unfortunately, " +
                         Text.magenta_text(Text.magenta_text(language)) +
                         " is not a programming language that is currently" +
                         " supported by DoCLine. :(")
    if error_msg:
        print_doc(error_msg)
        exit(0)

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
    doc_text = Text(doc)
    print doc_text

def get_query(args):
    """
    Finds and returns the query that the user searched for. The name of the
    language should be the first word of the arguments passed into the program.
    Equivalently, it should be the second element in sys.argv since the first
    element is the program name.

    Args:
        args (list): A list of strings that represent the arguments passed into
                     the program. You can pass in sys.argv. Note that the first
                     argument should be the program name.

    Returns:
        A tuple containing (language_name, query) where language_name is the
        name of the programming language that the user is requesting and
        query is the documentation they want to search for in that language.
    """
    return (args[1].lower(), ' '.join(args[2:]).lower())

def main():
    """
    Main logic of the program.

    Returns:
        None.
    """
    colorama.init()
    check_args()
    language, query = get_query(sys.argv)
    doc_url = app.doc_websites.websites[language]
    google_search_url = app.web_scraper.query_to_google_url(query, doc_url)
    google_html = app.web_scraper.get_website_html(google_search_url)
    soup = BeautifulSoup(google_html, 'html.parser')
    first_res = soup.find_all('div', class_='g')[0]
    url = first_res.find('a')['href'] # May return URL with some header.
    url = app.web_scraper.fix_href_url(url) # Fix the URL.
    # Check if the website allows us to scrape it for information.
    if not app.web_scraper.website_allows_scraping(url):
        text = ("Unfortunately, the documentation website for " +
                Text.magenta_text(language) + " does not allow scraping." +
                "The program will now exit.")
        print text
        exit(0)
    doc_html = app.web_scraper.get_website_html(url)

if __name__ == '__main__':
    main()
