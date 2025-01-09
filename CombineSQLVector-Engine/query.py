from llama_index.core.tools import QueryEngineTool
from setup_query_engine import vector_query_engine, sql_query_engine
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import SQLAutoVectorQueryEngine
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model="gpt-4o")
vector_query_engine = vector_query_engine()
sql_query_engine = sql_query_engine()

sql_tool = QueryEngineTool.from_defaults(
    query_engine=sql_query_engine,
    description=("""Useful for translating a natural language query into a SQL query over a table containing: netflix, 
    with columns including show_id, type, title, director, country, date_added, release_year, rating, duration, and 
    listed_in. This table contains information about Netflix shows and movies, including their metadata such as title, 
    genre, director, country of origin, release year, and rating""")
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=("""Useful for answering semantic questions about Netflix shows and movies, such as their titles, 
    genres, directors, countries of origin, release years, and ratings""")
)


query_engine = SQLAutoVectorQueryEngine(sql_tool, vector_tool, llm=llm)

while True:
    query = input("Please provide your query:")
    response = query_engine.query(query)
    print(response)