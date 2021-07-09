import csv
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


def read_participant_file():
    with open('participants_list.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def append_participant_file(data: dict):
    with open('participants_list.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)


def write_participant_file(data: List[dict]):
    with open('participants_list.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


class ParticipantSchema(pydantic.BaseModel):
    id: Optional[uuid.UUID]
    iecep_id: Optional[str]
    name: Optional[str]
    country: Optional[str]
    date_deleted: Optional[str]


class ParticipantListSchema(pydantic.BaseModel):
    data: List[ParticipantSchema]
    total: int


class ParticipantIDListSchema(pydantic.BaseModel):
    participant_ids: List[uuid.UUID]


@app.get('/participants', response_model=ParticipantListSchema)
def retrieve_participants():
    participants = read_participant_file()

    return {'data': participants, 'total': len(participants)}


@app.get('/participants/{participant_id}')
def retrieve_participant(participant_id: uuid.UUID):
    participants = read_participant_file()
    for participant in participants:
        if participant['id'] == str(participant_id):
            return participant

    return None


@app.post('/participants', response_model=ParticipantSchema)
def create_participant(data: ParticipantSchema):
    data.id = uuid.uuid4()
    data.date_deleted = None
    participant = data.dict()
    append_participant_file(participant)
    return participant


@app.put('/participants/{participant_id}', response_model=ParticipantSchema)
def update_participant(
        participant_id: uuid.UUID, data: ParticipantSchema
):
    participant_to_update = None

    participants = read_participant_file()
    # get participant to be updated
    for participant in participants:
        if participant['id'] == str(participant_id):
            participant_to_update = participant
            break

    if participant_to_update:
        for key, value in data.dict(exclude_unset=True).items():
            participant_to_update[key] = value

        # filter by participant_id
        # new_participants = [p for p in app.participants if p['id'] != participant_id]
        new_participants = []
        for participant in participants:
            if participant['id'] == str(participant_id):
                continue
            new_participants.append(participant)

        new_participants.append(participant_to_update)
        write_participant_file(new_participants)
        return participant_to_update

    return None


@app.delete('/participants/bulk')
def delete_participant(data: ParticipantIDListSchema):
    participants = read_participant_file()
    new_participants = []
    for participant in participants:
        if uuid.UUID(participant['id']) in data.participant_ids:
            continue
        new_participants.append(participant)
    write_participant_file(new_participants)

    return None


@app.delete('/participants')
def delete_all_participants():
    with open('participants_list.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(ParticipantSchema.__fields__.keys())


uvicorn.run(app, host="localhost", port=9002)  # noqa
