from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


def load_settings():
    Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-large')
    Settings.llm = OpenAI(model="gpt-4o")