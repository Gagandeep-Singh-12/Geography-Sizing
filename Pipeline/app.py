import utils
from flask import Flask, request, jsonify
import requests
import context
from utils import validate_json
import time, pickle, json

app = Flask(__name__)

@app.route('/')
def home():
     return "Flask"
url1 = 'http://52.146.41.91:2020/geography_revenue'
revenue = None

@app.route('/api', methods=['GET', 'POST'])
def testpost():

     input_json = request.get_json(force=True)
     if validate_json(input_json):
          from pyvirtualdisplay import Display
          display = Display(visible=0, size=(1920, 1080))  
          display.start()
          #context.context()
          response = requests.get(url1,

                        json= input_json

                        )
          print("inside api : ",response)
          print("inside api : ",response.text)
          '''
          
          if utils.check_cosmos(input_json):
               
          '''
          #time.sleep(30)
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
          print("Inside api revenue :  ",revenue)
          #default value for revenue is taken to be $100, this would be provided by model from anjali ma'am
          #obj = context.context(input_json["Comapny_name"],input_json["Company_URL"],100)
          obj = context.context(input_json["company_name"],input_json["company_website"],100)
          dictToReturn = obj.Ditribute()
          print(dictToReturn)
          display.stop()
          json.dump({'revenue' : False, 'status':False}, open('util_files/revenue.json','w'))
          return jsonify(dictToReturn)
     else:
          return jsonify({"Error": "Invalid Schema"})

@app.route('/leaf_sizing', methods=['POST'])
def get_revenue():
     input_json = request.get_json(force=True)
     print(input_json)
     if input_json['totalRevenue'] == None:
          revenue, status = False , False
     else:
          status = True
          revenue = input_json['totalRevenue']
     print("Inside get_revenue  :  {}".format(revenue))
     json.dump({'revenue' : revenue, "status" : status}, open('util_files/revenue.json','w'))
     return jsonify(input_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080 ,debug=True)