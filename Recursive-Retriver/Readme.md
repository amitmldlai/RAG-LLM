# RAG System for Unstructured HTML Documents

This project implements a **Retrieval-Augmented Generation (RAG)** system for querying unstructured HTML documents containing raw text and tables. The system provides two retrieval engines:

1. **Basic Query Retriever Engine**: A simple and efficient retrieval mechanism.
2. **Recursive Query Retriever Engine**: A context-aware hierarchical retriever for nested structures.

---

## Features

- **HTML Preprocessing**: Extracts raw text and table data from messy HTML structures.
- **Flexible Retrieval Engines**:
  - **Basic Query Retriever** for quick, direct searches.
  - **Recursive Query Retriever** for deep and complex queries.
- **Embedding-Based Search**: Improves query relevance using vector embeddings.

---

## Installation

### Prerequisites

- Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```
### Setup key in .env

```
OPENAI_API_KEY=
```