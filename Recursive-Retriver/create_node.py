from llama_index.readers.file import FlatReader
from pathlib import Path
import nest_asyncio
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import UnstructuredElementNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from dotenv import load_dotenv
import pickle
import os
from llama_index.core import load_index_from_storage, StorageContext


nest_asyncio.apply()
load_dotenv()

Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-large')
Settings.llm = OpenAI(model="gpt-4o")

docs = FlatReader().load_data(Path("./data/tesla_2021_10k.htm"))
node_parser = UnstructuredElementNodeParser()


def save_parse_documents():
    if not os.path.exists("raw_nodes.pkl"):
        raw_node = node_parser.get_nodes_from_documents(docs, show_progress=True)
        pickle.dump(raw_node, open("raw_nodes.pkl", "wb"))
    else:
        raw_node = pickle.load(open("raw_nodes.pkl", "rb"))
    return raw_node


def node_and_mapping(raw_node):
    base_node, node_mapping = node_parser.get_base_nodes_and_mappings(raw_node)
    return base_node, node_mapping


def setup_retriever(base_node):
    if not os.path.exists('./storage'):
        vector_index = VectorStoreIndex(base_node)
        vector_index.storage_context.persist("./storage")
    else:
        # Create storage context from persisted data
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        # Load index from storage context
        vector_index = load_index_from_storage(storage_context)
    vector_retriever = vector_index.as_retriever(similarity_top_k=1)
    return vector_index, vector_retriever


def setup_basic_query_engine(vector_index):
    query_engine = vector_index.as_query_engine(similarity_top_k=1)
    return query_engine


def setup_recursive_query_engine(vector_retriever, node_mapping):
    recursive_retriever = RecursiveRetriever(
        "vector",
        retriever_dict={"vector": vector_retriever},
        node_dict=node_mapping,
        verbose=True,
    )
    query_engine = RetrieverQueryEngine.from_args(recursive_retriever)
    return query_engine


def query(query_engine, user_query):
    response = query_engine.query(user_query).response
    return response


raw_nodes = save_parse_documents()
base_nodes, node_mappings = node_and_mapping(raw_nodes)
vector_index, retriever = setup_retriever(base_nodes)
basic_query_engine = setup_basic_query_engine(vector_index)
recursive_query_engine = setup_recursive_query_engine(retriever, node_mappings)
while True:
    # usr_query = 'What were the total cash flows in 2021?'
    usr_query = input('Please provide your query:')
    query_engine = int(input("Press 1 for Basic Query Engine, 2 for Recursive Query Engine"))
    if query_engine == 1:
        res = query(basic_query_engine, usr_query)
    else:
        res = query(recursive_query_engine, usr_query)
    print(res)