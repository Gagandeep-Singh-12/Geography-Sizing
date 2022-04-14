from distutils.log import error
import utils
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
revenue = None
status = False
error = None
@app.route('/api', methods=['GET', 'POST'])
def testpost():
     global status, revenue, error
     print('Inside api : 1 -> status : ',status)
     input_json = request.get_json(force=True)
     if validate_json(input_json):
          from pyvirtualdisplay import Display
          display = Display(visible=0, size=(1920, 1080))  
          display.start()
          #context.context()
          #hit url for revenue
          response = requests.get(url1,

                        json= input_json

                        )
          print("inside api : ",response)
          print("inside api : ",response.text)
          '''
          
          if utils.check_cosmos(input_json):
               
          
          time.sleep(30)
          start = time.time()
          #untill there is revenue
          while utils.check_revenue() == False:
               end = time.time()
               tt = (end - start)/60
               if  tt > 3:
                    break
               else:
                    pass
          revenue = utils.check_revenue()
          #if revenue == False:
          error = utils.get_error()
          '''
          print("Inside api revenue :  ",revenue)
          while status == False:
               pass
          if revenue == None:
               status = False
               return jsonify({"Error": "Revenue Not Found"})
          elif error != None:
               status =False
               return jsonify({"Error": error})
          #default value for revenue is taken to be $100, this would be provided by model from anjali ma'am
          #obj = context.context(input_json["Comapny_name"],input_json["Company_URL"],100)
          obj = context.context(input_json["company_name"],input_json["company_website"],revenue)
          dictToReturn = obj.Ditribute()
          print('HHHHHHH')
          print(dictToReturn)
          display.stop()
          #json.dump({'revenue' : False, 'status':False, "error":None}, open('util_files/revenue.json','w'))
          #print("Hi")
          #json.dump({'revenue' : False, 'status':False,"error":None}, local_config.revenue_file_pointer)
          status = False
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
     #json.dump({'revenue' : revenue, "status" : status, "error":error}, open('util_files/revenue.json','w'))
     #json.dump({'revenue' : revenue, "status" : status, "error":error}, local_config.revenue_file_pointer)
     return jsonify(input_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080 ,debug=True)