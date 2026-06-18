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
            
            # Example 2: Search for leadership roles
            
        print("\n2. Searching for leadership and management roles:")
        query_text = "team leader manager with experience"
        results = collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        print(f"Query: '{query_text}'")
        for i, (doc_id, document, distance) in enumerate(zip(
            results['ids'][0], results['documents'][0], results['distances'][0]
        )):
            metadata = results['metadatas'][0][i]
            print(f"  {i+1}. {metadata['name']} ({doc_id}) - Distance: {distance:.4f}")
            print(f"     Role: {metadata['role']}, Experience: {metadata['experience']} years")
            
        print("\n=== Metadata Filtering Examples ===")

        # Example 1: Filter by department
        print("\n3. Finding all Engineering employees:")
        results = collection.get(
            where={"department": "Engineering"}
        )
        print(f"Found {len(results['ids'])} Engineering employees:")
        for i, doc_id in enumerate(results['ids']):
            metadata = results['metadatas'][i]
            print(f"  - {metadata['name']}: {metadata['role']} ({metadata['experience']} years)")

        # Example 2: Filter by experience range
        print("\n4. Finding employees with 10+ years experience:")
        results = collection.get(
            where={"experience": {"$gte": 10}}
        )
        print(f"Found {len(results['ids'])} senior employees:")
        for i, doc_id in enumerate(results['ids']):
            metadata = results['metadatas'][i]
            print(f"  - {metadata['name']}: {metadata['role']} ({metadata['experience']} years)")

        # Example 3: Filter by location
        print("\n5. Finding employees in California:")
        results = collection.get(
            where={"location": {"$in": ["San Francisco", "Los Angeles"]}}
            )
        
        print(f"Found {len(results['ids'])} employees in California:")
        for i, doc_id in enumerate(results['ids']):
            metadata = results['metadatas'][i]
            print(f"  - {metadata['name']}: {metadata['location']}")
            
        print("\n=== Combined Search: Similarity + Metadata Filtering ===")
        # Example: Find experienced Python developers in specific locations
        print("\n6. Finding senior Python developers in major tech cities:")
        
        query_items =  "senior Python developer full-stack"
        results = collection.query(
            query_texts=[query_items],
            n_results=3,
            where={
                "$and":[
                    {"experience": {"$gte": 8}},
                    {"location": {"$in": ["San Francisco", "New York", "Seattle"]}}
                ]
            }
        )
        
        print(f"Query: '{query_text}' with filters (8+ years, major tech cities)")
        print(f"Found {len(results['ids'][0])} matching employees:")
        for i, (doc_id, document, distance) in enumerate(zip(
            results['ids'][0], results['documents'][0], results['distances'][0]
        )):
            metadata = results['metadatas'][0][i]
            print(f"  {i+1}. {metadata['name']} ({doc_id}) - Distance: {distance:.4f}")
            print(f"     {metadata['role']} in {metadata['location']} ({metadata['experience']} years)")
            print(f"     Document snippet: {document[:80]}...")
            
    except Exception as e:
        logger.error("Error in advance search: {e}")
        return str({e})