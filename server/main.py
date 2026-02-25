from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, shutil

from modules.pdf_handler import load_and_split_pdfs
from modules.load_vectorstore import create_vectorstore
from modules.query_handler import answer_query
from logger import logger

# Create FastAPI app
app = FastAPI(title="RagBot 2.0 API")

# Allow Streamlit to talk to FastAPI
# Without this → CORS error → connection blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create uploaded_pdfs folder automatically if not exists
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ─── ENDPOINT 1 — Health Check ───────────────────
@app.get("/")
def root():
    return {"status": "RagBot API is running!"}


# ─── ENDPOINT 2 — Upload PDF ─────────────────────
@app.post("/upload_pdfs/")
async def upload_pdfs(files: list[UploadFile] = File(...)):

    # Save each uploaded file to disk
    for file in files:
        if file.filename is not None:
            path = os.path.join(UPLOAD_DIR, file.filename)
            with open(path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            logger.info(f"Saved: {file.filename}")
        else:
            logger.warning("Uploaded file has no filename and was skipped.")

    # Load + split PDFs into chunks
    docs = load_and_split_pdfs(UPLOAD_DIR)
    logger.info(f"Total chunks: {len(docs)}")

    # Create ChromaDB from chunks
    create_vectorstore(docs)
    logger.info("Vector store ready!")

    return {"message": f"{len(files)} PDF(s) uploaded and indexed!"}


# ─── ENDPOINT 3 — Ask Question ───────────────────
class QueryRequest(BaseModel):
    question: str

@app.post("/ask/")
async def ask(req: QueryRequest):
    logger.info(f"Question: {req.question}")
    answer = answer_query(req.question)
    return {"answer": answer}
