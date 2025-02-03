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

BULLET_POINT_PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["text"])

chain = load_summarize_chain(llm,
                             chain_type="stuff",
                             prompt=BULLET_POINT_PROMPT)

output_summary = chain.run(docs)

wrapped_text=textwrap.fill(output_summary,
                           width=1000,
                           break_long_words=False,
                           replace_whitespace=False)

chain = load_summarize_chain(llm, chain_type="refine")
output_summary = chain.run(docs)
wrapped_text = textwrap.fill(output_summary, width=100)
print(wrapped_text)

def downnload_mp4_from_youtube(urls, job_id):
    video_info = []
    for i, url in enumberate(urls):
        file_temp = f'./{job_id}_{i}.mp4'
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m3a]/best[ext=mp3]',
            outtmpl: file_temp,
            'quiet': True,
        }
        
        with wt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.exrract_info(url, download=True)
            title = result.get('title', "")
            author = result.get('uploader', "")
            
        video_info.append((file_temp, title, author))
    
    return video_info

urls=['https://www.youtube.com/watch?v=mBjPyte2XZ0&t=78s']
video_details = download_mp4_from_youtube(urls, 1)

model = whisper.load_model("base")

results = []
for video in video_details:
    result = model.transcribe(video[0])
    results.append(result['text'])
    print(f"Transcription for {video[0]}:\n{result['text']}\n")
    
with open("text.txt", "w") as f:
    f.write(results['text'])

with open('text.txt') as f:
    text = f.read()
texts = text_splitter.split_text(text)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=0,
    separators=[" ", ",", "\n"]
)
texts = text_splitter.split_text(text)

docs = [Document(page_content=t) for t in texts[:4]]

embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings)
db.add_documents(docs)

retriever = db.as_retriever()
retriever.search_kwargs['distance_metric']= 'cos'
retriever.search_kwargs['k'] = 4

prompt_template = """Use the following pieces of transcripts from a video to answer the question in bullet points and summarized. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Summarized answer in bullter points:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=retriever,
                                 chain_type_kwargs=chain_type_kwargs)
print(qa.run("Summarize the mentions of google according to their AI program"))

