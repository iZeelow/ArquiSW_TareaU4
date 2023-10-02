import logging

from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import FastAPI, status, HTTPException
from fastapi import HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import Optional
from bson.objectid import ObjectId
from bson.errors import InvalidId
from app.schemas import userEntity, usersEntity
from passlib.hash import sha256_crypt
from app.events import Emit

app = FastAPI(title="APIREST FastAPI & MongoDB", version="0.3.1")

mongodb_client = MongoClient("tarea_U4_service_users_mongodb", 27017)


class User(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str = Field(examples=["Juan"])
    username: str = Field(examples=["juan1010"])
    password: str = Field(examples=["password123"])
    email: Optional[str] = Field(default=None, examples=["juan@gmail.com"])
    admin: Optional[bool] = Field(default=None, examples=["True"])
    phone_number: Optional[int] = Field(default=None, examples=["123456789"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Juan",
                    "username": "juan123",
                    "password": "asdsad123",
                    "email": "email@email.com",
                    "admin": "True",
                    "phone_number": "1234567890",
                }
            ]
        }
    }


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)

emit_events = Emit()


@app.get(
    "/users",
    tags=["User"],
    response_model=list[User],
    summary="Get all Users",
    response_description="A list of all Users",
    status_code=status.HTTP_200_OK,
)
def get_all_users():
    return usersEntity(mongodb_client.service_users.users.find({}))


@app.get(
    "/users/{id}",
    tags=["User"],
    response_model=User,
    summary="Get an User",
    response_description="The User found",
)
def get_user(id: str):
    try:
        user=mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        logging.info("Query user")
        return user
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")


@app.post(
    "/users",
    tags=["User"],
    response_model=User,
    summary="Create an User",
    response_description="The created User",
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: User):
    """
    Create an User with all the information:
    - **id**: optional parameter, the db generates it
    - **name**: the User's name
    - **password**: the User's password
    - **email**: optional parameter
    - **admin**: optional parameter, doesn't have an use for now
    - **phone_number***: optional parameter, the User's phone number
    """
    try:
        new_user = dict(user)
        new_user["password"] = sha256_crypt.encrypt(new_user["password"])
        del new_user["id"]
        id = mongodb_client.service_users.users.insert_one(new_user).inserted_id
        user = mongodb_client.service_users.users.find_one({"_id": id})
        logging.info("new user created")
        emit_events.send(id, "create", new_user)
        return userEntity(user)

    except ():
        raise HTTPException(status_code=404, detail="Something went wrong")


@app.put(
    "/users/{id}",
    tags=["User"],
    response_model=User,
    summary="Update an User",
    response_description="The updated User",
)
def update_user(id: str, user: User):
    try:
        mongodb_client.service_users.users.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(user)}
        )
        logging.info("User updated: %s" % id)
        emit_events.send(id, "update", user)
        return userEntity(
            mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        )
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{id}", tags=["User"], summary="Delete an User")
def delete_user(id: str):
    try:
        user = mongodb_client.service_users.users.find_one({"_id": ObjectId(id)})
        mongodb_client.service_users.users.delete_one(({"_id": ObjectId(id)}))
        logging.info("User deleted: %s" % id)
        emit_events.send(id, "delete", user)
        return
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail="User not found")
