import context
import config
import pandas as pd
import requests
import json
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1920, 1080))  
display.start()

df = pd.read_csv("/home/celebal/Data/genome_prod_20220113-companies.csv")
ids = [ 35, 708, 685,672, 14, 161]
for i in ids[:1]:
    company = df["CompanyName"].iloc[i]
    website = df["Website"].iloc[i]
    ID = int(df["CompanyId"].iloc[i])


    response = requests.post('http://20.25.81.60:3030/geography_revenue',timeout=180,

                    json={

                            "id":ID,

                            "company_name":company,

                            "company_website":website

                            }

                    )
    
    #print(type(result["revenue"]))
    print(response.text)
    if response.status_code == 200:
        result = json.loads(response.text)
        rev=result["revenue"]
        
        obj = context.context(ID,company,website,rev)
        obj.Distribute()
        print(obj.Data)
        print("")
    else:




display.stop()