# Not installing anything, so this program will not work

import os 
import requests
from bs4 import BeautifulSoup
from langchain.embeddings.openai import OpenAIEmbeddings
from langcahin.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import re 

emeddings = OpenAIEmbeddings(model_name="text-embedding-ada-002")

def get_documentation_urls():
    # List of relative URLs for Hugging Face documentation pages,
    # commented a lot of these because it would take too long to scrape
    # all of them
    return [
            '/docs/huggingface_hub/guides/overview',
            '/docs/huggingface_hub/guides/download',
            '/docs/huggingface_hub/guides/upload',
            '/docs/huggingface_hub/guides/hf_file_system',
            '/docs/huggingface_hub/guides/repository',
            '/docs/huggingface_hub/guides/search',
            # You may add additional URLs here or replace all of them
    ]

def construct_full_url(base_url, relative_url):
    # Construct the full URL by appending the relative URL to the base URL
    return base_url + relative_url

def scrape_page_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.body.text.strip()
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\xff]', '', text)

def scrape_all_content(base_url, relative_urls, filename):
    # Loop through the list of URLs, scrape content and add it to the
    # content list
    content = []
    for relative_url in relative_urls:
        full_url = construct_full_url(base_url, relative_url)
        scraped_content = scrape_page_content(full_url)
        content.append(scraped_content.rstrip('\n'))

    # Write the scraped content to a file
    with open(filename, 'w', encoding='utf-8') as file:
        for item in content:
            file.write("%s\n" % item)
    
    return content

def load_docs(root_dir, filename):
    docs = []
    try:
        loader = TextLoader(os.path.join(root_dir, filename), encoding='utf-8')
        docs.extend(loader.load_and_split())
    except Exception as e:
        pass
    return docs

def split_docs(docs):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(docs)

def main():
    base_url = 'https://huggingface.co'
    relative_urls = get_documentation_urls()
    filename = 'content.txt'

    root_dir = "./"
    relative_urls = get_documentation_urls()
    
    content = scrape_all_content(base_url, relative_urls, filename)
    
    docs = load_docs(root_dir, filename)
    
    texts = split_docs(docs)
    
    db = DeepLake(dataset_path=dataset_path, embedding_function=emeddings, overwrite=True)
    db.add_documents(texts)
    os.remove(filename)
    
if __name__ == "__main__":
    main()
    
    