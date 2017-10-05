import subprocess
import sys
import colorama
import app.web_scraper
from app import text

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
    return (args[1], ' '.join(args[2:]))

def main():
    """
    Main logic of the program.

    Returns:
        None.
    """
    if len(sys.argv) < 3:
        print "Wrong format. You should pass in the programming langauge name" \
              "as the first argument, a class as the second argument, and" \
              "an optional method in the third argument."
        exit(0)
    colorama.init()
    args = get_query(sys.argv)
    python_doc_url = 'https://docs.python.org/2/'
    if app.web_scraper.website_allows_scraping(python_doc_url):
        print python_doc_url + " allows scraping."

if __name__ == '__main__':
    main()
