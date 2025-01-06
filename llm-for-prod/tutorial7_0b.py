import os
import dotenv

from langchain.chains import LLMChain
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, 
                  api_key=os.getenv("OPENAI_API_KEY"))


examples = [
    {"animal": "lion", "habitat": "savannah"},
    {"animal": "elephant", "habitat": "savannah"},
    {"animal": "penguin", "habitat": "antarctica"},
    {"animal": "kangaroo", "habitat": "australia"},
]

example_template = """
Animial: {animal}
Habitat: {habitat}
"""

example_prompt = PromptTemplate(
    input_variables=["animal", "habitat"],
    template=example_template
)

dynamic_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Identify the habitat of the following animal",
    suffix="Animal: {input}\nHabitat:",
    input_variables=["input"],
    example_separator="\n\n"
)

chain = dynamic_prompt | llm

input_data = {"input": "tiger"}

response = chain.invoke(input_data)

print(response.content)

