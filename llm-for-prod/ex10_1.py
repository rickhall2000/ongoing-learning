import os
from langchain.agents import load_tools, initialize_agent
from langcahin.agents import AgentType
from langcahin.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
tools = load_tools(["google-search", "llm-math"], llm=llm)

agent = initialize_agent(tools, llm,
                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                         verbose=True)

query = "what is the result of 1000 plus the number of goals scored in the soccer world cup 2022"
response = agent.run(query)
print(response)

