from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import uvicorn

from modules.pdf_handler import load_and_split_pdfs
from modules.load_vectorstore import create_vectorstore
from modules.query_handler import answer_query
from logger import logger

app = FastAPI(title="RagBot 2.0 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"status": "RagBot API is running!"}


@app.post("/upload_pdfs/")
async def upload_pdfs(files: list[UploadFile] = File(...)):
    for file in files:
        filename = file.filename or "uploaded_file"
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        logger.info(f"Saved: {file.filename}")

    docs = load_and_split_pdfs(UPLOAD_DIR)
    create_vectorstore(docs)
    logger.info("Vector store ready!")
    return {"message": f"{len(files)} PDF(s) uploaded and indexed!"}


class QueryRequest(BaseModel):
    question: str


@app.post("/ask/")
async def ask(req: QueryRequest):
    answer = answer_query(req.question)
    return {"answer": answer}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)