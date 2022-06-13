
import context
import pymongo
import requests
import json
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1920, 1080))  
display.start()
#collection
uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
client = pymongo.MongoClient(uri)

company_data_with_id = client.get_database(name="geography_sizing").get_collection(name='company_data_with_id')

file = open('logs/final_pipeline.txt','w')

def check_revenue(id):
    for doc in revenue_data.find({},no_cursor_timeout=True):
        if doc['_id'] == id:
            return True
    return False
def check_final_results(id):
    for doc in final_results.find({},no_cursor_timeout=True):
        if doc['_id'] == id:
            return True
    return False
#print(check_final_results(8876))
ids, companies, websites = [], [], []
for doc in company_data_with_id.find({}):
    ids.append(doc['_id'])
    companies.append(doc["company_name"])
    websites.append(doc['Company_url'])


#for doc in company_data_with_id.find({},no_cursor_timeout=True):
for i in range(100):
    #collection
    uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
    client = pymongo.MongoClient(uri)

    company_data_with_id = client.get_database(name="geography_sizing").get_collection(name='company_data_with_id')
    revenue_data = client.get_database(name="geography_sizing").get_collection(name = 'revenue_leaf_sizing')
    #company_data_with_id = client.get_database(name="geography_sizing").get_collection(name = 'company_data_with_id')
    final_results =  client.get_database(name="geography_sizing").get_collection(name = 'Final_Results')

    #company = doc["company_name"]
    #website = doc['Company_url']
    #ID = doc['_id']
    ID,  company, website= ids[i], companies[i], websites[i]


    #if ID not in  [7,85,11]:
    #    continue
    file.write('\nID : {}'.format(ID))

    response = requests.post('http://20.25.81.60:3030/geography_revenue',#timeout=180,

                json={

                        "id":ID,

                        "company_name":company,

                        "company_website":website

                        }

                )
    file.write('\tResponse: {}  & Response status : '.format(response, response.status_code))


#print(type(result["revenue"]))
    print(response.text)
    if response.status_code == 200:
        result = json.loads(response.text)
        rev=result["revenue"]
        rec = {'_id': ID, 'CompanyName': company, 'Website': website, 'revenue':rev}
        obj = context.context(ID, company, website, rev)
        obj.Distribute()
        new_scraping_values = {"$set": obj.Data}
        company_data_with_id.update_one({"_id":ID}, new_scraping_values)
        rec_final = {'_id': ID, 'CompanyName': company, 'Website': website, 'output': obj.Data_out}
        if check_final_results(ID):
            new_values = {"$set": rec_final}
            final_results.update_one({"_id":ID}, new_values )

        else:
            final_results.insert_one(rec_final)
        
        if check_revenue(ID):
            query = {"_id":ID}
            new_values = {"$set": rec}
            revenue_data.update_one(query,new_values)
        else:
            revenue_data.insert_one(rec)

    else:
        rec = {'_id': ID, 'CompanyName': company, 'Website': website, 'revenue': "Revenue Not Found"}
        if check_revenue(ID):
            query = {"_id":ID}
            new_values = {"$set": rec}
            revenue_data.update_one(query,new_values)
        else:
            revenue_data.insert_one(rec)
        
file.close()
display.stop()