from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

promt = PromptTemplate(
    input_variables=["query"],
    template="You are a renowned science fiction writer. {query}"
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tools = [
    Tool(
        name="Science Fiction Writer",
        func=llm_chain.run,
        description="Use this tool for generating science fiction stories. Input should be a command about generating specific types of stories"
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

response = agent.run("Compose an epic science fiction saga about intersteller explorers")
print(response)

