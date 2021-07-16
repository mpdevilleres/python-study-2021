from datetime import (
    datetime,
    date
)
import json
import uuid
from typing import List, Optional

import requests
import fastapi, logging
import uvicorn
import pydantic
import psycopg2

logger = logging.getLogger()


class CovidCase(pydantic.BaseModel):
    id: uuid.UUID
    date_observed: datetime
    province: str
    region: str
    date_updated: date
    confirmed_count: float
    death_count: float
    recovered_count: float


class CovidCaseInput(pydantic.BaseModel):
    date_observed: datetime
    province: str
    region: str
    date_updated: date
    confirmed_count: float
    death_count: float
    recovered_count: float


class CovidCasePut(pydantic.BaseModel):
    date_observed: Optional[datetime]
    province: Optional[str]
    region: Optional[str]
    date_updated: Optional[date]
    confirmed_count: Optional[float]
    death_count: Optional[float]
    recovered_count: Optional[float]


app = fastapi.FastAPI(title='Covid Cases')

base_sw_url = 'https://swapi.dev/api'


def db_execute_and_fetch(sql):
    conn = psycopg2.connect(
        host="localhost",
        database="internal",
        user="postgres",
        password="postgres")
    cur = conn.cursor()
    cur.execute(sql)
    try:
        return cur.fetchall()
    except psycopg2.ProgrammingError:
        return None


def db_insert_update(sql):
    conn = psycopg2.connect(
        host="localhost",
        database="internal",
        user="postgres",
        password="postgres")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.fetchall()


def db_delete(sql):
    conn = psycopg2.connect(
        host="localhost",
        database="internal",
        user="postgres",
        password="postgres")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


@app.get('/covid-cases', response_model=List[CovidCase])
def retrieve_covid_cases():
    results = db_execute_and_fetch("""
        SELECT id, date_observed, province, region, date_updated, 
               confirmed_count, death_count, recovered_count 
        FROM covid_case;
    """)

    transformed = []
    for result in results:
        transformed.append(
            CovidCase(
                id=result[0],
                date_observed=result[1],
                province=result[2],
                region=result[3],
                date_updated=result[4],
                confirmed_count=result[5],
                death_count=result[6],
                recovered_count=result[7],
            )
        )

    return transformed


@app.get('/covid-cases/total-recovered', response_model=int)
def retrieve_covid_recovered_cases():
    results = db_execute_and_fetch("SELECT SUM(recovered_count) FROM covid_case;")
    return results[0][0]


@app.post('/covid-cases', response_model=CovidCase)
def create_covid_case(data: CovidCaseInput):
    results = db_insert_update(f"""
    INSERT INTO covid_case(
                       date_observed,
                       province,
                       region,
                       date_updated,
                       confirmed_count,
                       death_count,
                       recovered_count
                       )
    VALUES ('{data.date_observed}', '{data.province}', '{data.region}', '{data.date_updated}',
     {data.confirmed_count}, {data.death_count}, {data.recovered_count})
    RETURNING id, date_observed, province, region, date_updated, 
              confirmed_count, death_count, recovered_count;
    """)
    return results


@app.get('/covid-cases/{id}', response_model=CovidCase)
def retrieve_covid_case(id):
    results = db_execute_and_fetch(f"""
    SELECT id, date_observed, province, region, date_updated, 
               confirmed_count, death_count, recovered_count
    FROM covid_case WHERE id = '{id}'
    """)

    result = results[0]
    transformed = CovidCase(
        id=result[0],
        date_observed=result[1],
        province=result[2],
        region=result[3],
        date_updated=result[4],
        confirmed_count=result[5],
        death_count=result[6],
        recovered_count=result[7]
    )
    return transformed


@app.delete('/covid-cases/{id}')
def delete_covid_case(id):
    db_delete(f"""DELETE FROM covid_case WHERE id ='{id}'""")
    return


@app.put('/covid-cases/{id}', response_model=CovidCase)
def update_covid_case(id, data: CovidCasePut):
    update_parameters = data.dict(exclude_unset=True)
    update_parameters_string = []
    for key, value in update_parameters.items():
        if isinstance(value, int) or isinstance(value, float):
            value = value
        else:
            value = f"'{value}'"
        update_parameters_string.append(f"{key} = {value}")

    columns_data = ', '.join(update_parameters_string)
    results = db_insert_update(f"""
        UPDATE covid_case SET {columns_data} WHERE id = '{id}'
        RETURNING id, date_observed, province, region, date_updated, confirmed_count, death_count, recovered_count;
    """)

    result = results[0]
    transformed = CovidCase(
        id=result[0],
        date_observed=result[1],
        province=result[2],
        region=result[3],
        date_updated=result[4],
        confirmed_count=result[5],
        death_count=result[6],
        recovered_count=result[7]
    )
    return transformed


@app.get('/contacts/{id}')
def retrieve_contact(id):
    results = db_execute_and_fetch(f"""
        SELECT id, data FROM star_wars_people WHERE id = {id}
    """)

    if not results:
        response = requests.get(f'{base_sw_url}/people/{id}/')
        payload = response.json()
        results = db_insert_update(f"""
        INSERT INTO star_wars_people(id, data) VALUES ({id}, '{json.dumps(payload)}')
        RETURNING id, data
        """)
    result = results[0]
    return result[1]


@app.get('/contacts')
def retrieve_contact():
    counter = 0
    response = requests.get(f'{base_sw_url}/people/')
    payload = response.json()
    results = payload['results']
    counter += 1
    print(f'{counter} request to people {base_sw_url}/people/')
    while payload['next']:
        print(f'{counter} request to people {payload["next"]}')
        response = requests.get(payload['next'])
        payload = response.json()
        results.append(payload['results'])
        counter += 1

    return results


@app.get('/udp-echo')
def retrieve_echo():
    import socket
    conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    conn.sendto('2'.encode(), ('0.0.0.0', 31337))

    return


uvicorn.run(app, host='0.0.0.0', port=9002)
