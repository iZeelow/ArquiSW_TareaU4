import requests
from fastapi.testclient import TestClient
from .main import app
client = TestClient(app)

endpoint = "http://localhost:5000"

def test_create_and_delete_user():
    #crear usuario
    payload = {"name": "Juan1233232323123123",
                "username": "juan123",
                "password": "asdsad123"}
    response = requests.post(endpoint + "/users",json=payload)
    assert response.status_code == 201
    user_id = str(response.json()["id"])
    #borrar usuario
    delete_response = requests.delete(endpoint + f"/users/{user_id}")
    assert delete_response.status_code == 200

def test_update_user():
    #crear usuario
    payload = {"name": "Juan1233232323123123",
                "username": "juan123",
                "password": "asdsad123"}
    response = requests.post(endpoint + "/users",json=payload)
    payload = {"name": "Update"}
    user_id = str(response.json()["id"])
    payload_update = {"name":"Update"}
    response_update = requests.patch(endpoint + f"/users/{user_id}",json=payload_update)
    assert response_update.status_code == 200
    #borrar usuario
    delete_response = requests.delete(endpoint + f"/users/{user_id}")
    assert delete_response.status_code == 200


