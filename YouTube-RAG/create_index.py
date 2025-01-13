from llama_index.core import VectorStoreIndex
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.schema import ImageDocument
from llama_index.core.schema import TextNode
import os
import glob
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core import Settings
from llama_index.embeddings.google import GooglePaLMEmbedding
from llama_index.llms.gemini import Gemini


load_dotenv()

cwd = os.getcwd()
data_path = os.path.join(cwd, "data")
embed_model = GooglePaLMEmbedding(model_name="models/embedding-gecko-001")
llm = Gemini(model="models/gemini-1.5-flash")
Settings.embed_model = embed_model
Settings.model = llm


def create_image_text_node():
    image_text_node = list()
    llm_vision = GeminiMultiModal(model_name='models/gemini-1.5-flash')
    image_path = glob.glob(data_path + "/image/" + "*.png")

    image_documents = [ImageDocument(image_path=path) for path in image_path]
    for image in image_documents:
        resp = llm_vision.complete(
            prompt="Summarize the image ",
            image_documents=[image],
        )

        text_node = TextNode(
            text=resp.text,
            metadata={"image_path": image.image_path}
        )
        image_text_node.append(text_node)
    return image_text_node


def create_audio_text_node():
    text_path = glob.glob(data_path + "/text/*.txt")[0]
    with open(text_path, "r") as file:
        text = file.read()
    audio_text_node = TextNode(
        text=text,
        metadata={"audio_path": text_path}
    )
    return audio_text_node


if os.path.exists('./storage'):
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index = load_index_from_storage(storage_context)
else:
    image_node = create_image_text_node()
    audio_node = create_audio_text_node()
    index = VectorStoreIndex(image_node+[audio_node])
    index.storage_context.persist(persist_dir="./storage")

query_engine = index.as_query_engine()

while True:
    query = input("Please add your query:")
    response = query_engine.query(query)
    print(response)