import time
import logging
import requests

from ariadne import QueryType
from ariadne import MutationType
from ariadne import ObjectType
from ariadne import make_executable_schema
from ariadne import load_schema_from_path

from ariadne.asgi import GraphQL

from graphql.type import GraphQLResolveInfo

from starlette.middleware.cors import CORSMiddleware


type_defs = load_schema_from_path("./app/schema.graphql")

query = QueryType()
mutation = MutationType()

user= ObjectType("User")


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


@query.field("getUser")
def resolve_get_user(obj, resolve_info: GraphQLResolveInfo, id):
    response = requests.get(f"http://tarea_u4_service_users/users/{id}")

    if response.status_code == 200:
        return response.json()

@query.field("getAllUsers")
def resolve_get_all_users(obj, resolve_info: GraphQLResolveInfo):
    response = requests.get(f"http://tarea_u4_service_users/users")

    if response.status_code == 200:
        return response.json()

@mutation.field("createUser")
def resolve_create_user(obj, resolve_info: GraphQLResolveInfo, name, username, password):
    payload = dict(name=name,
                   username=username,
                   pasword=password)

    return requests.post(f"http://tarea_u4_service_users/users", json=payload).json()

@mutation.field("updateUser")
def resolve_update_user(obj, resolve_info: GraphQLResolveInfo, id, name=None,username=None , password=None):
    payload = {}
    if name is not None:
        payload["name"] = name
    if username is not None:
        payload["username"] = username
    if password is not None:
        payload["password"] = password

    return requests.put(f"http://tarea_u4_service_users/users/{id}", json=payload)

#@mutation.field("deleteUser")
#def resolve_delete_user(obj, resolve_info: GraphQLResolveInfo,id):
 #   user_data=mongodb_client.users.users.find_one({""})

  #  return requests.post(f"http://tarea_u4_service_users/users", json=payload).json()

schema = make_executable_schema(type_defs, query, mutation, user)
app = CORSMiddleware(GraphQL(schema, debug=True), allow_origins=['*'], allow_methods=("GET", "POST", "OPTIONS"))