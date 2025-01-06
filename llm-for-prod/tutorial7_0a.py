import os
import dotenv

from langchain.chains import LLMChain
from langchain_core.prompts import  PromptTemplate 
from langchain_openai import ChatOpenAI

dotenv.load_dotenv(".env")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, 
                  api_key=os.getenv("OPENAI_API_KEY"))

template = """Answer the question based on the context below. If the 
question cannot be answered using the information provided, answer with "I don't know".
Context: Quatnum computing is an emerging field that leverages quantum me-
chanics to solve complex problems faster than classical computers.
...
Question: {query}
Answer:"""

prompt_template = PromptTemplate(
    input_variables=["query"],
    template=template
)

chain = prompt_template | llm 

input_data = {"query": "What is the main advantage of quantum computing over classical computing?"}

response = chain.invoke(input_data)

print("Question: ", input_data["query"])
print("Answer: ", response)