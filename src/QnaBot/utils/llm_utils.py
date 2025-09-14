import os
import sys
from src.QnaBot.pipeline.prompts import qna_prompt_template, refine_prompt_template

def generate_qna(client, text, num_questions=5, page_num=None):
    if not text.strip():
        return "[]"

    prompt = qna_prompt_template.format(
        num_questions=num_questions,
        text=text,
        page_num=("null" if page_num is None else page_num)
    )
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", #"llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def refine_qna(client, qna_output):
    prompt = refine_prompt_template.format(qna_list=qna_output)
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
