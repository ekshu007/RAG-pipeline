import os
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_core.tools import tool


# Absolute path to vectordb
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "vectordb")

print("RAG DB PATH:")
print(DB_PATH)


client = chromadb.PersistentClient(
    path=DB_PATH
)


print("Collections in rag_tools.py:")
print(client.list_collections())


embedding_model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5"
)

def search_collection(collection_name, query):

    # Load collection
    collection = client.get_collection(
        name=collection_name
    )

    # Convert question into vector
    query_embedding = embedding_model.encode(
        query
    ).tolist()


    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )


    # Extract chunks
    documents = results["documents"][0]


    context = "\n\n".join(documents)

    return context



@tool
def company_policy_tool(question: str):
    """
    Search company policy documents.
    Use this for questions about general company rules,
    working hours, benefits, employee guidelines.
    """

    return search_collection(
        "company_policy",
        question
    )

@tool
def employee_handbook_tool(question:str):
    """
    Search the employee handbook.
    Use this for onboarding,workplace_facilities,
    IT setup,dresss code travel reimbursement, employee benefits and general handbook questions
    if answer long generate as points
    """
    return search_collection(
        "employee_handbook",
        question
    )


@tool
def leave_policy_tool(question: str):
    """
    Search leave policy documents.
    Use this for questions about leave,
    earned leave, sick leave, holidays.
    """

    return search_collection(
        "leave_policy",
        question
    )
@tool 
def employee_skills_tool(question:str):
    """
    Search employee skills information
    Use this tool for skills about
        1: Technical expertise
        2: Experience
        3: Departmental Skills
    """
    return search_collection(""
    "employee_skills",
    question)





@tool
def code_of_conduct_tool(question: str):
    """
    Search the company's Code of Conduct.

    Use this tool for questions about:
    - Professional behaviour
    - Workplace ethics
    - Information security
    - Password policies
    - Confidential information
    - Attendance and punctuality
    - Anti-harassment policy
    - Remote work expectations
    - Company resources
    - Disciplinary actions
    """

    return search_collection(
        "code_of_conduct",
        question
    )


@tool
def hr_policy_tool(question: str):
    """
    Search HR policy documents.
    Use this for questions about HR processes,
    onboarding, resignation, notice period.
    """

    return search_collection(
        "hr_policy",
        question
    )