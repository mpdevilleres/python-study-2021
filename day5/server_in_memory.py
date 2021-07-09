import uuid
from typing import List, Optional

import uvicorn
import fastapi
import pydantic

# Python Class
# Participants
app = fastapi.FastAPI(
    title='Python Class',
    description="This is a service to provide participants information"
)
app.participants = [
    {
        'id': uuid.uuid4(),
        'iecep_id': '098764',
        'name': 'Marc',
        'country': 'UAE',
        'date_deleted': '2021-07-07'
    },
    {
        'id': uuid.uuid4(),
        'iecep_id': '123456',
        'name': 'Leif',
        'country': 'UAE',
        'date_deleted': None
    },
    {
        'id': uuid.uuid4(),
        'iecep_id': '56788',
        'name': 'Renan',
        'country': 'UAE',
        'date_deleted': None
    },
]


class ParticipantSchema(pydantic.BaseModel):
    id: Optional[uuid.UUID]
    iecep_id: Optional[str]
    name: Optional[str]
    country: Optional[str]
    date_deleted: Optional[str]


class ParticipantListSchema(pydantic.BaseModel):
    data: List[ParticipantSchema]
    total: int


@app.get('/participants/deleted', response_model=ParticipantListSchema)
def retrieve_participants():
    filtered_participants = []

    for participant in app.participants:
        if not participant['date_deleted']:
            continue

        filtered_participants.append(participant)

    return {'data': filtered_participants, 'total': len(filtered_participants)}


@app.get('/participants', response_model=ParticipantListSchema)
def retrieve_participants():
    filtered_participants = []

    for participant in app.participants:
        if participant['date_deleted']:
            continue

        filtered_participants.append(participant)

    return {'data': filtered_participants, 'total': len(filtered_participants)}


@app.get('/participants/{participant_id}')
def retrieve_participant(participant_id: uuid.UUID):
    for participant in app.participants:
        if participant['id'] == participant_id:
            return participant

    return None


@app.post('/participants', response_model=ParticipantSchema)
def create_participant(data: ParticipantSchema):
    data.id = uuid.uuid4()
    participant = data.dict()
    app.participants.append(participant)
    return participant


@app.put('/participants/{participant_id}', response_model=ParticipantSchema)
def update_participant(
        participant_id: uuid.UUID, data: ParticipantSchema
):
    participant_to_update = None

    # get participant to be updated
    for participant in app.participants:
        if participant['id'] == participant_id:
            participant_to_update = participant
            break

    if participant_to_update:
        for key, value in data.dict(exclude_unset=True).items():
            participant_to_update[key] = value

        # filter by participant_id
        # new_participants = [p for p in app.participants if p['id'] != participant_id]
        new_participants = []
        for participant in app.participants:
            if participant['id'] == participant_id:
                continue
            new_participants.append(participant)

        app.participants = new_participants
        app.participants.append(participant_to_update)
        return participant_to_update

    return None


@app.delete('/participants/{participant_id}')
def delete_participant(participant_id: uuid.UUID):
    new_participants = []
    for participant in app.participants:
        if participant['id'] == participant_id:
            participant['date_deleted'] = '2021-07-09'
        new_participants.append(participant)
    app.participants = new_participants

    return None


uvicorn.run(app, host="localhost", port=9002)  # noqa
