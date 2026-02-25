import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import API_BASE_URL

def upload_pdfs(files):
    file_list = [
        ("files", (f.name, f, "application/pdf"))
        for f in files
    ]
    try:
        response = requests.post(
            f"{API_BASE_URL}/upload_pdfs/",
            files=file_list,
            timeout=120  # wait up to 2 minutes
        )
        if response.text.strip() == "":
            return {"message": "Error: Server returned empty response. Check FastAPI terminal."}
        return response.json()
    except Exception as e:
        return {"message": f"Error: {str(e)}"}


def ask_question(question: str):
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask/",
            json={"question": question},
            timeout=60
        )
        return response.json().get("answer", "No answer received")
    except Exception as e:
        return f"Connection error: {str(e)}"