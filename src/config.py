import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq
from langchain_groq import ChatGroq
def load_chat_model():
    if not load_dotenv(find_dotenv()):
        raise RuntimeError(".env file not found. Please set GROQ_API_KEY")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(" GROQ_API_KEY is missing in environment")

    return ChatGroq(groq_api_key=api_key, model="llama-3.3-70b-versatile")
def load_config():
    if not load_dotenv(find_dotenv()):
        raise RuntimeError(".env file not found. Please set GROQ_API_KEY")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(" GROQ_API_KEY is missing in environment")

    return Groq(api_key=api_key)
