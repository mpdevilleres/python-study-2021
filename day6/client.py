# pip install requests

import requests

base_url_0 = '/fruits'
base_url_1 = '/fruit'

# GET - Retrieve
response = requests.get('veggies')

# POST - Create
response = requests.post('veggies', json={})

# PUT - Update
response = requests.put('veggies', json={})

# DELETE - Delete
response = requests.delete('veggies')
