import os 

import requests
from newspaper import Article
import time
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'''
}

article_urls = [
    """https://www.artificialintelligence-news.com/2023/05/23/meta-open-source-speech-ai-models-support-over-1100-languages/""",
    """https://www.artificialintelligence-news.com/2023/05/18/beijing-launches-campaign-against-ai-generated-misinformation/"""
    """https://www.artificialintelligence-news.com/2023/05/16/openai-ceo-ai-regulation-is-essential/""",
    """https://www.artificialintelligence-news.com/2023/05/15/jay-migliaccio-ibm-watson-on-leveraging-ai-to-improve-productivity/""",
    """https://www.artificialintelligence-news.com/2023/05/15/iurii-milovanov-softserve-how-ai-ml-is-helping-boost-innovation-and-personalisation/""",
    """https://www.artificialintelligence-news.com/2023/05/11/ai-and-big-data-expo-north-america-begins-in-less-than-one-week/""",
    """https://www.artificialintelligence-news.com/2023/05/11/eu-committees-green-light-ai-act/""",
    """https://www.artificialintelligence-news.com/2023/05/09/wozniak-warns-ai-will-power-next-gen-scams/""",
    """https://www.artificialintelligence-news.com/2023/05/09/infocepts-ceo-shashank-garg-on-the-da-market-shifts-and-impact-of-ai-on-data-analytics/""",
    """https://www.artificialintelligence-news.com/2023/05/02/ai-godfather-warns-dangers-and-quits-google/""",
    """https://www.artificialintelligence-news.com/2023/04/28/palantir-demos-how-ai-can-used-military/""",
    """https://www.artificialintelligence-news.com/2023/04/26/ftc-chairwoman-no-ai-exemption-to-existing-laws/""",
    """https://www.artificialintelligence-news.com/2023/04/24/bill-gates-ai-teaching-kids-literacy-within-18-months/""",
    """https://www.artificialintelligence-news.com/2023/04/21/google-creates-new-ai-division-to-challenge-openai/"""
]

session = requests.Session()
pages_content = []

for url in article_urls:
    try:
        time.sleep(2)
        response = session.get(url, headers=headers, timeout = 10)
        
        if response.status_code == 200:
            article = Article(url)
            article.download(input_html=response.text)
            article.parse()
            pages_content.append(article.text)
        else:
            print(f"Failed to retrieve {url}: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

db = DeepLake(embedding_function=embeddings)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

all_texts = []
for d in pages_content:
    chunks = text_splitter.split_text(d["text"])
    for chunk in chunks:
        all_texts.append(chunk)
        
db.add_texts(all_texts)

retriever = db.as_retriever()
retriever.search_kwargs["k"] = 3

CUSTOM_TOOL_DOCS_SEPARATOR = "\n--------\n"

def retrieve_n_docs_tool(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    texts = [doc.page_content for doc in docs]
    texts_merged = "--------\n" + CUSTOM_TOOL_DOCS_SEPARATOR.join(texts) + "\n--------"
    return texts_merged

tools = [
    Tool(
        name="Search Private Docs",
        func=retrieve_n_docs_tool,
        description="Use this tool to retrieve relevant documents from the private knowledge base. The documents are separated by '--------'.",
    )
]

model = ChatOpenAI(model="gpt-4o", temperature=0)
planner = load_chat_planner(model=model)
executor = load_agent_executor(model=model, tools=tools, verbose=True)
agent = PlanAndExecute(planner=planner, excutor=executor, verbose=True)

response = agent.run("Write an overview of Artifical Intelligence regulations by governments by country")
