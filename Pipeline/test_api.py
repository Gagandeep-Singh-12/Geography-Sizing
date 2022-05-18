import pandas as pd
l=[]
df = pd.read_csv("/home/celebal/Data/genome_prod_20220113-companies.csv")
import requests
#ids = [14, 35, 161, 163, 261, 285, 289, 320, 376, 509, 526, 538, 559, 542]
ids = [ 35, 708, 685,672, 14, 161]
for i in range(708):
    company = df["CompanyName"].iloc[i]
    website = df["Website"].iloc[i]
    ID = int(df["CompanyId"].iloc[i])
    if ID in ids:

        response = requests.get('http://20.231.206.6:8080/api',

                                json={

                                        "id":ID,

                                        "company_name":company,

                                        "company_website":website

                                        }

                                )

        #result = json.loads(response.text)

        #print(result) 
        print(response.text) 
        print(ID)
        print('\n\n')