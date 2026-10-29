from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
loader = CSVLoader(
    file_path="data/employee_skills.csv"
)
documents = loader.load()
print(f"Loaded {len(documents)} rows")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)
vector_db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="vectordb",
    collection_name="employee_skills"
)

print("CSV Vector DB created successfully!")