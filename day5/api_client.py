from pprint import pprint
import requests

# HTTP GET REQUEST
# response = requests.get('http://localhost:9001/cars')
# pprint(response.status_code)
# pprint(response.json())

# response = requests.get('http://localhost:9001/cars/f3ab5c9e-0574-4f33-8cca-103ec0ce4c23')
# pprint(response.status_code)
# pprint(response.json())
#

# response = requests.post('http://localhost:9001/cars', json={
#     "brand": "hyundai",
#     "color": "black",
#     "type": "sedan",
#     "model": "elantra",
#     "year": "2021"
# })
# pprint(response.status_code)
# pprint(response.json())

# response = requests.get('http://localhost:9001/cars')
# pprint(response.status_code)
# pprint(response.json())

# response = requests.put('http://localhost:9001/cars/1638c7eb-daa7-4b65-a82d-b72cf6deccd4', json={
#     'model': 'sonata',
#     'year': '2018'
# })
# pprint(response.status_code)
# pprint(response.json())

# response = requests.get('http://localhost:9001/cars')
# pprint(response.status_code)
# pprint(response.json())

# response = requests.delete('http://localhost:9001/cars/79e5b434-952a-4e38-87d9-8d2573535068')
# pprint(response.status_code)
# pprint(response.json())

response = requests.get('http://localhost:9001/cars')
pprint(response.status_code)
pprint(response.json())
