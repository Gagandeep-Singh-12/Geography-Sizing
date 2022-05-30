from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from utils import validate_json
import pymongo

app = Flask(__name__)
#CORS(app)

@app.route('/')
def home():
     return "Flask HERE"

@app.route('/geography_sizing', methods=['GET', "OPTIONS"])
def get_results():
    if request.method == "OPTIONS" :
        return _build_cors_preflight_response()

    elif request.method == "GET" :
        input_json = request.get_json(force=True)

        uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
        client = pymongo.MongoClient(uri)
        mongo_data = client.get_database(name="geography_sizing").get_collection(name='Final_Results')
        cursor = mongo_data.find({})

        if validate_json(input_json):
            for document in cursor:
                #print(document)
                if document["_id"] == input_json["id"]:
                    return _corsify_actual_response(jsonify(document["output"]))
                    #response.headers.add("Access-Control-Allow-Origin", "*")
                    #return response
            return _corsify_actual_response(jsonify({"Error": 'Company not present in data'}))    
        else:
            return _corsify_actual_response(jsonify({"Error": "Invalid Schema"}))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2020 ,debug=True)

'''
@app.route('/landing_page', methods=['GET'])
def get_landing_page():
    ls = []
    for document in cursor:
        #print(document)
        d = {"id" : document['_id'],
            "company_name": document['CompanyName'],
            "company_website": document['Website']}
        ls.append(d)
    return jsonify({
        'result':ls
    }) 
'''

    