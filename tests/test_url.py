import json

from tests.conftest import client


def test_anonymus_create():
    post_data = {"url": "https://example.com/", "private": True}
    response = client.post("api/url", json=post_data)

    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert response_data["private"] is False
    assert response_data["original_url"] == post_data["url"]


def test_anonymus_get():
    response = client.get("api/url/1")

    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert response_data["private"] is False
    assert response_data["original_url"] == "https://example.com/"


def test_logged_in_create():
    response = client.post(
        "auth/jwt/login",
        data="grant_type=&username=user@example.com&password=string&scope=&client_id=&client_secret=",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 204

    post_data_private = {"url": "https://example1.com/", "private": True}
    response = client.post("api/url", json=post_data_private)

    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert response_data["private"] is True
    assert response_data["original_url"] == post_data_private["url"]

    post_data_public = {"url": "https://example1.com/", "private": False}
    response = client.post("api/url", json=post_data_public)

    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert response_data["private"] is False
    assert response_data["original_url"] == post_data_public["url"]


def test_logged_in_batch_load():
    batch_json = {"ids": [1, 2, 3]}
    response = client.post("api/url/items/", json=batch_json)
    response_data = json.loads(response.content)
    assert len(response_data) == 3


def test_logged_in_get_user():
    response = client.get("api/url/user/user")

    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert len(response_data) == 2


def test_logged_out_get_user():
    response = client.post(
        "auth/jwt/logout"
    )

    assert response.status_code == 204

    response = client.get("api/url/user/user")

    response_data = json.loads(response.content)

    assert response.status_code == 200
    assert len(response_data) == 1
