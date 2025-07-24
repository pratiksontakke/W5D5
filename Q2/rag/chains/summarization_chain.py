# rag/chains/summarization_chain.py

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

summary_prompt = PromptTemplate(
    input_variables=["results"],
    template="""
Summarize the product-related results below for the user.

{results}

Respond in clear and helpful language.
"""
)

summarizer = summary_prompt | llm

def generate_summary(results: dict) -> str:
    joined = "\n\n".join([f"Source: {k}\n{k_res}" for k, k_res in results.items()])
    return summarizer.invoke({"results": joined})
