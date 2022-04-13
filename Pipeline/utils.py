import jsonschema
from jsonschema import validate
import json
import config
import pymongo
azure_config = config.Azure_config()
local_config = config.Local_config()
client = pymongo.MongoClient(azure_config.COSMOS_CONNECTION)
mongo_data1 = client.get_database(name=azure_config.DB_NAME).get_collection(name=azure_config.COLLECTION_NAME)

file =  open('util_files/revenue.json','r') 
revenue_js = json.load(file)

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

def check_cosmos(input):
    cursor = mongo_data1.find({})
    for document in cursor:
        if document['_id'] == input["company_name"]:
            return True
        else:
            return False

def check_revenue():
    #with open('util_files/revenue.json','r') as file:
    #    revenue_js = json.load(file)
        #if there is  revenue
    if revenue_js['status']:
        return revenue_js['revenue']
    else:
        return revenue_js['status']#false



