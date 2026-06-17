import chroma
from chroma.chroma_utils import collection_name, chroma_client, ef
from logger import get_logger

logger = get_logger("chroma-main")

def main():
    try:
        
        if not collection_name:
            raise ValueError("collection name is empty or none")
         
        collection = chroma_client.create_collection(
            name=collection_name,
            metadata={"description": "A collection for storing grocery data"},
            configuration = {
                "hnsw":{
                    "space":"cosine"
                },
                "embedding_function":ef
            }
        )
        
        if not collection:
            raise ValueError(f"{collection_name} is not found")
        
        logger.info(f"{collection_name} is created")
        
        
    except Exception as e:
        logger.error(f"Unknown error: {e}")    
        return str({e})