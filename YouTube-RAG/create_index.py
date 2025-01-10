from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core import VectorStoreIndex
import pickle
import os
from llama_parse import LlamaParse
from dotenv import load_dotenv
from llama_index.core import StorageContext
import glob
from llama_index.vector_stores.lancedb import LanceDBVectorStore
load_dotenv()

cwd = os.getcwd()
data_path = os.path.join(cwd, "data")
compiled_data = glob.glob(data_path+'/audio/*.mp3') + glob.glob(data_path+'/image/*.png') + glob.glob(data_path+'/text/*.txt')


def load_or_parse_data():
    data_file = os.path.join(cwd, "parsed_data.pkl")

    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        parser = LlamaParse(api_key=os.getenv('LLAMA_CLOUD_API_KEY'), result_type='markdown')
        parsed_data = parser.load_data(file_path=compiled_data)
        with open(data_file, "wb") as f:
            pickle.dump(llama_parse_document, f)

    return parsed_data


text_store = LanceDBVectorStore(uri="lancedb", table_name="text_collection")
image_store = LanceDBVectorStore(uri="lancedb", table_name="image_collection")
storage_context = StorageContext.from_defaults(vector_store=text_store, image_store=image_store)


llama_parse_document = load_or_parse_data()
index = MultiModalVectorStoreIndex.from_documents(
    llama_parse_document,
    storage_context=storage_context,
)