import json

# def parse_qna(qna_json_str):
#     if not qna_json_str or not qna_json_str.strip():
#         return []
#     try:
#         return json.loads(qna_json_str)
#     except json.JSONDecodeError:
#         return []
# import json
#from logging import Logger


def parse_qna(qna_text):
    """
    Parse Q&A text into a list of dictionaries with 'page', 'question', and 'answer' keys.
    
    Args:
        qna_text (str): Raw or refined Q&A text from the model, expected to be a JSON string.
    
    Returns:
        list: List of dictionaries containing Q&A pairs with page numbers.
    """
    try:
        # Remove any code block markers (e.g., ```json or ```)
        qna_text = qna_text.strip()
        if qna_text.startswith("```"):
            qna_text = qna_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
        
        # Parse JSON
        qna_list = json.loads(qna_text)
        
        # Validate structure
        parsed_qnas = []
        for qa in qna_list:
            if not isinstance(qa, dict):
             
                continue
            if "question" not in qa or "answer" not in qa:
                
                continue
            # Ensure page is included, even if None
            qa_dict = {
                "page": qa.get("page"),
                "question": qa["question"],
                "answer": qa["answer"]
            }
            parsed_qnas.append(qa_dict)
        
 
        return parsed_qnas
    
    except json.JSONDecodeError as e:
        return []
    except Exception as e:
        return []
# import json
# import re
# import re
# def parse_qna(output: str):
#     """
#     Try to parse QnAs from model output.
#     Supports JSON format or plain text (Q: / A: style).
#     """
#     qnas = []

#     # --- First try: JSON format ---
#     try:
#         data = json.loads(output)
#         if isinstance(data, list):
#             for item in data:
#                 qnas.append({
#                     "question": item.get("question", "").strip(),
#                     "answer": item.get("answer", "").strip()
#                 })
#             if qnas:
#                 return qnas
#     except Exception:
#         pass

#     # --- Fallback: plain text format ---
#     qa_pairs = re.findall(r"(?:Q\d*[:.-]\s*)(.*?)(?:\n\s*A\d*[:.-]\s*)(.*?)(?=\n\s*Q|\Z)", output, re.S | re.I)
#     for q, a in qa_pairs:
#         qnas.append({
#             "question": q.strip(),
#             "answer": a.strip()
#         })

#     return qnas
