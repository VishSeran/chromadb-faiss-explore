from chroma.logger import get_logger
from employee_records_lab.employee_utils import client, ef, collection_name

logger = get_logger("employee_logger")

def main ():
    
    try:
        
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "A collection for storing employee data"},
            configuration={
                "hnsw":{
                    "space":"cosine"
                },
                "embedding_function":ef
            }
        )
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return str({e})