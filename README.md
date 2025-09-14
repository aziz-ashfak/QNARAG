<p align="center">
  <img src="https://img.shields.io/badge/QnA-RAG-blueviolet?style=for-the-badge&logo=python&logoColor=white" alt="QnA RAG Logo" />
</p>

# 🤖 Q&A Bot with RAG

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)  
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)  
![Status](https://img.shields.io/badge/Status-Active-success)  

A **Retrieval-Augmented Generation (RAG)-powered Q&A bot** for answering queries using research papers and PDF documents.  
It supports **summarization, graph/image analysis, and exporting results** into multiple formats.  

---

## ✨ Features
- 📄 Generate **Q&A pairs** from PDFs or custom queries  
- 🔍 **RAG-based Retrieval** – context-aware answers from stored documents  
- 🧠 **LLM integration** – enhance answers with transformer models  
- 📊 Analyze **figures, graphs, and tables** inside research papers  
- 📝 Export results in: `Markdown (.md)`, `CSV (.csv)`, `DOCX (.docx)`, `PDF (.pdf)`  
- 🌐 REST API + Web interface (FastAPI + Jinja2)  
- ⚡ Modular design for research & production  

---

## 📂 Directory Structure
```bash
     
├── research 
    ├── research(RAg).ipynb   # Jupyter notebooks for RAG experimentation.
├── src  # Core source code.
    ├── QnaBot # Q&A pipeline and utilities ( LLM interactions, PDF processing).
        ├── pipeline  
            ├── __init__.py
            ├── helper.py      # main file of QnABot
            ├── prompts.py      # prompts for qna
        ├── utils
            ├── _init__.py
            ├── export_utils.py      #  all export function
            ├── llm_utils.py         # llm details
            ├── pdf_utils.py         # extract text with pages
            ├── qna_utils.py         # parse qna
    ├── QnaRag        # RAG-specific pipeline for document processing and retrieval.
        ├── rag_pipeline
            ├── _init__.py
            ├── pdf_process.py   # process pdf
            ├── prompt.py        # prompt for rag 
    ├── __init__.py
    ├── config.py       
├── style
    ├── styles.css         # style file
├── templates 
    ├──  index.html        #  html bacbone    
├── .gitignore             
├── LICENSE                                
├── app.py       # app details
├── logger.py 
├── README.md          
├── requirements.txt   # installation details   
└── setup.py           # setup details
```
**Prerequisites**  
Python 3.10++

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/aziz-ashfak/QNARAG.git
cd QNARAG
```
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage
Run the FastAPI app locally:
```bash
uvicorn app:app --reload
```
## 🚀 This APP is available in web 
### Web service link 
```bash
  https://qnarag.onrender.com
```
## 🤝 Contributing
Contributions are welcome! Please **fork** this repo and submit a **pull request**.  

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.  

---

## 🙌 Acknowledgements
- [LangChain](https://www.langchain.com/) – LLM orchestration  
- [HuggingFace](https://huggingface.co/) – Transformers & embeddings  
- [FAISS](https://faiss.ai/) – Vector search engine  
- [FastAPI](https://fastapi.tiangolo.com/) – High-performance API framework  
- [Groq](https://groq.com/) – For free LLMs
---

## 👤 Author
**Aziz Ashfak**  
📧 [azizashfak@gmail.com](mailto:azizashfak@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/aziz-ashfak1/)  
🐙 [GitHub](https://github.com/aziz-ashfak)  
