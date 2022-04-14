import requests
import pandas as pd
df = pd.read_csv("/home/celebal/Data/companies_data.csv")
for i in range(10):
        company = df.iloc[i, 3]
        website = df.iloc[i, 0]
        response = requests.get('http://20.231.206.6:8080/api',

                                json={

                                        "id":123,

                                        "company_name":company,

                                        "company_website":website

                                        }

                                )

        #result = json.loads(response.text)

        #print(result) 
        print(response.text) 