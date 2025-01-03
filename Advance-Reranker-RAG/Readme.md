# **LlamaParse Query Engine**

This project is a document parsing and querying system built using LlamaParse and LlamaIndex, enabling efficient indexing and querying of documents. The system supports both basic and advanced search capabilities, including reranking of results using SentenceTransformer models.

---

## **Features**
- **Document Parsing**: Parses and processes documents into structured data using `LlamaParse`.
- **Indexing**: Supports recursive and non-recursive indexing for better search performance.
- **Reranking**: Enhances query results by reranking with SentenceTransformer models.
- **Interactive Querying**: Allows users to interactively query the indexed data using different query engines.

---

## **Requirements**
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

---

## **Installation**
1. Clone the repository:
2. Setup key in .env file:
    ```
    OPENAI_API_KEY=
    LLAMA_CLOUD_API_KEY=
    ```
3. Install dependencies:
    ```
   pip install -r requirements.txt
    ```

4. Ensure the necessary data is available:
    Place your documents in the ./data/ folder (e.g., uber_10q_march_2022.pdf).

## **Usage**

1. Execute the script:
    ```
    python query.py
    ```

2. Enter your query when prompted:
    ```
    Please provide your query:
    ```

3. Choose the query engine:
    ```
    Press 1: Raw Query Engine
    Press 2: Reranked Raw Query Engine
    Press 3: Recursive Query Engine
    Press 4: Reranked Recursive Query Engine
    ```
   
## **Functionality**
1. *Document Parsing* : Loads and parses PDF documents using LlamaParse with custom parsing instructions.
2. *Indexing* 
   1. **Raw Indexing** : Builds a basic index from the parsed documents.
   2. **Recursive Indexing** : Creates an index with hierarchical relationships.
3. *Query Engines*
   1. **Raw Query Engine** : Retrieves results without reranking.
   2. **Reranked Raw Query Engine** : Enhances raw results using a reranking model for improved relevance.
   3. **Recursive Query Engine** : Fetches results while considering the hierarchical structure of the document.
   4. **Reranked Recursive Query Engine** : Combines recursive querying with reranking to deliver the most contextually relevant results.
      
