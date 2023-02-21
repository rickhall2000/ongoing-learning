import unittest
import downloader as d

star_wars_file = "star_wars_iv.html"
clone_wars1_file = "clone_wars1.html"
clone_wars2_url = "/title/tt1288768/?ref_=tt_ep_nx"


class test_cast_link_finder(unittest.TestCase):
    def test_find_clonewars_cast(self):
        with open(clone_wars1_file, 'r', encoding='utf-8') as file:
            html = file.read()
        self.assertEqual('/title/tt1288767/fullcredits/cast/?ref_=tt_cl_sm', d.find_cast_link(html))
    def test_find_starwars_cast(self):
        with open(star_wars_file, 'r', encoding='utf-8') as file:
            html = file.read()
        self.assertEqual('/title/tt0076759/fullcredits/cast/?ref_=tt_cl_sm', d.find_cast_link(html))
    
class test_next_finder(unittest.TestCase):
    def test_no_next_found_when_doesnt_exist(self):
        with open(star_wars_file, 'r', encoding='utf-8') as file:
            html = file.read()
        self.assertEqual(None, d.find_next_page(html))
    
    def test_finds_next_when_does_exist(self):
        with open(clone_wars1_file, 'r', encoding='utf-8') as file:
            html = file.read()
        self.assertEqual(clone_wars2_url, d.find_next_page(html))    
        
if __name__ == '__main__':
    unittest.main()        