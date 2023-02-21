# we need a function that accepts a URL for an imdb page
# This function will need to return the next page when there is a series of pages
# this function will need to return the list of characters
import urllib.request
from bs4 import BeautifulSoup

clone_wars1_url = "https://www.imdb.com/title/tt1288767/"
a_new_hope = "https://www.imdb.com/title/tt0076759/"
sample_file = "star_wars_iv.html"

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
    
if __name__ == "__main__":
    download_sample_page(a_new_hope, sample_file)