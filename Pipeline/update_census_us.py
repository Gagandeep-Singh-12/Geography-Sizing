import census_class
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))  
display.start()
census_obj = census_class.scrape_us()
census_obj.get_us_data()
clean_obj = census_class.clean_data()
clean_obj.clean_data()
display.stop()

import pymongo
uri = "mongodb://celebal:bZPUhXkQDcdWioAIiwECCdSEiZL3zmQ6bojzYjdiDxQlHhBgzKrJjiuYCWtEbSB4QcinajhByNwKbWlsRoBQ0A==@celebal.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@celebal@"
client = pymongo.MongoClient(uri)
census_data = client.get_database(name="geography_sizing").get_collection(name='census_US')
cursor = census_data.find({})
d1 = '/home/celebal/Data/census_data/US/clean_data/median_age.csv'
d2 = '/home/celebal/Data/census_data/US/clean_data/median_income.csv'
d3 = '/home/celebal/Data/census_data/US/clean_data/population.csv'
import pandas as pd

df1 = pd.read_csv(d1)
df2 = pd.read_csv(d2)
df3 = pd.read_csv(d3)
df1.drop(columns = {'Unnamed: 0'}, inplace = True)
df2.drop(columns = {'Unnamed: 0'}, inplace = True)
df3.drop(columns = {'Unnamed: 0'}, inplace = True)
state_codes = list(df1.state_code.values)
median_age = [int(i) for i in list(df1.median_age.values)]
median_income = [int(i) for i in list(df2.median_income.values)]
population = [int(i) for i in list(df3.population.values)]

for i in range(len(state_codes)):
    #dic ={'_id':state_codes[i], 'median_age':median_age[i],'median_income':median_income[i], 'population':population[i] }
    query = {"_id":state_codes[i]}
    new_values = {"$set": {"median_age":median_age[i], "median_income":median_income[i], "population":population[i]} }
    census_data.update_one(query, new_values)