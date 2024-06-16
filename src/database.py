import pandas as pd
import dotenv
import os
import json
from pymongo import MongoClient

class Database:
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.__mongo_info = {
            "uri": os.getenv("MONGO_URI"),
            "database": os.getenv("MONGO_DATABASE"),
            "identifier_collection": os.getenv("MONGO_IDENTIFIER_COLLECTION"),
            "data_collection": os.getenv("MONGO_DATA_COLLECTION")
        }
        self.__initialize_identifiers()
        # Make sure all the required environment variables are set
        if not all(self.__mongo_info.values()):
            raise ValueError(f"Please set all the required environment variables related to the database. missing: {', '.join([x for x, y in self.__mongo_info.items() if not y])}")


    def get_identifiers(self) -> list:
        client = self.__open_connection()
        db = client[self.__mongo_info["database"]]
        identifier_collection = db[self.__mongo_info["identifier_collection"]]
        identifiers = list(identifier_collection.find({}))
        client.close()
        return identifiers
        
    def get_data(self, identifier: str) -> pd.DataFrame:
        client = self.__open_connection()
        db = client[self.__mongo_info["database"]]
        data_collection = db[self.__mongo_info["data_collection"]]
        data = list(data_collection.find({"identifier": identifier}, {"_id": 0}))
        client.close()
        return pd.DataFrame(data)
    
    def add_identifier(self, identifier: str, description: str, datatype: str) -> None:
        # Load the existing identifiers
        identifiers = self.get_identifiers()
        print(identifiers)
        # Add the new identifier
        new_identifier = {
            "_id": f"{identifier.lower()}_{datatype}",
            "identifier": identifier.lower(),
            "description": description,
            "datatype": datatype
        }
        # Make sure identifiers are unique
        if new_identifier["_id"] in [x["_id"] for x in identifiers]:
            raise ValueError(f"Identifier '{identifier}' already exists.")
        identifiers.append(new_identifier)
        client = self.__open_connection()
        db = client[self.__mongo_info["database"]]
        identifier_collection = db[self.__mongo_info["identifier_collection"]]
        identifier_collection.insert_one(new_identifier)
        client.close()

    def add_entry(self, data: pd.DataFrame) -> None:
        client = self.__open_connection()
        db = client[self.__mongo_info["database"]]
        data_collection = db[self.__mongo_info["data_collection"]]
        records = json.loads(data.to_json(orient='records'))
        data_collection.insert_many(records)
        client.close()

    def __initialize_identifiers(self) -> None:
        # Make sure the identifiers collection is empty
        # Check if identifiers are already initialized
        current_identifiers = self.get_identifiers()
        if len(current_identifiers) > 0:
            return

        client = self.__open_connection()
        db = client[self.__mongo_info["database"]]
        identifier_collection = db[self.__mongo_info["identifier_collection"]]
        identifier_collection.delete_many({})
        client.close()
        self.add_identifier("name", "The unique name of the entry", "str")

    def __open_connection(self) -> MongoClient:
        return MongoClient(self.__mongo_info["uri"])