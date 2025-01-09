import os
import glob
from create_databse import create_db_from_csv_with_pandas
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import SQLDatabase
from sqlalchemy import create_engine
from llama_parse import LlamaParse
from dotenv import load_dotenv
import pickle
load_dotenv()

cwd = os.getcwd()

data_path = os.path.join(cwd, "data")
db_path = os.path.join(cwd, "db")
parsed_path = os.path.join(cwd, "parsed_data")


csv_file_path = os.path.join(data_path, "netflix.csv")
db_name = os.path.join(db_path, 'netflix.db')
table_name = 'netflix'

if not glob.glob(f'{db_path}/*.db'):
    create_db_from_csv_with_pandas(csv_file_path, db_name, table_name)


def load_or_parse_data():
    data_file = os.path.join(parsed_path, "parsed_data.pkl")

    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        parser = LlamaParse(api_key=os.getenv('LLAMA_CLOUD_API_KEY'), auto_mode=True, result_type='markdown',
                            auto_mode_trigger_on_image_in_page=True,
                            auto_mode_trigger_on_table_in_page=True)
        llama_parse_documents = parser.load_data(os.path.join(data_path, "List_of_Netflix_original_programming.pdf"))

        with open(data_file, "wb") as f:
            pickle.dump(llama_parse_documents, f)
        parsed_data = llama_parse_documents

    return parsed_data


def vector_query_engine():
    parsed_data = load_or_parse_data()
    node_parser = MarkdownElementNodeParser()
    nodes = node_parser.get_nodes_from_documents(parsed_data)
    nodes, objects = node_parser.get_nodes_and_objects(nodes)
    if not os.path.exists(os.path.join(cwd, 'index_storage')):
        vector_store_index = VectorStoreIndex(nodes+objects)
        vector_store_index.storage_context.persist(persist_dir=os.path.join(cwd, 'index_storage'))
    else:
        storage_context = StorageContext.from_defaults(persist_dir=os.path.join(cwd, 'index_storage'))
        vector_store_index = load_index_from_storage(storage_context)

    vector_store_info = VectorStoreInfo(
        content_info="Information about shows running on Netflix",
        metadata_info=[
                     MetadataInfo(name="tenure",
                                  type="str",
                                  description="The time duration of the shows on Netflix")
                     ])
    vector_auto_retriever = VectorIndexAutoRetriever(vector_store_index, vector_store_info=vector_store_info)

    retriever_query_engine = RetrieverQueryEngine.from_args(vector_auto_retriever, llm=OpenAI(model="gpt-4"))
    return retriever_query_engine


def sql_query_engine():
    engine = create_engine(f"sqlite:///{db_name}", future=True)
    sql_database = SQLDatabase(engine)
    query_engine = NLSQLTableQueryEngine(sql_database=sql_database, tables=[table_name])
    return query_engine
