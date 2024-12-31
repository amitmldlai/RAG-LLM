# RAG Application Using Microsoft Graph RAG

This application enables users to upload documents (e.g., `.txt` or `.pdf`) and perform retrieval-augmented generation (RAG) queries utilizing two search techniques: **local** and **global**. It allows users to upload multiple documents and train the RAG system to compute embeddings and metadata for efficient query resolution.

---

## Features

1. **Document Upload**:
   - Supports uploading multiple `.txt` and `.pdf` documents.
   - Documents are processed to compute embeddings and metadata for RAG-based retrieval.

2. **Search Techniques**:
   - **Local Search**: Focuses on specific document segments for precise queries.
   - **Global Search**: Searches across all available documents for a broader query context.

3. **Training Options**:
   - **Train Latest**: Computes embeddings and metadata for the most recently uploaded document and sets up the query engine using it.
   - **Train All**: Processes and computes embeddings and metadata for all documents present in the input directory.

4. **Web Interface**:
   - User-friendly web application accessible at: [http://localhost:5005/fact-fusion](http://localhost:5005/fact-fusion).

---

## Requirements

- **Python**: Version 3.10 or higher.
- **Virtual Environment**: Use a virtual environment to manage dependencies.

---

## Setup Instructions

1. **Clone the Repository**

2. **Inside the cloned repo directory, create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate    # For Linux/MacOS
   venv\Scripts\activate       # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Graph RAG workspace using**:
   ```
   graphrag init --root ./
   ```
   It will setup the .env and setting.yaml file, if required change the model configuration in setting.yaml 

5. **Add your specific model key in .env file**
    ```
    GRAPHRAG_API_KEY=
    ```
6. **Start the Application**:
   ```bash
   python app.py
   ```

7. **Access the Web Application**:
   Open your browser and navigate to [http://localhost:5005/fact-fusion](http://localhost:5005/fact-fusion).

---

## Usage

1. Upload documents in `.txt` or `.pdf` format.
2. Choose one of the training options:
   - **Train Latest**: Processes only the most recent document.
   - **Train All**: Processes all documents in the upload directory.
3. Perform queries using local or global search techniques to retrieve insights from the uploaded documents.

---

## Notes

- The application is designed to work with Python 3.10+.
- Train your RAG system after uploading documents to ensure queries are up-to-date.

---

