from langchain.chains import LLMChain
from langchain.chains.base import Chain 
from langchain.prompts import PromptTemplate

from typing import Dict, List

llm = "this should be an llm"

class ConcatenateChain(Chain):
    chain_1: LLMChain
    chain_2: LLMChain

    @property
    def input_keys(self) -> List[str]:
        all_input_vars = set(self.chain_1.input_keys).union(set(self.chain_2.input_keys))
        return list(all_input_vars)
    
    @property
    def output_keys(self) -> List[str]:
        return ['concat_output']
    
    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        output_1 = self.chain_1.run(inputs)
        output_2 = self.chain_2.run(inputs)
        return {'concat_output': f'{output_1} {output_2}'}

prompt_1 = PromptTemplate(
    input_variables=['word'],
    template = "What is the meaning of the word {word}?",
)

prompt_2 = PromptTemplate(
    input_variables=['word'],
    template = "what is a word to replace the following word: {word}?",
)

chain_1 = prompt_1 | llm
chain_2 = prompt_2 | llm

concat_chain = ConcatenateChain(chain_1=chain_1, chain_2=chain_2)

concat_output = concat_chain.run("artificial")
print(f"Concatenated output: {concat_output}")

