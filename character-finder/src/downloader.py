# we need a function that accepts a URL for an imdb page
# This function will need to return the next page when there is a series of pages
# this function will need to return the list of characters
import urllib.request

sample_url = "https://www.imdb.com/title/tt1288767/"
#sample_url "https://rickslearning.com"
next_url = "https://www.imdb.com/title/tt1288768/?ref_=tt_ep_nx"
sample_file = "sample_page.html"

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
        
        
if __name__ == "__main__":
    download_sample_page(sample_url, sample_file)