import unittest, sys, os
from bs4 import BeautifulSoup, SoupStrainer
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import requests
from req_scrape import BreadthParser

class TestBreadthParser(unittest.TestCase):
    def setUp(self):
        al_file = open(os.path.dirname(__file__) + "/saved_endpoints/breadth-al.html")
        self.al_html = al_file.read()
        self.al_parser = BreadthParser("arts-literature")

        self.al_soup = BeautifulSoup(self.al_html, 'lxml', parse_only=SoupStrainer(['tr']))

        self.al_soup = self.al_parser.setup_soup('arts-literature')
        self.al_req_dict = self.al_parser.make_req_dict(self.al_soup, 'arts-literature', 'al')

    def test_saved_al(self):
        self.assertTrue('AFRICAM' in self.al_req_dict)
        self.assertEqual(len(self.al_req_dict['AFRICAM']), 16)

    def test_comp_curr_saved_al(self):



if __name__=='__main__':
    unittest.main()