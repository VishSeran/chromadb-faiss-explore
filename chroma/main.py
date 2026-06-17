import chroma
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
