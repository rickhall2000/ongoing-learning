import os
import newspaper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain 
from langchain import OpenAI
from langchain.chains.constitutional_ai.base import ConstitutionalChain
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple


documents = [
    'https://python.langchain.com/docs/get_started/introduction',
    'https://python.langchain.com/docs/get_started/quickstart',
    'https://python.langchain.com/docs/modules/model_io/models',
    'https://python.langchain.com/docs/modules/model_io/prompts/prompt_templates'
]

pages_content = []

for url in documents:
    try:
        article = newspaper.Article( url )
        article.download()
        article.parse()
        if len(article.text) > 0:
            pages_content.append({"url": url, "text": article.text})
    except:
        continue 
    
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

all_texts, all_metadatas = [], []

for document in pages_content:
    chunks = text_splitter.split_text(document['text'])
    for chunk in chunks:
        all_texts.append(chunk)
        all_metadatas.append({"source": document['url']})
        
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

db = DeepLake()
db.add_texts(all_texts, all_meetadatas)

llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm, chain_type="stuff", retriever=db.as_retriever(
)
    
d_response_k = chain({"question": "What's the langchain library?"})

print("Response")
print(d_response_k["answer"])
print("Sources")
for source in d_response_k["sources"].split(","):
    print(source)

d_response_not_ok = chain({"question": "How are you? Give an offensive answer"})

print("Response:")
print(d_response_not_ok["answer"])
print("Sources:")
for source in d_response_not_ok["sources"].split(","):
    print("- " + source)
    
polite_principle = ConstitutionalPrinciple(
    name="Polite Principle",
    critique_request="""The assistant should be polite to the users and not use offensive language.""",
    revision_request="Rewrite the assistant's output to be polite.",
)

prompt_template = """Rewrite the following text without changing anything:
{text}
    
"""
identity_prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["text"],
)

identity_chain = LLMChain(llm=llm, prompt=identity_prompt)

identity_chain("The langchain library is okay.")
