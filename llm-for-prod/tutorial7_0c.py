from langchain.prompts import PromptTemplate, FewShotPromptTemplate

examples = [
    {"query": "What is the weather like?",
     "answer": "It's raining cats and dogs, better bring an umbrella!"},
     {"query": "How old are you?",
      "answer": "Age is just a number, but I'm timeless"}
]

example_template = """
User: {query}
AI: {answer}
"""

example_prompt = PromptTemplate(
    input_variables=["query", "answer"],
    template=example_template
)

prefix = """The following are excerpts from conversations with an AI
assistant. The assistant is known for its humor and wit, and often responds
with unexpected and creative answers.
"""

suffix = """
User: {query}
AI: """

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=suffix,
    input_variables=["query"],
    example_separator="\n\n"
)

]