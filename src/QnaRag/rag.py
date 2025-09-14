from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import sys
import time
import markdown
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.QnaRag.rag_pipeline.pdf_process import make_vectorstore,final_documents
from src.QnaRag.rag_pipeline.prompt import prompt
from src.config import load_config,load_chat_model
from logger import logger
llm = load_chat_model()

# def rag_bot(path):
#     documents = final_documents(path)
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_documents(documents, embeddings)
#     document_chain=create_stuff_documents_chain(llm,prompt)
    
#     retriever=vectorstore.as_retriever()
#     retrieval_chain=create_retrieval_chain(retriever,document_chain)
#     start=time.process_time()
#     response=retrieval_chain.invoke({'input':"Explain the summary of the paper in detail.",
#                                     'context':" ".join([doc.page_content for doc in documents[:3]])})
#     print("Response time :",time.process_time()-start)
#     #print(response['answer'])
#     if isinstance(response['answer'], list):  
#         print(response['answer'][0])  # take the first response
#     else:
#         print(response['answer'])

# rag_bot("C:\\QNARAG\\IEEE_SMC_2025_Omar.pdf")
def rag_bot(path, query):
    logger.debug(f"Processing RAG for file: {path}, query: {query}")
    try:
        documents = final_documents(path)
        logger.debug(f"Extracted {len(documents)} documents")
        
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(documents, embeddings)
        llm = load_chat_model()
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vectorstore.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response = retrieval_chain.invoke({'input': query, 'context': " ".join([doc.page_content for doc in documents[:3]])})
        result = response['answer'] if not isinstance(response['answer'], list) else response['answer'][0]
        markdown_result = f"### Query: {query}\n\n**Answer**: {result}"
        logger.debug(f"RAG Markdown result: {markdown_result}")
        return markdown_result, markdown.markdown(markdown_result, extensions=['extra'])
    except Exception as e:
        logger.error(f"Error in rag_bot: {e}")
        markdown_result = f"### Query: {query}\n\n**Error**: Failed to generate answer: {str(e)}"
        return markdown_result, markdown.markdown(markdown_result, extensions=['extra'])