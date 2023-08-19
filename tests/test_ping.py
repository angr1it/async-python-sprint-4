from tests.conftest import client
from main import app


def test_ping_anonymus():
    response = client.get(
        url=app.url_path_for('get_ping'),
    )

    assert response.content == b'{"status":"OK","data":{"db_on":true,"user":null},"description":null}'


def test_ping_logged():
    response = client.post(
        url=app.url_path_for('register:register'),
        json={
            "username": "ping",
            "email": "ping@test.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )

    assert response.status_code == 201

    response = client.post(
        url=app.url_path_for('auth:jwt.login'),
        data="grant_type=&username=ping@test.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 204
    login_cookie = response.cookies

    response = client.get(
        url=app.url_path_for('get_ping'),
        cookies=login_cookie
    )

    assert response.content == b'{"status":"OK","data":{"db_on":true,"user":"ping@test.com"},"description":null}'

    response = client.post(
        url=app.url_path_for('auth:jwt.logout'),
        cookies=login_cookie
    )

    assert response.status_code == 204
