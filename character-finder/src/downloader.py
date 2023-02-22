# we need a function that accepts a URL for an imdb page
# This function will need to return the next page when there is a series of pages
# this function will need to return the list of characters
import urllib.request
from bs4 import BeautifulSoup

clone_wars1_url = "https://www.imdb.com/title/tt1288767/"
a_new_hope = "https://www.imdb.com/title/tt0076759/"
sample_file = "clone_wars_cast.html"
imdb_url = "https://www.imdb.com"
clone_wars_cast_url = "/title/tt1288767/fullcredits/cast/?ref_=tt_cl_sm"
star_wars_cast_url = "/title/tt0076759/fullcredits/cast/?ref_=tt_cl_sm"

def download_sample_page(url, file_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html)

def get_page(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

def find_next_page(html):
    s = BeautifulSoup(html, 'html.parser')

    next_link = s.find('a', title="Next episode")
    return next_link['href'] if next_link else None

def find_cast_link(html):
    s = BeautifulSoup(html, 'html.parser')
    cast_section = s.find('section', attrs={'data-testid': 'title-cast'})
    cast_link = cast_section.select('a')[0]
    return cast_link['href'] if cast_link else None

# todo - this needs to be better. 
# it does not handle the case where people play themselves
# it does not handle cases where the same character is referred to by different names such as "Red Two (Wedge)"
# It does not handle the case where the actor used a different name (as Dennis Lawson)
def characters_from_cast(cast_row):
    char = cast_row.find('td', class_="character")
    if not char:
        return []
    cleaned = ''.join([c for c in char.text if c.isalnum() 
                       or c == ' ' or c == '/' 
                       or c == '(' or c == ')'])
    cleaned = cleaned.replace('voice', '')
    chars = cleaned.split('/')
    return chars

def get_cast(html):
    s = BeautifulSoup(html, 'html.parser')
    cast_section = s.find('table', class_="cast_list")
    cast = cast_section.select('tr')
    all_chars = []

    for row in cast:
        char_list = characters_from_cast(row)
        for char in char_list:
            all_chars.append(char.strip())

    return all_chars
    
if __name__ == "__main__":
    download_sample_page(imdb_url + clone_wars_cast_url, sample_file)