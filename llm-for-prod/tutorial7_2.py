import os 
import json
import dotenv
import requests
from newspaper import Article
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from pydantic import field_validator
from pydantic import BaseModel, Field
from typing import List
from langchain.prompts import PromptTemplate


dotenv.load_dotenv()


headers = {
    'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'''
}

article_url = """https://www.artificialintelligence-news.com/2022/01/25/meta-claims-new-ai-supercomputer-will-set-records/"""

session = requests.Session()

try:
    response = session.get(article_url, headers=headers, timeout=10)

    if response.status_code == 200:
        article = Article(article_url)
        article.download()
        article.parse()

        # print(f"Title: {article.title}")
        # print(f"Text: {article.text}")
    else:
        print(f"Failed to retrieve article at {article_url}")
except Exception as e:
    print(f"Error occurred while retrieving article {article_url}: {e}")

article_text = article.text
article_title = article.title

template = """
As an advanced AI you've been tasked to summarize online articles into
bulleted points. Here are a few examples of how you've done this in the past.
ints. Here are a few examples of how you've done this in the past:

Example 1:
Original Article: 'The Effects of Climate Change
Summary:
- Climate change is causing a rise in global temperatures.
- This leads to melting ice caps and rising sea levels.
- Resulting in more frequent and severe weather conditions.

Example 2:
Original Article: 'The Evolution of Artificial Intelligence
Summary:
- Artificial Intelligence (AI) has developed significantly over the past decade.
- AI is now used in multiple fields such as healthcare, finance, and transportation.
- The future of AI is promising but requires careful regulation.

Now, here's the article you need to summarize:

==================
Title: {article_title}

{article_text}
==================

Please provide a summarized version of the article in a bulleted list format.
"""

prompt = template.format(article_title=article_title, article_text=article_text)

messages = [HumanMessage(content=prompt)]

chat = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

#summary = chat.invoke(messages)

# print(summary.content)

class ArticleSummary(BaseModel):
    title: str = Field(description="The title of the article")
    summary: List[str] = Field(description="A bulleted list of the most important points from the article")

    @field_validator('summary')
    def has_three_or_more_Lines(cls, list_of_lines):
        if len(list_of_lines) < 3:
            raise ValueError("Summary must have at least three lines")
        return list_of_lines
    
parser = PydanticOutputParser(pydantic_object=ArticleSummary)

new_template = """
You are a very good assistant that summarizes online articles.

Here's the article you want to summarize.

==================
Title: {article_title}

{article_text}
==================

{format_instructions}
"""


prompt_template = PromptTemplate(
    template=new_template,
    input_variables=["article_title", "article_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt_template | chat | parser

result = chain.invoke({"article_title": article_title, "article_text": article_text})

print(result)

