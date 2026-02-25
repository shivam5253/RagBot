from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import SecretStr
import os

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return ChatGroq(
        api_key=SecretStr(api_key),
        model="llama-3.1-8b-instant"
    )
