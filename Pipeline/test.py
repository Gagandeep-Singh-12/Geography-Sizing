
import random
import time
import context
import pandas as pd
import pickle
l=[]
df = pd.read_csv("/home/celebal/Data/genome_prod_20220113-companies.csv")
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))  
display.start()

import pymongo

uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
client = pymongo.MongoClient(uri)
mongo_data2 = client.get_database(name="geography_sizing").get_collection(name='company_data_with_id')
cursor2 = mongo_data2.find({})

#try:
for i in range(100):
    start = time.time()
    company = df["CompanyName"].iloc[i]
    website = df["Website"].iloc[i]
    ID = int(df["CompanyId"].iloc[i])
    obj = context.context(ID,company,website,100)
    res = obj.Distribute()
    
    l.append(res)
    end = time.time()
    file = open('/home/celebal/Pipeline/logs/context.txt','a')
    file.write('Time taken for {} company = {} min\n'.format(company,(end-start)/60))
    pickle.dump(l, open('outputs/context_output.pkl', 'wb'))
display.stop()

'''
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


