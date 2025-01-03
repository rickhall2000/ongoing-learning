import json 
import os
import dotenv
import requests
from newspaper import Article
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'''
}

article_url = """https://www.artificialintelligence-news.com/2022/01/25/meta-claims-new-ai-supercomputer-will-set-records/"""

session = requests.Session()

try:
    response = session.get(article_url, headers=headers, timeout=10)

    if response.status_code == 200:
        article = Article(article_url)
        article.download()
        article.parse()

        print(f"Title: {article.title}")
        print(article.text)


    else:
        print(f"failed to fetch article at {article_url}")
except Exception as e:
    print(f"An error occurred: {e}")


def summarize_article(article):

    template = """You are a very good assistant that summarizes online articles into bulleted lists in french.
    
    Here is the article you want to summarize.
    
    ====================
    Title: {article_title}
    {article_text}
    ====================

    write a summary of the previous article.
    """

    prompt = template.format(article_title=article.title, article_text=article.text)
    messages = [HumanMessage(content=prompt)]
    response = chat.invoke(messages)
    return response.content

print("================================================")
print("SUMMARY")
print("================================================")
print(summarize_article(article))
