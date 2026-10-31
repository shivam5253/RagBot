# 🤖 RagBot 2.0

<div align="center">

### 🚀 [LIVE DEMO — Try RagBot](https://shivam5253-ragbot-ui.hf.space/)

</div>

## Project Architecture

```text
RagBot/
│
├── server/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   ├── load_vectorstore.py
│   │   ├── pdf_handler.py
│   │   └── query_handler.py
│   │
│   ├── .env
│   ├── logger.py
│   ├── main.py
│   └── requirements.txt
│
└── client/
    ├── utils/
    │   └── api.py
    ├── app.py
    └── config.py
```

## Architecture Overview

- **main.py** → Controls the API.
- **modules/** → Contains the actual RAG implementation.
- **app.py** → Streamlit user interface.
- **api.py** → Connects the frontend to the backend.
- **config.py** → Stores the backend API URL.
- **logger.py** → Records application events.

## PDF Upload Pipeline

```text
PDF
 ↓
Document Loader
 ↓
Split into Chunks
 ↓
Embedding Model
 ↓
Generate Embeddings
 ↓
Store in Vector Database (FAISS)
```

## Query Pipeline

```text
User Question
 ↓
Load Embeddings
 ↓
Retriever
 ↓
Similarity Search
 ↓
FAISS Vector Database
 ↓
Find Top 4 Similar Chunks
 ↓
Build Context + Prompt
 ↓
LLM (Groq - Llama 3.1 8B Instant)
 ↓
Generated Answer
```

## Modules Explanation

### 1. modules/__init__.py

Created an empty `__init__.py` file to mark the modules directory as a Python package, allowing me to organize and import functionality from different Python files.

### 2. modules/llm.py — LLM Initialization

Initializes the Groq LLM using the API key stored in environment variables.

### 3. modules/pdf_handler.py — PDF Loading and Chunking

- Uses `PyPDFLoader` to load PDF documents.
- Creates an empty list `all_docs = []` to collect extracted documents.
- Loops through all PDF files in the folder.
- Uses `RecursiveCharacterTextSplitter` to split documents into chunks.
- Chunk size: 500
- Chunk overlap: 50

### 4. modules/load_vectorstore.py — Embeddings and FAISS

Uses Hugging Face embeddings and FAISS for vector storage.

Main functions:

- `get_embeddings()` — Initializes the Hugging Face embedding model.
- `create_vectorstore(docs)` — Generates embeddings and creates the FAISS vector store.
- `load_vectorstore()` — Loads the previously saved FAISS index.

```python
FAISS_PATH = "faiss_store"
```

### 5. modules/query_handler.py — Retrieval and Answer Generation

The query handler implements the retrieval and generation stages of RAG.

1. Loads the FAISS index.
2. Retrieves the top four relevant chunks using similarity search.
3. Combines the retrieved chunks into a context.
4. Constructs a prompt containing the context and user question.
5. Sends the prompt to the Groq-hosted Llama model.
6. Returns the generated answer.

## Main Backend — server/main.py

`main.py` is the entry point of the backend.

It acts as the controller of the application. It receives HTTP requests, calls the appropriate modules, and sends responses back to the frontend.

It does not implement chunking, embeddings or similarity search itself. It delegates those tasks to the modules.

### Main Imports

- `FastAPI` — Creates the backend application.
- `UploadFile` and `File` — Handle uploaded PDF files.
- `CORSMiddleware` — Handles cross-origin requests.
- `BaseModel` — Validates request data.
- `os` — Handles directories, environment variables and file paths.
- `shutil` — Copies uploaded file data.
- `uvicorn` — Runs the FastAPI application.
- `logger` — Records application events.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Checks whether the API is running. |
| POST | `/upload_pdfs/` | Uploads and indexes PDF files. |
| POST | `/ask/` | Accepts a question and returns an answer. |

### CORS — Cross-Origin Resource Sharing

CORS allows the backend to specify which origins can access its resources.

For example:

- Frontend: `http://localhost:8501`
- Backend: `http://localhost:8000`

These are different origins because their ports are different.

CORS middleware handles cross-origin request permissions.

### Middleware

Middleware is a component that processes requests and responses around application endpoints.

### Binary File Handling

```python
with open(path, "wb") as f:
```

- `w` means write mode.
- `b` means binary mode.

Binary mode is used because PDF files contain binary data, not just ordinary text.

### if __name__ == "__main__"

Python automatically creates a special variable called `__name__` in every Python module.

- When a Python file is executed directly, `__name__` becomes `"__main__"`.
- When the file is imported into another module, `__name__` contains the module name.

This condition ensures that the Uvicorn startup code runs when `main.py` is executed directly.

### Uvicorn Configuration

```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=port
)
```

| Argument | Meaning |
|---|---|
| `main:app` | Import the app object from main.py. |
| `host="0.0.0.0"` | Listen on all available network interfaces. |
| `port=port` | Run on the selected port. |

### Async def vs def

- `async def` defines an asynchronous function that can use `await`.
- `def` defines a normal synchronous function.

Although the FastAPI endpoints use `async def`, the internal PDF processing, FAISS operations and LLM invocation are synchronous.

## Logger.py — Application Logging

Logging is the process of recording events that happen while an application runs.

Examples:
- A PDF was uploaded.
- A vector store was created.
- An error occurred.
- An API operation completed.

Log format:

```python
'%(asctime)s - %(levelname)s - %(message)s'
```

Example:

```text
2026-10-30 16:30:00 - INFO - Saved: resume.pdf
2026-10-30 16:30:02 - INFO - Vector store ready!
```

### Python Logging Levels

| Level | Purpose |
|---|---|
| DEBUG | Detailed debugging information |
| INFO | Normal application events |
| WARNING | Something unexpected |
| ERROR | An operation failed |
| CRITICAL | Serious application failure |

## Client — Frontend

### 1. app.py

- Creates the Streamlit user interface.
- Allows users to upload multiple PDFs.
- Provides a question input field.
- Displays generated answers.
- Maintains chat history using `st.session_state`.
- Provides a button to clear chat history.

### 2. utils/api.py

Connects the Streamlit frontend to the FastAPI backend using the Python Requests library.

Main functions:

- `upload_pdfs(files)` — Sends PDF files to the `/upload_pdfs/` endpoint using a POST request.
- `ask_question(question)` — Sends the user's question to the `/ask/` endpoint and returns the answer.

### 3. config.py

Stores the backend API base URL.

```python
API_BASE_URL = "http://127.0.0.1:8000"
```

This makes it easier to change the backend URL without modifying API request functions.

---

## Technologies Used

- Python
- FastAPI
- Streamlit
- LangChain
- Hugging Face Embeddings
- FAISS
- Groq
- Llama 3.1 8B Instant
- Uvicorn
- Requests
