# pip install fastapi
# pip install uvicorn
from typing import List

import fastapi
import uvicorn
import pydantic

app = fastapi.FastAPI()

app.fruits = [
    {'name': 'apple', 'color': 'red', 'taste': 'sweet'},
    {'name': 'banana', 'color': 'yellow', 'taste': 'sweet'},
    {'name': 'tomato', 'color': 'red', 'taste': 'sweet'}
]


class Fruit(pydantic.BaseModel):
    name: str
    color: str
    taste: str


# GET SINGLE
@app.get('/fruits/{name}', response_model=Fruit)
def retrieve_fruit(name):
    for fruit in app.fruits:
        if fruit['name'] == name:
            return fruit

    return None


# GET ALL
@app.get('/fruits', response_model=List[Fruit])
def retrieve_fruits():
    return app.fruits


# POST
@app.post('/fruits', response_model=Fruit)
def create_fruit(data: Fruit):
    app.fruits.append(data.dict())
    return data


# PUT
@app.put('/fruits/{name}', response_model=Fruit)
def update_fruit(data: Fruit, name):
    new_fruits = []
    for fruit in app.fruits:
        if fruit['name'] != name:
            new_fruits.append(fruit)

    new_fruits.append(data.dict())
    app.fruits = new_fruits

    return data


# DELETE
@app.delete('/fruits/{name}')
def delete_fruit(name):
    new_fruits = []
    for fruit in app.fruits:
        if fruit['name'] != name:
            new_fruits.append(fruit)
    app.fruits = new_fruits
    return None


uvicorn.run(app, host='0.0.0.0', port=9001)
