from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
loader=Docx2txtLoader("data/Employee_Handbook.docx")
docs=loader.load()
splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)
chunks=splitter.split_documents(docs)
model=SentenceTransformer("BAAI/bge-base-en-v1.5")
client=chromadb.PersistentClient(path="vectordb")
collection=client.get_or_create_collection(name="employee_handbook")
#add chunks
for i,chunk in enumerate(chunks):
    embedding=model.encode(chunk.page_content).tolist()
    collection.add(
        ids=[f"handbook_{i}"],
        documents=[chunk.page_content],
        embeddings=[embedding]
    )
print("Employee handbook ingested successfully!")
