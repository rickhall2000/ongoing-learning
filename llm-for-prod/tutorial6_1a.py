import dotenv
import os

from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


dotenv.load_dotenv(".env")

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0, 
                  api_key=os.getenv("OPENAI_API_KEY"))

template = "You are an assistant that helps users find information about movies"
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "Find information about {movie_title}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

response = chat.invoke(chat_prompt.format_prompt(movie_title="The Matrix").to_messages())

print(response)