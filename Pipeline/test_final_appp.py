import pymongo
import requests

#uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
#client = pymongo.MongoClient(uri)
#mongo_data = client.get_database(name="geography_sizing").get_collection(name='Final_Results')

url1 = 'http://20.231.206.6:2020/geography_sizing'
url2 = 'http://127.0.0.1:2020/geography_sizing'
url3 = 'http://10.0.0.4:2020/geography_sizing'

url = 'http://20.231.206.6:2020/landing_page'

#for document in mongo_data.find({}):
#resp = requests.get('http://20.231.206.6:2020')
#print(resp.text)
       
resp = requests.post(url1,
                json ={
	"id" : 14,
	"company_name" : "Adaptimmune",
	"company_website" : "https://www.adaptimmune.com",

}
                )
print(resp.text)

'''
resp = requests.get(url2,
                                json = {
                                        "id" : document['_id'],
                                        "company_name" : document['CompanyName'],
                                        "company_website" : document['Website']
                                        }
                                )
'''
        








                        
                      
