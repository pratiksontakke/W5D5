# rag/agents/query_agent.py

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from rag.config import DB_PATHS

llm = ChatOpenAI(model="gpt-4", temperature=0, verbose=True)

def get_agent(source: str):
    print(source)
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATHS[source]}")
    print(db)

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    return agent
