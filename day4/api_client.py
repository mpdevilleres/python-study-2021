# CREATE a python client the will scrap/get data from swapi to retrieve species data
# and store in a csv file

import csv
import requests

BASE_URL = 'https://swapi.dev/api/'

people = []

print(f'{BASE_URL}people/')
response = requests.get(f'{BASE_URL}people/')
payload = response.json()
people.extend(payload['results'])
next_url = payload['next']
print(next_url)

while next_url:
    response = requests.get(next_url)
    payload = response.json()
    people.extend(payload['results'])
    next_url = payload['next']
    print(next_url)

print(f'count: {len(people)}')
print(people)

with open('people.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'created', 'mass', 'height', 'birth_year', 'eye_color', 'homeworld', 'gender', 'skin_color',
                     'hair_color', 'edited', 'name', 'film_titles'])
    for p in people[:4]:
        film_titles = []
        for film_url in p['films']:
            print(film_url)
            response = requests.get(film_url)
            payload = response.json()
            film_titles.append(payload['title'])

        data = [
            p['url'],
            p['created'],
            p['mass'],
            p['height'],
            p['birth_year'],
            p['eye_color'],
            p['homeworld'],
            p['gender'],
            p['skin_color'],
            p['hair_color'],
            p['edited'],
            p['name'],
            film_titles
        ]
        writer.writerow(data)
