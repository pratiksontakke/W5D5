# rag/main.py

from rag.utils.query_parser import detect_sources
from rag.agents.query_agent import get_agent
from rag.chains.summarization_chain import generate_summary

def process_user_query(query: str):
    sources = detect_sources(query)
    results = {}

    for source in sources:
        try:
            agent = get_agent(source)
            answer = agent.run(query)
            results[source] = answer
        except Exception as e:
            results[source] = f"Error: {str(e)}"

    return generate_summary(results)

if __name__ == "__main__":
    question = input("Ask your question: ")
    final_answer = process_user_query(question)
    print("\n✅ Final Answer:\n", final_answer)
