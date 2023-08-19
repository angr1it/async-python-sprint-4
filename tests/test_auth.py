from tests.conftest import client
from main import app


def test_register():
    response = client.post(
        url=app.url_path_for('register:register'),
        json={
            "username": "user",
            "email": "user@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert response.status_code == 201


def test_login():
    response = client.post(
        url=app.url_path_for('auth:jwt.login'),
        data="grant_type=&username=user@example.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 204
    login_cookie = response.cookies

    response = client.post(
        url=app.url_path_for('auth:jwt.logout'),
        cookies=login_cookie
    )

    assert response.status_code == 204
