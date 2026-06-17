import chroma
from chroma.chroma_utils import collection_name, chroma_client, ef


def main():
    try:
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
        
        
    except Exception as e:
        print(f"Unknown error: {e}")    
        return str({e})