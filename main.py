from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdateRequest
from uuid import UUID

app = FastAPI()

db: List[User] = [
  User(
    id=UUID('ad229b74-7d53-4cb8-a717-ca2aefa1a30c'),
    first_name='Jamila',
    last_name='Aaaa',
    gender=Gender.female,
    roles=[Role.student]
  ),
  User(
    id=UUID('ed4400b2-f22d-4a6e-b8d0-6d4e8086cdb5'),
    first_name='Alex',
    last_name='BB',
    gender=Gender.male,
    roles=[Role.admin, Role.user]
  )
]

@app.get('/')
def root():
  return {'hello': 'world'}

@app.get('/limit')
def limit(skip: int=0, limit: int=1):
  return db[skip: skip + limit]

@app.get('/api/v1/users')
async def fetch_users():
  return db

@app.post('/api/v1/users')
async def register_user(user: User):
  db.append(user)
  return {"id": user.id}

@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: UUID):
  #filter_data = list(filter(lambda x: x.id != user_id, db))
  #filter_data = [item for item in db if item.id != user_id]
  #return {"id": user_id} if len(filter_data) != len(db) else {"no encontrado"}
  for user in db:
    if user.id == user_id:
      db.remove(user)
      return
  raise HTTPException(
    status_code=404,
    detail=f'user with id "{user_id} does not exists'
  )

@app.put('/api/v1/users/{user_id}')
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
  for user in db:
    if user.id == user_id:
      if user_update.first_name is not None:
        user.first_name = user_update.first_name
      if user_update.last_name is not None:
        user.last_name = user_update.last_name
      if user_update.middle_name is not None:
        user.middle_name = user_update.middle_name
      if user_update.roles is not None:
        user.roles = user_update.roles
      return
  raise HTTPException(
    status_code=404,
    detail=f'user whith id: {user_id} does not exists'
  )