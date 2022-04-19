import jsonschema
from jsonschema import validate
import json
import config
import pymongo
azure_config = config.Azure_config()
local_config = config.Local_config()
client = pymongo.MongoClient(azure_config.COSMOS_CONNECTION)
mongo_data1 = client.get_database(name=azure_config.DB_NAME).get_collection(name=azure_config.COLLECTION_NAME)


def get_schema():
    """This function loads the given schema available"""
    with open('util_files/input_schema.json', 'r') as file:
        schema = json.load(file)
    return schema

def validate_json(json_data):
    # Describe what kind of json you expect.
    execute_api_schema = get_schema()
    try:
        validate(instance=json_data, schema=execute_api_schema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True



