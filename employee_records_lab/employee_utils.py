import chromadb
from chromadb.utils import embedding_functions
from chromadb import Collection

from chroma.logger import get_logger

logger = get_logger("employee_utils_logger")

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name= "all-MiniLM-L6-v2"
)

client = chromadb.Client()
collection_name = "employee_collection"

def perform_advance_search(collection:Collection, all_items):
    try:
        
        print("=== Similarity Search Examples ===")
        
        # Example 1: Search for Python developers
        print("\n1. Searching for Python developers:")
        query_text = "Python developer with web development experience"
        results = collection.query(
            query_texts=[query_text],
            n_results=3
        ) 
        
        print(f"Query: {query_text}")
        
        for i , (doc_id, document, distance) in enumerate(zip(
            results['ids'][0], results['documents'][0], results['distances'][0])):
            
            metadata = results['metadatas'][0][i]
            print(f"  {i+1}. {metadata['name']} ({doc_id}) - Distance: {distance:.4f}")
            print(f"     Role: {metadata['role']}, Department: {metadata['department']}")
            print(f"     Document: {document[:100]}...")
        
    except Exception as e:
        logger.error("Error in advance search: {e}")
        return str({e})