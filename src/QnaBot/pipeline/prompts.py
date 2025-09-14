qna_prompt_template = """
You are an expert at creating high-quality exam-style Question-Answer (QnA) pairs
from programming materials, coding tutorials, and documentation.

Your goal is to prepare coders and programmers for exams, coding interviews, and real-world problem solving.

I will give you a passage of text. Based on it:
- Generate exactly {num_questions} QnA pairs.
- If page_num is provided, include it as "page".
- Cover key definitions, concepts, use-cases, and coding logic.
- Include a mix of conceptual, practical, and problem-solving questions.
- Keep answers concise, correct, and based ONLY on the given text.
- Do not invent information that is not present in the text.

------------
{text}
------------

Output format (JSON list):
[
  {{
    "page": {page_num},
    "question": "What is ...?",
    "answer": "..."
  }},
  ...
]
"""

refine_prompt_template = """
You are an expert editor for technical Question-Answer (QnA) sets.

I will provide you with a list of QnAs generated from programming materials.
Your task is to refine them without losing meaning.

Requirements:
- Keep the same number of QnAs.
- If page numbers exist, keep them intact.
- Make questions clearer, more natural, and exam-ready.
- Ensure answers remain factually correct and concise.
- Use simple, precise language suitable for programmers preparing for exams.
- Keep JSON output format.

------------
{qna_list}
------------

Output format (JSON list):
[
  {{
    "page": 1,
    "question": "Refined question...",
    "answer": "Refined answer..."
  }},
  ...
]
"""