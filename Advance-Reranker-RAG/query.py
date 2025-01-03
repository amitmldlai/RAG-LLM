from llama_parse import LlamaParse
from dotenv import load_dotenv
import pickle
import os
from instructions import instruction
from llama_index.core import VectorStoreIndex
from settings import load_settings
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core.postprocessor import SentenceTransformerRerank


from llama_index.core import load_index_from_storage, StorageContext


load_dotenv()
load_settings()

# Reranker Embedding model
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=3
)


def load_or_parse_data():
    data_file = "./parsed_data.pkl"

    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        parser = LlamaParse(api_key=os.getenv('LLAMA_CLOUD_API_KEY'), result_type="markdown", parsing_instruction=instruction)
        llama_parse_documents = parser.load_data("./data/uber_10q_march_2022.pdf")
        with open(data_file, "wb") as f:
            pickle.dump(llama_parse_documents, f)
        parsed_data = llama_parse_documents

    return parsed_data


def create_index(documents, recursive=False):
    if recursive:
        if os.path.exists('./recursive_index'):
            storage_context = StorageContext.from_defaults(persist_dir='./recursive_index')
            index = load_index_from_storage(storage_context)
        else:
            node_parser = MarkdownElementNodeParser(num_workers=8)
            nodes = node_parser.get_nodes_from_documents(documents)
            base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
            index = VectorStoreIndex(nodes=base_nodes + objects)
            index.storage_context.persist('./recursive_index')
    else:
        if os.path.exists('./raw_index'):
            storage_context = StorageContext.from_defaults(persist_dir='./raw_index')
            index = load_index_from_storage(storage_context)
        else:
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist('./raw_index')

    return index


def setup_query_engine(index, rerank=False):
    if rerank:
        query_eng = index.as_query_engine(similarity_top_k=5, node_postprocessors=[reranker], verbose=True)
    else:
        query_eng = index.as_query_engine(similarity_top_k=5, verbose=True)
    return query_eng


def query(query_eng, user_query):
    response = query_eng.query(user_query)
    return response


# Load Documents
document = load_or_parse_data()

# Create Index
raw_index = create_index(document)
recursive_index = create_index(document, recursive=True)

# create Raw Engine
raw_engine = setup_query_engine(raw_index)
# create Reranked Raw Engine
rerank_raw_engine = setup_query_engine(raw_index, rerank=True)

# create Recursive Engine
recursive_engine = setup_query_engine(recursive_index)
# create Reranked Recursive Engine
rerank_recursive_engine = setup_query_engine(recursive_index, rerank=True)


while True:
    usr_query = input('Please provide your query:')
    query_engine = int(input("Press 1 for Raw Query Engine, 2 for Reranked Raw Query Engine, 3 for Recursive Query "
                             "Engine, 4 for Reranked Recursive Query Engine"))
    if query_engine == 1:
        res = query(raw_engine, usr_query)
    elif query_engine == 2:
        res = query(rerank_raw_engine, usr_query)
    elif query_engine == 3:
        res = query(recursive_engine, usr_query)
    else:
        res = query(rerank_recursive_engine, usr_query)
    print(res)