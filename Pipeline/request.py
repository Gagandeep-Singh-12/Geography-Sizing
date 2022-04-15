import requests
import pandas as pd
df = pd.read_csv("/home/celebal/Data/companies_data.csv")
d = {'id': 123, 'company_name': '1mage Software, Inc.', 'company_website': 'https://1mage.com/'}
'''
d1 = {

                                        "id":123,

                                        "company_name":company,

                                        "company_website":website

                                        }
'''
for i in range(1):
        company = df.iloc[i, 3]
        website = df.iloc[i, 0]
        print(company, '        ', website)
        response = requests.get('http://20.231.206.6:8080/api',

                                json=d

                                )
        print(response.text) 
        print('--------------------------------------------------')