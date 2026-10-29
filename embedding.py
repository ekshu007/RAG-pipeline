from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,  # Fixed: Lowercase 'd'
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize models and client
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

client = chromadb.PersistentClient(
    path=os.path.join(BASE_DIR, "vectordb"),
    tenant="default_tenant",
    database="default_database"
)

# Global splitter configuration
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)


def create_collection(collection_name, pdf_path):
    # Safe delete if exists
    try:
        client.delete_collection(collection_name)
    except:
        pass

    # Create fresh collection
    collection = client.create_collection(collection_name)

    # Load and split PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    docs = splitter.split_documents(pages)

    # Loop and embed
    for i, doc in enumerate(docs):
        metadata = doc.metadata or {}
        metadata["source"] = pdf_path

        embedding = model.encode(
            doc.page_content, normalize_embeddings=True
        ).tolist()

        collection.add(
            ids=[str(i)],
            documents=[doc.page_content],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    print(f"{collection_name} -> {collection.count()} chunks stored")


# Execute for your paths
create_collection("company_policy", "data/Corporate_Operations_Policy.pdf")
create_collection("leave_policy", "data/Leave_and_Time_Off_Policy.pdf")
create_collection("hr_policy", "data/HR_Policy_Manual.pdf")

print("\nAll collections created successfully!")

print("\nCollections in embedding.py:")
print(client.list_collections())