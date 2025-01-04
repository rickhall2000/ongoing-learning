import os
import dotenv

import logging
import sys

from llama_index.readers.wikipedia import WikipediaReader
from llama_index.core.node_parser import SimpleNodeParser

from llama_index.core import VectorStoreIndex

dotenv.load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

loader = WikipediaReader()
documents = loader.load_data(pages=["Natural Language Processing", "Artificial Intelligence"])

parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=20)
nodes = parser.get_nodes_from_documents(documents)
print(len(nodes))

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("What is the difference between natural language processing and artificial intelligence?")
print(response)
