from chroma.logger import get_logger
from employee_records_lab.employee_utils import client, ef, collection_name
from employee_records_lab.employee_data import employees

logger = get_logger("employee_logger")


def main():

    try:
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "A collection for storing employee data"},
            configuration={"hnsw": {"space": "cosine"}, "embedding_function": ef},
        )

        if not collection:
            raise ValueError(f"{collection_name} is empty or none")

        logger.info(f"{collection_name} is created")

        employees_documents = []

        for employee in employees:
            document = f"{employee['role']} with {employee['experience']} years of experience in {employee['department']}."
            document += (
                f"Skills: {employee['skills']}. Located in {employee['location']}."
            )
            document += f"Employment type: {employee['employment_type']}."
            employees_documents.append(document)

        employees_ids = [employee["id"] for employee in employees]

        if not employees_ids or employees_documents:
            raise ValueError("emplyees ids or employees document is empty or none")

        collection.add(
            ids=employees_ids,
            documents=employees_documents,
            metadatas=[
                {
                    "name": employee["name"],
                    "department": employee["department"],
                    "role": employee["role"],
                    "experience": employee["experience"],
                    "location": employee["location"],
                    "employment_type": employee["employment_type"],
                }
                for employee in employees
            ],
        )
        all_items = collection.get()
        
        if len(all_items) == 0:
            logger.warning(f"{collection_name} is not updated")
            raise ValueError("Collection is not updated")
        
        logger.info(f"{collection_name} is updated")
        print("Collection contents:")
        print(f"Number of documents: {len(all_items['documents'])}")

    except ValueError as e:
        logger.error(f"value error: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return str({e})
