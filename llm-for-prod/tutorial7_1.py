from langchain.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser, StructuredOutputParser, ResponseSchema
from pydantic import BaseModel, Field, field_validator
from typing import List
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import dotenv

dotenv.load_dotenv()

class Suggestions(BaseModel):
    words: List[str] = Field(description="""list of substitute words based on context""")
    reasons: List[str] = Field(description="""the reasoning of why this word fits the context""")

    @field_validator('words')
    def not_start_with_number(cls, field):
        for item in field:
            if item[0].isnumeric():
                raise ValueError("The word can not start with numbers!")
        return field
    
    @field_validator('reasons')
    def end_with_dot(cls, field):
        for idx, item in enumerate(field):
            if item[-1] != '.':
                field[idx] += "."
        return field
    
# Example 1
parser = PydanticOutputParser(pydantic_object=Suggestions)

template = """
Offer a list of suggestions to substitute for the specified tartet_word based on the presented context and the reasoning for each word.
{format_instructions}
target_word={target_word}
context={context}
"""

target_word = "behavior"
context = "The behavior of the students in the classroom was disruptive and made it difficult for the teacher to conduct the lesson."

prompt_template = PromptTemplate(
    template=template,
    input_variables=["target_word", "context"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

model_name = 'gpt-3.5-turbo'
temperature = 0.0
model = ChatOpenAI(model_name=model_name, temperature=temperature)

chain = prompt_template | model | parser

output = chain.invoke({"target_word": target_word, "context": context})

print(output)

# Example 2

parser2 = CommaSeparatedListOutputParser()

template2 = """
Offer a list of suggestions to substitute for the specified tartet_word based on the presented context and the reasoning for each word.
{format_instructions}
target_word={target_word}
context={context}
"""

prompt_template2 = PromptTemplate(
    template=template2,
    input_variables=["target_word", "context"],
    partial_variables={"format_instructions": parser2.get_format_instructions()}
)

chain2 = prompt_template2 | model | parser2

output2 = chain2.invoke({"target_word": target_word, "context": context})
print("================")
print(output2)

# Example 3

print("================")

response_schemas = [
    ResponseSchema(name="words", description="A substitute word based on the context"),
    ResponseSchema(name="reasons", description="The reasoning of why this word fits the context")
]

parser3 = StructuredOutputParser(response_schemas=response_schemas)

chain3 = prompt_template | model | parser3

output3 = chain3.invoke({"target_word": target_word, "context": context})
print("================")
print(output3)

