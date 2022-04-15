import context
import pymongo
import config

azure_config = config.Azure_config()
client = pymongo.MongoClient(azure_config.COSMOS_CONNECTION)
mongo_data1 = client.get_database(name=azure_config.DB_NAME).get_collection(name='testing_chronjob')

file = open('logs/chronejob.txt','w')
cursor = mongo_data1.find({})
for document in cursor:
    scrape = context.context(document["Compnay_Name"],document["Compnay_url"])
    record = scrape.Scraper()
    query = {"_id":document["_id"]}
    mongo_data1.update_one(query,record)
    file.write("Updated : {} -> {}\n".format(document["Compnay_Name"],document["Compnay_url"]))
file.close()


