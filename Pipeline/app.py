from ipaddress import ip_address
from flask import Flask, request, jsonify
import context

app = Flask(__name__)

@app.route('/')
def home():
     return "Flask"

@app.route('/api', methods=['GET', 'POST'])
def testpost():
     input_json = request.get_json(force=True)
     #default value for revenue is taken to be $100, this would be provided by model from anjali ma'am
     obj = context.context(input_json["Comapny_name"],input_json["Company_URL"],100)
     dictToReturn = obj.Ditribute()
     print(dictToReturn)
     return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080 ,debug=True)