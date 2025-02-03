import os
import dotenv
import yt_dlp
import whisper
from openai import OpenAI
from langchain.chains import LLMChain
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chains import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import textwrap
dotenv.load_env()

# The library this needed messed up my machine, so I uninstalled it. This program won't work.

def download_mp4_from_youtube(url):
    filename = 'lecuninterview.mp4'
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': filename,
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)

url = "https://www.youtube.com/watch?v=mBjPyte2ZZo"
download_mp4_from_youtube(url)

model = whisper.load_model("base")
result = model.transcribe("lecuninterview.mp4")
print(result["text"])

with open("text.txt", "w") as f:
    f.write(result["text"])

llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                               chunk_overlap=200,
                                               separators=[" ", ",", "\n"])

with open('text.txt', 'r') as file:
    text = file.read()

texts = text_splitter.split_text(text)
docs = [Document(page_content=t) for t in texts[:4]]

chain = load_summarize_chain(llm, chain_type="map_reduce")

output_summary =chain.run(docs)
wrapped_text = textwrap.fill(output_summary, width=100)
print(wrapped_text)

