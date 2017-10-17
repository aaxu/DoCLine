import unittest
import sys
sys.path.append("../")
import app.web_scraper

class WebScraperTestCases(unittest.TestCase):
    def test_get_google_url(self):
        query = 'dict setdefault'
        site = 'https://docs.python.org/2/'
        expected = ("http://www.google.com/search?q=site:" +
                    site + "+dict+setdefault")
        self.assertEqual(app.web_scraper.query_to_google_url(query, site),
                         expected)

# This file currently only runs if you are in to root directory of this
# project. It will not work if you are in the docline/tests directory.
# Use the unit_tests.py file instead.
if __name__ == '__main__':
    unittest.main()