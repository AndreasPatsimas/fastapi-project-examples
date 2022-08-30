from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_all_users():
    response = client.get("/users")
    print(response.content)
    assert response.status_code == 200


def test_login_for_access_token():
    response = client.post("/auth/token", data={"username": "apatsimas", "password": "aris1914"})
    print(response.content)
    assert response.status_code == 200


def test_read_todos_by_user():
    auth = client.post("/auth/token", data={"username": "apatsimas", "password": "aris1914"})
    token = auth.json().get("token")

    response = client.get("/todos/user", headers={"Authorization": f"Bearer {token}"})
    print(response.content)
    assert response.status_code == 200


def test_create_todo():
    auth = client.post("/auth/token", data={"username": "apatsimas", "password": "aris1914"})
    token = auth.json().get("token")

    response = client.post("/todos/",
                           json={
                                  "title": "ComeBack",
                                  "description": "vlue for money",
                                  "priority": 1,
                                  "complete": False
                                },
                           headers={"Authorization": f"Bearer {token}"})
    print(response.content)
    assert response.status_code == 200
