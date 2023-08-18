
from tests.conftest import client


def test_ping_anonymus():
    response = client.get(
        "api/ping",
    )

    assert response.content == b'{"status":"OK","data":{"db_on":true,"user":null},"description":null}'


def test_ping_logged():
    response = client.post(
        "auth/register",
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
        "auth/jwt/login",
        data="grant_type=&username=ping@test.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 204
    login_cookie = response.cookies

    response = client.get(
        "api/ping",
        cookies=login_cookie
    )

    assert response.content == b'{"status":"OK","data":{"db_on":true,"user":"ping@test.com"},"description":null}'

    response = client.post(
        "auth/jwt/logout",
        cookies=login_cookie
    )

    assert response.status_code == 204
