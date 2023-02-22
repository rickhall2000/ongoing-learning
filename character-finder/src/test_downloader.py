import unittest
import downloader as d

star_wars_file = "star_wars_iv.html"
clone_wars1_file = "clone_wars1.html"
clone_wars2_url = "/title/tt1288768/?ref_=tt_ep_nx"
clone_wars_cast_url = "/title/tt1288767/fullcredits/cast/?ref_=tt_cl_sm"
star_wars_cast_url = "/title/tt0076759/fullcredits/cast/?ref_=tt_cl_sm"
clone_wars_cast_file = "clone_wars_cast.html"
star_wars_cast_file = "star_wars_cast.html"

imdb_url = "https://www.imdb.com"

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
        
class test_get_cast(unittest.TestCase):
    def test_gets_cast_from_clonewars(self):
        with open(clone_wars_cast_file, 'r', encoding='utf-8') as file:
            html = file.read()
        self.assertEqual(10, len(d.get_cast(html)))
    def test_gets_cast_from_starwars(self):
        with open(star_wars_cast_file, 'r', encoding='utf-8') as file:
            html = file.read()
        self.assertEqual(115, len(d.get_cast(html)))
        
if __name__ == '__main__':
    unittest.main()        