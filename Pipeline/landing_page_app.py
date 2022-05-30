from flask import Flask, request, jsonify
import pymongo

app = Flask(__name__)

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
    response = jsonify({   'result':ls }) 
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3030 ,debug=True)
    