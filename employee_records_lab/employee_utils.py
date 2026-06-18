import chromadb
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name= "all-MiniLM-L6-v2"
)

client = chromadb.Client()
collection_name = "employee_collection"