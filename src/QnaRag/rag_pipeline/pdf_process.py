import os 
import sys 
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

#_ = load_dotenv(find_dotenv())
# groq_api_key=os.getenv('GROQ_API_KEY')

# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# llm=ChatGroq(groq_api_key=groq_api_key,
#              model_name="llama-3.3-70b-versatile")
def final_documents(path):
    loader = PyPDFLoader(path)
    doc = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(doc[:20])  # splitting
    return documents

def make_vectorstore(path): 
    final_documents = final_documents(path)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(final_documents, embeddings)
    return vectorstore

