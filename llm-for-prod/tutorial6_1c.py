import os
import dotenv

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

dotenv.load_dotenv(".env")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, 
                  api_key=os.getenv("OPENAI_API_KEY"))

prompt = PromptTemplate(template="Question: {question}\nAnswer: ", input_variables=["question"])

chain = prompt | llm

result = chain.invoke({"question": "What is the meaning of life?"})

print(result)