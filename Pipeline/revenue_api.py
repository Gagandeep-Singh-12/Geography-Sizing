import requests

#url = ''
#data = {'id': 123,
#        'company': }
url1 = 'http://52.146.41.91:2020/geography_revenue'
#url2 = 'http'
response = requests.get(url1,

                        json={

                                "id":123,

                                "company_name":"Abbott Laboratories",

                                "company_website":"https://www.abbott.com"

                                }

                        )

#result = json.loads(response.text)

print(response) 
print(response.text) 