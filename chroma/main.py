from chromadb import Collection
from logger import get_logger
from chroma.data import texts, ids
from chroma.chroma_utils import collection_name, chroma_client, ef


logger = get_logger("chroma-main")


def main():
    try:
        if not collection_name:
            raise ValueError("collection name is empty or none")

        collection = chroma_client.create_collection(
            name=collection_name,
            metadata={"description": "A collection for storing grocery data"},
            configuration={"hnsw": {"space": "cosine"}, "embedding_function": ef},
        )

        if not collection:
            raise ValueError(f"{collection_name} is not found")

        logger.info(f"{collection_name} is created")

        collection.add(
            documents=texts,
            metadatas=[{"source": "grocery_store", "category": "food"} for _ in texts],
            ids=ids,
        )

        logger.info(f"documents added to {collection_name}")

        all_items = collection.get()
        print("Collection contents:")
        print(f"Number of documents: {len(all_items['documents'])}")

    except Exception as e:
        logger.error(f"Unknown error: {e}")
        return str({e})
    

def perform_similarity_search (collection:Collection, all_items):
    
    query_term = "apple"
    
    try:
        results = collection.query(
            query_texts=[query_term],
            n_results=3
        )
        logger.info(f"results for {query_term}: \n{results}")
        
        if not results or not results['ids'] or len(results['ids'][0]) == 0:
            print(f'No documents found similar to "{query_term}"')
            return
        
        print(f'Top 3 similar documents to "{query_term}":')
        
        for i in range(min(3, len(results['ids'][0]))):
            doc_id = results['ids'][i]
            score = results['distances'][i]
            
            text= results['documents'][i]
            
            if not text:
                print(f' - ID: {doc_id}, Text: "Text not available", Score: {score:.4f}')
            else:
                print(f' - ID: {doc_id}, Text: "{text}", Score: {score:.4f}')
        
        
        
    except ValueError as e:
        logger.error(f"Value error in similarity search: {e}")
        return str({e})
    
    except Exception as e:
        logger.error(f"Error in similarity search: {e}")
        return str({e})
