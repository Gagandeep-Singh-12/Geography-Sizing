
import requests
for i in range(50):
    response = requests.get('http://20.231.206.6:8080/api',

                            json={

                                    "id":123,

                                    "company_name":"Abbott Laboratories",

                                    "company_website":"https://www.abbott.com"

                                    }

                            )

    #result = json.loads(response.text)

    #print(result) 
    print(response.text) 