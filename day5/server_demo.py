from typing import Optional
import uuid
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Python Workshop 2021')


class CarSchema(BaseModel):
    id: Optional[uuid.UUID]
    brand: Optional[str]
    color: Optional[str]
    type: Optional[str]
    model: Optional[str]
    year: Optional[str]


class CarListSchema(BaseModel):
    data: list[CarSchema]
    total: int


app.cars = [
    {'id': uuid.uuid4(), 'brand': 'toyota', 'color': 'red', 'type': 'sedan', 'model': 'corolla', 'year': '2019'},
    {'id': uuid.uuid4(), 'brand': 'kia', 'color': 'white', 'type': 'suv', 'model': 'sportage', 'year': '2020'},
]

default_tags = ['Cars API']


def get_car_by_id(car_id):
    for car in app.cars:
        if car['id'] == car_id:
            return car
    return None


@app.get("/cars", tags=default_tags, response_model=CarListSchema)
async def retrieve_cars():
    return {'data': app.cars, 'total': len(app.cars)}


@app.get("/cars/{car_id}", tags=default_tags, response_model=CarSchema)
async def retrieve_car(car_id: uuid.UUID):
    car = get_car_by_id(car_id)
    return car


@app.post("/cars", tags=default_tags, response_model=CarSchema)
async def create_car(car_data: CarSchema):
    car = {'id': uuid.uuid4(), **car_data.dict(exclude_unset=True)}
    app.cars.append(car)
    return car


@app.put("/cars/{car_id}", tags=default_tags, response_model=CarSchema)
async def update_car(car_id: uuid.UUID, car_data: CarSchema):
    car = get_car_by_id(car_id)
    app.cars = [car for car in app.cars if car['id'] != car_id]

    if not car:
        return None

    for k, v in car_data.dict(exclude_unset=True).items():
        car[k] = v

    app.cars.append(car)
    return car


@app.delete("/cars/{car_id}", tags=default_tags)
async def delete_car(car_id: uuid.UUID):
    app.cars = [car for car in app.cars if car['id'] != car_id]
    return ''


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)  # noqa
