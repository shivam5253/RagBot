from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_and_split_pdfs(pdf_folder="uploaded_pdfs"):
    all_docs = []
    
    # Loop through all PDF files in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            loader = PyPDFLoader(path)
            docs = loader.load()
            all_docs.extend(docs)
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(all_docs)
    return chunks