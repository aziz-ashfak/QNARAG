import os
import sys
import tempfile
import logging
import markdown
from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Adjust sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from QnaBot.utils.pdf_utils import extract_text_with_pages
    from QnaBot.utils.export_utils import export_to_pdf, export_to_csv, export_to_word
    from QnaBot.utils.llm_utils import refine_qna, generate_qna
    from QnaBot.utils.qna_utils import parse_qna
    from QnaBot.pipeline.helper import extract_output
    from QnaRag.rag_pipeline.pdf_process import make_vectorstore, final_documents
    from QnaRag.rag_pipeline.prompt import prompt
    from QnaRag.rag import rag_bot 
    from config import load_config, load_chat_model
except ImportError as e:
    logger.error(f"Import error: {e}")
    raise

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/style", StaticFiles(directory="style"), name="style")

# Store results and PDF path temporarily
bot_results = {"qna": "", "qna_html": "", "qna_list": [], "query": [], "query_html": []}
temp_pdf_path = None



@app.get("/")
async def home(request: Request):
    logger.debug("Rendering home page")
    return templates.TemplateResponse("index.html", {"request": request, "bot_results": bot_results})

@app.post("/process")
async def process_pdf(request: Request, file: UploadFile = Form(...), num_questions: int = Form(...), mode: str = Form(...)):
    global bot_results, temp_pdf_path
    logger.debug(f"Process request: num_questions={num_questions}, mode={mode}, file={file.filename}")
    old_pdf_path = temp_pdf_path
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            temp_pdf_path = tmp.name
        
        bot_results["qna"], bot_results["qna_html"], bot_results["qna_list"] = extract_output(temp_pdf_path, num_questions, mode)
        bot_results["query"] = []
        bot_results["query_html"] = []
        logger.debug(f"Process results: qna_html={bot_results['qna_html'][:100]}...")
        return templates.TemplateResponse("index.html", {"request": request, "bot_results": bot_results})
    except Exception as e:
        logger.error(f"Error in process_pdf: {e}")
        markdown_text = f"# Q&A Results\n\n**Error**: Failed to process PDF: {str(e)}"
        bot_results["qna"] = markdown_text
        bot_results["qna_html"] = markdown.markdown(markdown_text, extensions=['extra'])
        bot_results["qna_list"] = []
        bot_results["query"] = []
        bot_results["query_html"] = []
        return templates.TemplateResponse("index.html", {"request": request, "bot_results": bot_results})
    finally:
        if old_pdf_path and os.path.exists(old_pdf_path):
            os.remove(old_pdf_path)

@app.post("/query")
async def query_pdf(request: Request, query: str = Form(...)):
    global bot_results, temp_pdf_path
    logger.debug(f"Query request: query={query}")
    try:
        if not temp_pdf_path or not os.path.exists(temp_pdf_path):
            logger.warning("No PDF available for query")
            markdown_text = f"### Query: {query}\n\n**Error**: No PDF uploaded. Please upload a PDF first."
            bot_results["query"].append(markdown_text)
            bot_results["query_html"].append(markdown.markdown(markdown_text, extensions=['extra']))
            return templates.TemplateResponse("index.html", {"request": request, "bot_results": bot_results})
        
        markdown_result, html_result = rag_bot(temp_pdf_path, query)
        bot_results["query"].append(markdown_result)
        bot_results["query_html"].append(html_result)
        logger.debug(f"Query result: {markdown_result}")
        return templates.TemplateResponse("index.html", {"request": request, "bot_results": bot_results})
    except Exception as e:
        logger.error(f"Error in query_pdf: {e}")
        markdown_text = f"### Query: {query}\n\n**Error**: Failed to process query: {str(e)}"
        bot_results["query"].append(markdown_text)
        bot_results["query_html"].append(markdown.markdown(markdown_text, extensions=['extra']))
        return templates.TemplateResponse("index.html", {"request": request, "bot_results": bot_results})

@app.get("/download/qna_md")
async def download_qna_md():
    global bot_results
    logger.debug("Download Q&A Markdown request")
    if not bot_results["qna"] or bot_results["qna"].startswith("# Q&A Results\n\n**Error**"):
        logger.warning("No Q&A results available to download")
        return {"error": "No Q&A results available to download"}
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode='w', encoding="utf-8") as tmp:
            temp_path = tmp.name
            tmp.write(bot_results["qna"])
        return FileResponse(temp_path, media_type="text/markdown", filename="qna_results.md")
    except Exception as e:
        logger.error(f"Error in download_qna_md: {e}")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return {"error": f"Failed to generate Markdown: {str(e)}"}

@app.get("/download/csv")
async def download_csv():
    global bot_results
    logger.debug("Download CSV request")
    if not bot_results["qna_list"]:
        logger.warning("No Q&A results available to download")
        return {"error": "No Q&A results available to download"}
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            temp_path = tmp.name
            export_to_csv(bot_results["qna_list"], temp_path)
        return FileResponse(temp_path, media_type="text/csv", filename="qna_results.csv")
    except Exception as e:
        logger.error(f"Error in download_csv: {e}")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return {"error": f"Failed to generate CSV: {str(e)}"}

@app.get("/download/doc")
async def download_doc():
    global bot_results
    logger.debug("Download DOC request")
    if not bot_results["qna_list"]:
        logger.warning("No Q&A results available to download")
        return {"error": "No Q&A results available to download"}
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            temp_path = tmp.name
            export_to_word(bot_results["qna_list"], temp_path)
        return FileResponse(temp_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="qna_results.docx")
    except Exception as e:
        logger.error(f"Error in download_doc: {e}")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return {"error": f"Failed to generate DOC: {str(e)}"}

@app.get("/download/pdf")
async def download_pdf():
    global bot_results
    logger.debug("Download PDF request")
    if not bot_results["qna_list"]:
        logger.warning("No Q&A results available to download")
        return {"error": "No Q&A results available to download"}
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            temp_path = tmp.name
            export_to_pdf(bot_results["qna_list"], temp_path)
        return FileResponse(temp_path, media_type="application/pdf", filename="qna_results.pdf")
    except Exception as e:
        logger.error(f"Error in download_pdf: {e}")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return {"error": f"Failed to generate PDF: {str(e)}"}

@app.get("/download/query_md")
async def download_query_md():
    global bot_results
    logger.debug("Download Query Markdown request")
    if not bot_results["query"]:
        logger.warning("No query results available to download")
        return {"error": "No query results available to download"}
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode='w', encoding="utf-8") as tmp:
            temp_path = tmp.name
            tmp.write("# Query Results\n\n" + "\n\n".join(bot_results["query"]))
        return FileResponse(temp_path, media_type="text/markdown", filename="query_results.md")
    except Exception as e:
        logger.error(f"Error in download_query_md: {e}")
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return {"error": f"Failed to generate Markdown: {str(e)}"}

@app.on_event("shutdown")
async def shutdown_event():
    global temp_pdf_path
    if temp_pdf_path and os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)
        logger.info("Temp PDF cleaned up on shutdown")