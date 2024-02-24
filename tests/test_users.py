from app import schemas
import pytest
from jose import jwt
from app.config import settings



@pytest.fixture
def test_user(client):
    user_data = {"email": "mike@test.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Welcome to my API! Docker & Ubuntu practice!"}

def test_create_user(client):
    response = client.post("/users/", json={"email": "meg@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**response.json())# unpack the response into a new user object
    assert new_user.email == "meg@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    
    login_response = schemas.Token(**response.json())#Used for token validation. Matches auth.py router
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])#decode the jwt token
    id = payload.get("user_id")#get the user id from the payload
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("meg@gmail.com", "wrongpassword", 403),
    ("wrongemaiL@gmail.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("meg@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password, })
    assert response.status_code == status_code
    #assert response.json().get("detail") == "Invalid credentials"  # Invalid credentials syntax MUST match auth.py router. This is removed bc invalid credentials wont match 422 error code
