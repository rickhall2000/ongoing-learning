import os
import dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.document_loaders import SeleniumURLLoader
from langchain import PromptTemplate


## This won't run. I don't have deep lake account.

dotenv.load_dotenv()

# we'll use information from the following articles
urls = ['https://beebom.com/what-is-nft-explained/',
        'https://beebom.com/how-delete-spotify-account/',
        'https://beebom.com/how-download-gif-twitter/',
        'https://beebom.com/how-use-chatgpt-linux-terminal/',
        'https://beebom.com/how-delete-spotify-account/',
        'https://beebom.com/how-save-instagram-story-with-music/',
        'https://beebom.com/how-install-pip-windows/',
        'https://beebom.com/how-check-disk-usage-linux/']

loader = SeleniumURLLoader(urls=urls)
docs_not_splitted = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(docs_not_splitted)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

db = DeepLake(dataset_path="deeplake-db", embedding=embeddings)

db.add_documents(docs)

query = "how to check disk usage in linux?"
docs = db.similarity_search(query)

print(docs[0].page_content)

template = """You are an exceptional customer support chatbot that gently answers questions

You know the following context information.

{chunks_formatted}

Answer the following question from a customer. Use only information from the previous context information. Do not invent stuff.


Question: {query}


Answer:"""


prompt = PromptTemplate(
    input_variables=["chunks_formatted", "query"],
    template=template
)

retrieved_chunks = [doc.page_content for doc in docs]

chunks_formatted = "\n\n".join(retrieved_chunks)

prompt_formatted = prompt.format(chunks_formatted=chunks_formatted, query=query)

llm = OpenAI(model="gpt-3.5-turbo")

response = llm.invoke(prompt_formatted)

print(response)

