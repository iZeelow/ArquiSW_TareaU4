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

player = ObjectType("Player")

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)


@query.field("getPlayer")
def resolve_get_player(obj, resolve_info: GraphQLResolveInfo, id):
    response = requests.get(f"http://tarea_u4_service_users/users/{id}")

    if response.status_code == 200:
        return response.json()


@query.field("listPlayers")
def resolve_list_players(obj, resolve_info: GraphQLResolveInfo, team_id=None):
    # Make it slow
    time.sleep(3)

    response = requests.get(f"http://tarea_u4_service_users/users")

    if response.status_code == 200:
        return response.json()


@mutation.field("createUser")
def resolve_create_user(
    obj,
    resolve_info: GraphQLResolveInfo,
    id,
    name,
    username,
    password,
    email,
    admin,
    phone_number,
):
    payload = dict(
        id=id,
        name=name,
        username=username,
        password=password,
        email=email,
        admin=admin,
        phone_number=phone_number,
    )

    return requests.post(f"http://tarea_u4_service_users/users", json=payload).json()


schema = make_executable_schema(type_defs, query, mutation, player)
app = CORSMiddleware(
    GraphQL(schema, debug=True),
    allow_origins=["*"],
    allow_methods=("GET", "POST", "OPTIONS"),
)
