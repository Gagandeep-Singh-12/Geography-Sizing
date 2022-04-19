from tracemalloc import start
from flask import Flask, request, jsonify
import requests
import context
from utils import validate_json
import time, pickle, json
import config
local_config = config.Local_config()

app = Flask(__name__)

@app.route('/')
def home():
     return "Flask"

#gloabl variables
url1 = 'http://52.146.41.91:2020/geography_revenue'
global revenue, status, error
revenue = None
status = False
error = None
@app.route('/api', methods=['GET', 'POST'])
def testpost():
     global status, revenue, error
     print('Inside api : 1 -> status : ',status)
     input_json = request.get_json(force=True)
     print("Inside Api ",input_json)
     if validate_json(input_json):
          from pyvirtualdisplay import Display
          display = Display(visible=0, size=(1920, 1080))  
          display.start()
          response = requests.get(url1,
                        json= input_json
                        )
          print("inside api : ",response)
          print("inside api : ",response.text)
          start = time.time()
          while status == False:
               pass
          end = time.time()
          print("Time taken for status to become True : ",(end-start), "seconds")
          print("Inside api revenue :  ",revenue)
          print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
          if error != None:
               status, error =False, None
               return jsonify({"Error": "invalid company website"})
          elif revenue == None:
               status, revenue = False, None
               return jsonify({"Error": "Revenue Not Found"})
          #default value for revenue is taken to be $100, this would be provided by model from anjali ma'am
          obj = context.context(input_json["company_name"],input_json["company_website"],revenue)
          dictToReturn = obj.Ditribute()
          #print(dictToReturn)
          display.stop()
          status, revenue = False,None
          return jsonify(dictToReturn)
     else:
          return jsonify({"Error": "Invalid Schema"})

@app.route('/leaf_sizing', methods=['POST'])
def get_revenue():
     global status, revenue, error
     print('Inside leaf sizing : 1 -> status : ',status)
     input_json = request.get_json(force=True)
     print(input_json)
     if 'error' in input_json.keys():
          error,status = input_json['error'], True
     else:
          if input_json["revenue"] == None:
               revenue, status = None , True
          else:
               revenue, status = input_json["revenue"], True
     print("Inside get_revenue  :  {}".format(revenue))
     print('#############################################################')
     return jsonify(input_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080 ,debug=True)