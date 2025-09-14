from langchain.prompts import ChatPromptTemplate

prompt=ChatPromptTemplate.from_template(
"""
You are an AI research assistant with expertise in analyzing academic papers. 
Answer the user's question based only on the provided context.
If the answer is not found in the context, state that clearly.
Context: {context}
Questions:{input}

"""
)
