import logging

from pymongo import MongoClient
from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()
mongodb_client = MongoClient("tarea_U4_service_users_mongodb", 27017)

logging.basicConfig( level = logging.INFO, 
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

class User(BaseModel):
    id: str | None = None
    name: str
    username: str
    password: str
    
    def __init__(self, **kargs):
        if "_id" in kargs:
            kargs["id"] = str(kargs["id"])
        BaseModel.__init__(self, **kargs)

@app.get("/")
async def root():
    logging.info("Hello World (end=point)")
    return {"Hello": "World"}

@app.get("/users", response_model=list[User])
def users_all():
    filters = {}
    return [User(**user) for user in mongodb_client.service_users.users.find(filters)]

@app.get("/users/{user_id}")
def users_get(user_id: str):
    try:
        user_id = ObjectId(user_id)
        return User(
            **mongodb_client.service_users.users.find_one({"_id": user_id})
        )
    except (InvalidId, TypeError):
        raise HTTPException(status_code = 404, detail = "User not found")
    
@app.get("users/{user_id}")
def users_update(user_id: str, user: dict):
    try:
        user_id: ObjectId(user_id)
        mongodb_client.service_users.update_one(
            {"__id": user_id}, {"$set", user}
        )
        return User(
            **mongodb_client.users.users.find_one({"_id": user_id})
        )
    except (InvalidId, TypeError):
        raise HTTPException(status_code = 405, detail= "Can't create user")
    
@app.delete("/users/{user_id}")
def users_delete(user_id: str):
    try:
        user_id = ObjectId(user_id)
        user = User(
            **mongodb_client.users.users.find_one({"_id"})
        )
    except (InvalidId, TypeError):
        raise HTTPException(status_code = 404, detail = "User not found")
    
    mongodb_client.users.users.delete_one(
        {"_id": ObjectId(user_id)}
    )
    
    return user

@app.post("/users")
def users_create(user: User):
    inserted_id = mongodb_client.service_users.users.insert_one(
        user.dict()
    ).inserted_id

    new_user = User(
        **mongodb_client.service_users.users.find_one(
            {"_id": ObjectId(inserted_id)}
        )
    )

    #emit_events.send(inserted_id, "create", new_player.dict())

    logging.info(f"New player created: {new_user}")

    return new_user