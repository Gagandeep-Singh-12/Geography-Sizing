import pymongo

uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
client = pymongo.MongoClient(uri)
mongo_data1 = client.get_database(name="geography_sizing").get_collection(name='company_data_with_id')

import pandas as pd
df = pd.read_csv('/home/celebal/Data/genome_prod_20220113-companies.csv')

for i in range(len(df)):
    id = int(df.iloc[i,0])
    name = df.iloc[i, 2]
    web = df.iloc[i, 6]
    rec = {'_id' : id, 'company_name' : name, 'Company_url' : web, 'Linkedin': '', 'Glassdoor' : '', 'Website': ''}
    mongo_data1.insert_one(rec)
    #print(rec)