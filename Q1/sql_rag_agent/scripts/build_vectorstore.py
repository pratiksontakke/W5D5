import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# --- 1. CONFIGURATION ---
# Load environment variables from a .env file (for your OpenAI API key)
load_dotenv()

# Define the paths relative to the script's location
# This makes the script runnable from anywhere
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, '..', 'data', 'db', 'customer_support.db')
CHROMA_PERSIST_DIR = os.path.join(SCRIPT_DIR, '..', 'vector_store', 'chroma_db')
TABLE_NAME = "tech_support"
COLUMN_TO_EMBED = "Tech_Response"  

# --- 2. DATA LOADING ---
def load_data_from_db():
    """Connects to the SQLite DB and loads the data into a pandas DataFrame."""
    print(f"Loading data from '{TABLE_NAME}' table in {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
        conn.close()
        print(f"Successfully loaded {len(df)} records.")
        return df
    except Exception as e:
        print(f"Error loading data from the database: {e}")
        return None

# --- 3. DOCUMENT PREPARATION ---
def create_documents(df):
    """Converts a DataFrame into a list of LangChain Document objects."""
    print("Creating LangChain documents...")
    # Using a list comprehension for efficiency
    documents = [
        Document(
            page_content=row[COLUMN_TO_EMBED],
            # You can add other relevant columns as metadata
            metadata={
                "ticket_id": row["Conversation_ID"],
                "category": row["Issue_Category"],
                "status": row["Issue_Status"]
            }
        ) for _, row in df.iterrows() if row[COLUMN_TO_EMBED] and isinstance(row[COLUMN_TO_EMBED], str)
    ]
    print(f"Created {len(documents)} documents.")
    return documents

# --- 4. CHUNKING ---
def split_documents(documents):
    """Splits the documents into smaller chunks for better embedding and retrieval."""
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    return chunks

# --- 5. EMBEDDING AND STORAGE ---
def create_and_store_embeddings(chunks):
    """Creates embeddings and stores them in a ChromaDB persistent vector store."""
    print("Generating embeddings and creating ChromaDB vector store...")

    # Ensure the target directory exists
    if not os.path.exists(CHROMA_PERSIST_DIR):
        os.makedirs(CHROMA_PERSIST_DIR)
        print(f"Created directory: {CHROMA_PERSIST_DIR}")

    # Initialize the embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Create the Chroma vector store from the document chunks
    # This will generate embeddings and save them to the specified directory
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )
    print("Vector store created and saved successfully!")
    print(f"ChromaDB is persisting data to: {CHROMA_PERSIST_DIR}")
    return vector_store

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Step 1: Load data
    dataframe = load_data_from_db()

    if dataframe is not None and not dataframe.empty:
        # Step 2: Create documents
        docs = create_documents(dataframe)

        if docs:
            # Step 3: Split documents
            doc_chunks = split_documents(docs)

            # Step 4: Create and store embeddings
            create_and_store_embeddings(doc_chunks)
        else:
            print("No documents were created. Please check the source data.")
    else:
        print("Data loading failed or the DataFrame is empty. Halting execution.")