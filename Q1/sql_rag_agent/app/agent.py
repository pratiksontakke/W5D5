import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# --- LLM and Embeddings ---
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# --- Agent and Tools ---
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.agent_toolkits import create_sql_agent
from langchain.tools.retriever import create_retriever_tool
from langchain.tools import Tool  # <<< --- IMPORT THIS
from langchain import hub

# --- Database and Vector Store ---
from langchain_community.utilities import SQLDatabase
from langchain_chroma import Chroma  # <<< --- CORRECTED CHROMA IMPORT

# --- 1. CONFIGURATION ---
load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
DB_PATH = os.path.join(ROOT_DIR, 'data', 'db', 'customer_support.db')
CHROMA_PERSIST_DIR = os.path.join(ROOT_DIR, 'vector_store', 'chroma_db')

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- 2. SETUP THE TOOLS ---

# === TOOL 1: SQL Database Tool (CORRECTED) ===
def get_sql_tool():
    """
    Initializes the SQL Database and wraps the SQL agent executor in a Tool.
    """
    print("Initializing SQL Tool...")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    db = SQLDatabase(engine=engine)

    # 1. Create the specialized SQL Agent Executor
    sql_agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=True
    )

    # 2. Wrap it in a Tool object
    # This gives it the .name and .description attributes the main agent needs
    sql_tool = Tool(
        name="sql_database_query",
        func=sql_agent_executor.invoke,
        description="Use this tool for specific questions about the customer support database, including tickets, statuses, and categories. Input should be a full question."
    )
    return sql_tool

# === TOOL 2: RAG (Vector Store) Tool ===
def get_rag_tool():
    """Initializes the ChromaDB vector store and creates a retriever tool."""
    print("Initializing RAG Tool...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    retriever_tool = create_retriever_tool(
        retriever,
        "support_ticket_description_search", # A more descriptive name
        "Searches and returns relevant excerpts from support ticket descriptions. Use this for questions about how to solve a problem, what a problem was about, or other qualitative inquiries."
    )
    return retriever_tool

# --- 3. CREATE THE AGENT ---
def create_main_agent():
    """Combines all tools into a single, powerful agent."""
    print("Creating the main agent...")
    sql_tool = get_sql_tool()
    rag_tool = get_rag_tool()
    tools = [sql_tool, rag_tool]

    prompt = hub.pull("hwchase17/openai-functions-agent")

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

# --- 4. MAIN FUNCTION TO PROCESS QUERIES ---
main_agent = create_main_agent()

def get_answer(query: str):
    """
    Takes a user query, processes it with the main agent, and returns the final answer.
    """
    if not query:
        return "Please provide a question."
    print(f"\nProcessing query: '{query}'")
    try:
        response = main_agent.invoke({"input": query})
        return response.get("output", "Sorry, I couldn't find an answer.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request. Please try again."

# --- 5. EXAMPLE USAGE ---
if __name__ == '__main__':
    print("Agent is ready. Running test queries...")

    query_a = "How many tickets have a 'Pending' status?"
    answer_a = get_answer(query_a)
    print("\n" + "="*50)
    print(f"Query A: {query_a}")
    print(f"Answer A: {answer_a}")
    print("="*50 + "\n")

    query_b = "What are the common solutions for Wi-Fi connection problems?"
    answer_b = get_answer(query_b)
    print("\n" + "="*50)
    print(f"Query B: {query_b}")
    print(f"Answer B: {answer_b}")
    print("="*50)