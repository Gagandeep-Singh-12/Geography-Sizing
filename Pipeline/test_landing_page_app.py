import requests
url1 = 'http://20.231.206.6:3030/landing_page'
url2 = 'http://127.0.0.1:3030/landing_page'
url3 = 'http://10.0.0.4:3030/landing_page'
response = requests.get(url1)
print(response.text)