import pandas as pd
import re
import pymongo
class Model():
    def __init__(self,cosmos_conn,db_name,census_coll):
        self.Census_coll= census_coll
        self.cosmos_conn= cosmos_conn
        self.db_name= db_name
        self.client = pymongo.MongoClient(self.cosmos_conn)
        self.mongo_data = self.client.get_database(name="geography_sizing").get_collection(name='census_US')

    def Country(self,sales,countries,Revenue):
        uni_countries = list(set(countries))
        Country_Dist={}
        total = 0
        for i in uni_countries:
            for j in range(len(countries)):
                if i == countries[j] and i!="NA":
                    sales_value = int(re.sub(",","",sales[j]))
                    total+=sales_value
                    if i not in Country_Dist.keys():
                        Country_Dist[i] = sales_value
                    else:
                        Country_Dist[i] += sales_value

        for i in Country_Dist.keys():
            Country_Dist[i] /= total
            Country_Dist[i] *= Revenue
        return Country_Dist


    def Census(self,State_List,rev):
        State={}
        tot=0

        uni_state=list(set(State_List))
        if len(uni_state) == 1:
            State[uni_state[0]] = rev
            return State
        for s in uni_state:
            rec = self.mongo_data.find_one({"_id":s.upper()})

            income = rec["median_age"]
            Age = rec["median_income"]
            pop = rec["population"]
            Value = income*.25 + Age*0.1 + pop*0.1/(income+Age+pop)
            State[s] = Value
            tot+=Value
        for k in State.keys():
            State[k]/=tot
            State[k]*=rev
        return State

    def State_level(self,Country_Dist,Combined,Website):
        State_Dist ={}
        for country in Country_Dist.keys():
            if country not in Combined.keys():
                continue
            if country == "us":
                State_Dist["us"] = self.Census(Combined["us"],Country_Dist["us"])
            else:
                State={}
                val = 0            
                for City in list(set(Combined[country])):
                    flag = -1
                    City = City.lower()
                    for loc in Website["web_data"]:
                        loc = loc.lower()
                        if City in loc or City==loc:
                            State[City] = 2
                            val+=2
                            flag = 0
                            break
        
                    if flag == -1:
                        State[City]=1
                        val+=1

                for k in State.keys():
                    State[k]/=val
                    State[k]*=Country_Dist[country]
                State_Dist[country] = State
        return State_Dist

    def Distribute(self,Sales,Linkedin,Glassdoor,Website,Revenue):
        Combined={}
        Linkedin_countries = list(Linkedin.keys())
        Glassdoor_countries = list(Glassdoor.keys())
        Country_Dist=self.Country(Sales["sales_count"],Sales["country"],Revenue)
        #return Country_Dist

        for i in list(set(Linkedin_countries+Glassdoor_countries)):
            if i in Linkedin_countries and i in Glassdoor_countries:
                Combined[i] = Linkedin[i]+Glassdoor[i]
            elif i in Linkedin_countries:
                Combined[i] = Linkedin[i]
            elif i in Glassdoor_countries:
                Combined[i] = Glassdoor[i]
        
        State_Dist = self.State_level(Country_Dist, Combined, Website)

        return Country_Dist, State_Dist
