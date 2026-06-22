import chromadb
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection_name = "my_grocery_collection"

# Create a new instance of ChromaClient to interact with the Chroma DB
chroma_client = chromadb.Client()

