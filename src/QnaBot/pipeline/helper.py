import os
import sys
import json
import re
import markdown
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.config import load_config
from src.QnaBot.utils.pdf_utils import extract_text_with_pages
from src.QnaBot.utils.export_utils import export_to_pdf, export_to_csv, export_to_word
from src.QnaBot.utils.llm_utils import refine_qna, generate_qna
from src.QnaBot.utils.qna_utils import parse_qna
from config import load_config
from logger import logger 

def extract_output(uploaded_file_path, num_questions, mode):
    logger.debug(f"Processing file: {uploaded_file_path}, num_questions: {num_questions}, mode: {mode}")
    try:
        pages = extract_text_with_pages(uploaded_file_path)
        logger.debug(f"Extracted {len(pages)} pages: {[p['page'] for p in pages]}")
        
        if not pages:
            logger.warning("No pages extracted from PDF")
            markdown_text = "# Q&A Results\n\nNo Q&A generated: Empty PDF."
            return markdown_text, markdown.markdown(markdown_text, extensions=['extra']), []

        client = load_config()
        all_qnas = []

        if mode == "Per Page":
            for page in pages:
                if not page["text"].strip():
                    logger.debug(f"Skipping empty page {page['page']}")
                    continue
                logger.debug(f"Generating Q&A for page {page['page']}")
                raw_qna = generate_qna(client, page["text"], num_questions, page_num=page["page"])
                logger.debug(f"Raw Q&A for page {page['page']}: {raw_qna}")
                refined_qna = refine_qna(client, raw_qna)
                logger.debug(f"Refined Q&A for page {page['page']}: {refined_qna}")
                try:
                    parsed_qna = parse_qna(refined_qna)
                    logger.debug(f"Parsed Q&A for page {page['page']}: {parsed_qna}")
                except Exception as e:
                    logger.error(f"Error parsing Q&A for page {page['page']}: {e}")
                    parsed_qna = []
                for qa in parsed_qna:
                    qa["page"] = page["page"]
                    all_qnas.append(qa)
        else:  # Merged mode
            full_text = "\n".join([p["text"] for p in pages if p["text"].strip()])
            if not full_text:
                logger.warning("No text extracted for merged mode")
                markdown_text = "# Q&A Results\n\nNo Q&A generated: No text extracted."
                return markdown_text, markdown.markdown(markdown_text, extensions=['extra']), []
            logger.debug("Generating Q&A for merged text")
            raw_qna = generate_qna(client, full_text, num_questions, page_num=None)
            logger.debug(f"Raw Q&A for merged text: {raw_qna}")
            refined_qna = refine_qna(client, raw_qna)
            logger.debug(f"Refined Q&A for merged text: {refined_qna}")
            try:
                parsed_qna = parse_qna(refined_qna)
                logger.debug(f"Parsed Q&A for merged text: {parsed_qna}")
            except Exception as e:
                logger.error(f"Error parsing Q&A for merged text: {e}")
                parsed_qna = []
            all_qnas.extend(parsed_qna)

        if not all_qnas:
            logger.warning("No Q&A pairs generated")
            markdown_text = "# Q&A Results\n\nNo Q&A pairs generated."
            return markdown_text, markdown.markdown(markdown_text, extensions=['extra']), []
        
        markdown_text = "# Q&A Results\n\n"
        for qa in all_qnas:
            page_str = f"Page {qa['page']}" if qa.get('page') else "Merged"
            markdown_text += f"## {page_str}\n\n**Question**: {qa['question']}\n\n**Answer**: {qa['answer']}\n\n"
        
        logger.debug(f"Generated Markdown Q&A: {markdown_text[:200]}...")
        html = markdown.markdown(markdown_text, extensions=['extra'])
        return markdown_text, html, all_qnas
    except Exception as e:
        logger.error(f"Error in extract_output: {e}")
        markdown_text = f"# Q&A Results\n\n**Error**: Failed to generate Q&A: {str(e)}"
        return markdown_text, markdown.markdown(markdown_text, extensions=['extra']), []
# def extract_output(uploaded_file, num_questions, mode):
#     print(f"📂 Loading PDF: {uploaded_file}")
#     pages = extract_text_with_pages(uploaded_file)
#     client = load_config()

#     if not pages:
#         print("⚠️ No pages extracted from PDF. Possibly scanned images.")
#         return []

#     print(f"📄 Extracted {len(pages)} pages from PDF.")

#     all_qnas = []

#     if mode == "Per Page":
#         for page in pages:
#             if not page["text"].strip():
#                 print(f"⚠️ Skipping empty page {page['page']}")
#                 continue

#             print(f"\n=== Processing Page {page['page']} ===")
#             print(f"📝 First 200 chars of text:\n{page['text'][:200]}...\n")

#             raw_qna = generate_qna(client, page["text"], num_questions, page_num=page["page"])
#             print(f"🤖 RAW MODEL OUTPUT (Page {page['page']}):\n{raw_qna}\n")

#             refined_qna = refine_qna(client, raw_qna)
#             print(f"✨ Refined Output (Page {page['page']}):\n{refined_qna}\n")

#             parsed_qna = parse_qna(refined_qna)
#             print(f"✅ Parsed {len(parsed_qna)} QnAs from Page {page['page']}")

#             for qa in parsed_qna:
#                 qa["page"] = page["page"]
#                 all_qnas.append(qa)

#     else:  # Merged mode
#         full_text = "\n".join([p["text"] for p in pages if p["text"].strip()])
#         if not full_text:
#             print("⚠️ No usable text found in merged mode.")
#             return []

#         print(f"📝 First 200 chars of merged text:\n{full_text[:200]}...\n")

#         raw_qna = generate_qna(client, full_text, num_questions, page_num=None)
#         print(f"🤖 RAW MODEL OUTPUT (Merged):\n{raw_qna}\n")

#         refined_qna = refine_qna(client, raw_qna)
#         print(f"✨ Refined Output (Merged):\n{refined_qna}\n")

#         parsed_qna = parse_qna(refined_qna)
#         print(f"✅ Parsed {len(parsed_qna)} QnAs from merged content.")
#         all_qnas.extend(parsed_qna)

#     # Print results
#     if all_qnas:
#         for idx, qa in enumerate(all_qnas, 1):
#             page_info = f"(Page {qa.get('page')}) " if qa.get("page") else ""
#             print(f"**{page_info}Q{idx}: {qa['question']}**")
#             print(f"A{idx}: {qa['answer']}")
#             print("---")
#     else:
#         print("⚠️ No QnAs were generated.")

#     return all_qnas


# -----------------------
# Run Example
# -----------------------
# uploaded_file = "C:/QNARAG/IEEE_SMC_2025_Omar.pdf"
# num_questions = 3
# mode = "Per Page"

# qnas = extract_output(uploaded_file, num_questions, mode)

# print(f"\n🎉 Final Generated {len(qnas)} QnAs\n")
# for qa in qnas[:3]:
#     print("Q:", qa["question"])
#     print("A:", qa["answer"])
