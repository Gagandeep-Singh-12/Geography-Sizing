import requests
url = 'http://127.0.0.1:5000/api '
response = requests.post(url,json={'Comapny_name':'23andMe Holding Co.' , 'Company_URL':'https://www.23andme.com/'})
print(response)