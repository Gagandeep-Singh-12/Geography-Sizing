from flask import Flask, request, jsonify
import pymongo
import us
import pandas as pd
from flask_cors import CORS, cross_origin
import requests
from utils import validate_json
import pymongo
import config

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
     return "Flask here"

@app.route('/landing_page', methods=['GET'])
def get_results():
    ls = []
    uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
    client = pymongo.MongoClient(uri)
    mongo_data = client.get_database(name="geography_sizing").get_collection(name='Final_Results')
    cursor = mongo_data.find({})
    for document in  cursor:
        #print(document)
        d = {"id" : document['_id'],
            "company_name": document['CompanyName'],
            "company_website": document['Website']}
        ls.append(d)
    return jsonify({   'result':ls })

@app.route('/geography_sizing', methods=['POST'])
def get_geo_sizing():
    input_json = request.get_json(force=True)
    #inp = request.json
    #print(inp)
    #print(input_json)
 
    input_json = request.get_json(force=True)
    print("geography sizing : ", input_json)

    uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
    client = pymongo.MongoClient(uri)
    mongo_data = client.get_database(name="geography_sizing").get_collection(name='Final_Results')
    cursor = mongo_data.find({})

    if validate_json(input_json):
        for document in cursor:
            #print(document)
            if document["_id"] == input_json["id"]:
                
                if "Error" in list(document["output"].keys()):
                    return jsonify(document["output"])
                else:
                    doc_out = code2country(document["output"])
                    return jsonify(doc_out)
        return jsonify({"Error": 'Company not present in data'})    
    else:
        return jsonify({"Error": "Invalid Schema"})
    


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def code2country(dist_dict):
    country_df = pd.read_csv(local.COUNTRY_DATA_PATH)
    c_keys = list(dist_dict["Country"].keys())
    for c in c_keys:
        countries = list(country_df.loc[country_df['alpha2'] == c]["en"].values)
        if countries != []:
                dist_dict["Country"][countries[0]] = dist_dict["Country"].pop(c)
    s_keys = list(dist_dict["State"].keys())
    for c in s_keys:
        countries = list(country_df.loc[country_df['alpha2'] == c]["en"].values)
        if c == 'us':
            us_keys = list(dist_dict["State"]["us"].keys())
            for s in us_keys:
                state = us.states.lookup(s)
                if state != None:
                    dist_dict["State"]['us'][str(state)]= dist_dict["State"]['us'].pop(s)
        if countries != []:
                dist_dict["State"][countries[0]] = dist_dict["State"].pop(c)
    return dist_dict

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2020 ,debug=True)
    