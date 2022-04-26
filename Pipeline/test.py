
import random
import time
import context
import pandas as pd
import pickle
l=[]
df = pd.read_csv("/home/celebal/Data/companies_data.csv")
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))  
display.start()

import pymongo

uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
client = pymongo.MongoClient(uri)
mongo_data2 = client.get_database(name="geography_sizing").get_collection(name='company_data_with_id')
cursor2 = mongo_data2.find({})

for document in cursor2:
    start = time.time()
    obj = context.context(document['_id'],document['company_name'], document['Compnay_url'],100)
    res = obj.Distribute()
    print(res)
    print('----------------------------------------------')
    l.append(res)
    end = time.time()
    file = open('/home/celebal/Pipeline/logs/context.txt','a')
    file.write('Time taken for {} company = {} min\n'.format(document['_id'],(end-start)/60))
    pickle.dump(l, open('outputs/context_output.pkl', 'wb'))
display.stop()

'''
#try:
for i in range(900, len(df)):
    start = time.time()
    company = df.iloc[i, 3]
    website = df.iloc[i, 0]
    obj = context.context(company,website,100)
    res = obj.Ditribute()
    l.append(res)
    end = time.time()
    file = open('/home/celebal/Pipeline/logs/context.txt','a')
    file.write('Time taken for {} company = {} min\n'.format(company,(end-start)/60))
    pickle.dump(l, open('outputs/context_output.pkl', 'wb'))
    #min = random.randint(1,2)
    #time.sleep(min*60)
#except Exception as e:
    #display.stop()
    #file = open('logs/context.txt','a')
    #file.write(str(e))
    #file.close()
display.stop()


'''
