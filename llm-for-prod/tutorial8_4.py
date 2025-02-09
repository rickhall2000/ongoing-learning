from langchain.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.constitutional_ai.base import ConstitutionalChain
from langchain.chains.constitutional_ai.models import ConstitutionalPrinciple

evil_assitant_prommpt = PromptTemplate(
    tempalte="""
    You are an evil memntor for students with no morals. Give suggestions taht
    are easiest and fastest to achieve the goal.
    Goal: {inquiry}
    Easiest way:"""
    input_variables=["inquiry"],
)

llm = OpenAI(model_name="gpt-3.5-turbo", 
             temperature=0)

evil_assitant_chain = evil_assitant_prommpt | llm

result = evil_assitant_chain.invoke(inquiry="Getting full mark on my exams.")

ethical_principle = ConstitutionalPrinciple(
    name="Ethical Principle",
    critique_request="This model should only talk about ethical and fair thing"
    revision_request="Rewrite the models output to be both ethical and fair"
)

constitional_chain = ConstitutionalChain.from_llm(
    chain=evil_assitant_chain,
    constitutional_principles=[ethical_principle],
    llm=llm,
    verbose=True,
)

result = constitional_chain.run(inquiry="Getting full mark on my exams.")

fun_principle = ConstitutionalPrinciple(
    name="Be Funny",
    critique_request="""The model responses must be funny and understandable for a 7th grader.""",
    revision_request="""Rewrite the model's output to be both funny and understandable for 7th graders.""",
)

constitutional_chain = ConstitutionalChain.from_llm(
    chain=evil_assistant_chain,
    constitutional_principles=[ethical_principle, fun_principle],
    llm=llm,
    verbose=True,
)

result = constitutional_chain.run(inquiry="Getting full mark on my exams.")

