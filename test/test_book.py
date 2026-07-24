import pytest
from fastapi.testclient import TestClient

BOOKS_PREFIX = "/api/v1/books"
AUTH_PREFIX = "/api/v1/auth"

sample_book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "publisher": "Test Publisher",
    "published_date": "2023-01-01",
    "page_count": 100,
    "language": "en",
}

test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpass123",
}


@pytest.fixture(scope="module")
def auth_headers(client: TestClient):
    client.post(f"{AUTH_PREFIX}/signup", json=test_user)
    response = client.post(
        f"{AUTH_PREFIX}/login",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_book(client, auth_headers):
    response = client.post(f"{BOOKS_PREFIX}/", json=sample_book_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_book_data["title"]
    assert data["author"] == sample_book_data["author"]


def test_get_all_books(client, auth_headers):
    response = client.get(f"{BOOKS_PREFIX}/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_book(client, auth_headers):
    response = client.post(f"{BOOKS_PREFIX}/", json=sample_book_data, headers=auth_headers)
    assert response.status_code == 201
    book_uid = response.json()["uid"]

    updated_data = {**sample_book_data, "title": "Updated Test Book"}
    response = client.patch(f"{BOOKS_PREFIX}/{book_uid}", json=updated_data, headers=auth_headers)
    assert response.status_code in (200, 202)
    assert response.json()["title"] == "Updated Test Book"


def test_update_book_not_found(client, auth_headers):
    response = client.patch(
        f"{BOOKS_PREFIX}/00000000-0000-0000-0000-000000000000",
        json=sample_book_data,
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_delete_book(client, auth_headers):
    response = client.post(f"{BOOKS_PREFIX}/", json=sample_book_data, headers=auth_headers)
    assert response.status_code == 201
    book_uid = response.json()["uid"]

    response = client.delete(f"{BOOKS_PREFIX}/{book_uid}", headers=auth_headers)
    assert response.status_code == 200


def test_delete_book_not_found(client, auth_headers):
    response = client.delete(
        f"{BOOKS_PREFIX}/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404
