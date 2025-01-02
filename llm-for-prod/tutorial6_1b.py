import os
import dotenv

dotenv.load_dotenv(".env")

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, 
                  api_key=os.getenv("OPENAI_API_KEY"))

summarize_chain = load_summarize_chain(llm)

document_loader = PyPDFLoader("data/the_cask_of_amontillado.pdf")
document = document_loader.load()

summary = summarize_chain.invoke(document)

print(summary["output_text"])
