import os
from llama_index import SimpleDirectoryReader
from llama_index.vector_stores import DeepLakeVectorStore
from llama_index.storage.storage_context import StorageContext
from lama_index import VectorStoreIndex
from llama_index.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.agent import OpenAIAgent, FnRetrieverOpenAIAgent
from llama_index.objects import ObjectIndex, SimpleToolNodeMapping

tesla_docs = SimpleDirectoryReader(
    input_files=["/content/data/1k/tesla.txt"]
).load_data()

vector_store = DeepLakeVectorStore()

storage_context = StorageContext.from_defaults(vector_store=vector_store)
tesla_index = VectorStoreIndex.from_documents(tesla_docs, storage_context=storage_context)

webtext_docs = SimpleDirectoryReader(
    input_files=["/content/data/1k/webtext.txt"]
).load_data()

try:
    storage_context = StorageContext.from_defaults(persist_dir="/content/storage/webtext")
    webtext_index = load_index_from_storage(storage_context)
except:
    webtext_index = VectorStoreIndex.from_documents(webtext_docs)
    webtext_index.storage_context.persist(persist_dir="/content/storage/webtext")
    
tesla_engine = tesla_index.as_query_engine(similarity_top_k=3)
webtext_engine = webtext_index.as_query_engine(similarity_top_k=3)

query_engine_tools = [
    QueryEngineTool(
        query_engine=tesla_engine,
        metadata=ToolMetadata(
            name="tesla_1k",
            description=(
                """"Provides information about Tesla's statements that refers to future
                times and predictions."""
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=webtext_engine,
        metadata=ToolMetadata(
            name="webtext_1k",
            description=(
                """Provides information about Tesla's statements that refers to future
                times and predictions."""
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
]

agent = OpenAIAgent.from_tools(query_engine_tools, verbose=True)

agent.chat_repl()


def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b

def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b

multiply_tool = FunctionTool.from_defaults(fn=multiply, name="multiply", description="Multiply two integers")
add_tool = FunctionTool.from_defaults(fn=add, name="add", description="Add two integers")

all_tools = [multiply_tool, add_tool]

tool_mapping = SimpleToolNodeMapping.from_objects(all_tools)
obj_index = ObjectIndex.from_objects(all_tools, tool_mapping, VectorStoreIndex,)

agent = FnRetrieverOpenAIAgent.from_index(obj_index.as_retriever(), verbose=True)

agent.chat("What's 12 multiplied by 22? Make sure to use Tools")