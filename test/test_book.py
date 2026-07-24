

# Prefix for book routes
BOOKS_PREFIX = "/api/v1/books"

# Sample book data for testing
sample_book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "publisher": "Test Publisher",
    "published_date": "2023-01-01",
    "page_count": 100,
    "language": "en",
}

def test_create_book(client):
    """Test creating a new book."""
    response = client.post(BOOKS_PREFIX, json=sample_book_data)
    assert response.status_code == 201
    created_book = response.json()
    assert created_book["title"] == sample_book_data["title"]
    assert created_book["author"] == sample_book_data["author"]

def test_get_all_books(client):
    """Test retrieving all books."""
    response = client.get(BOOKS_PREFIX)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_book(client):
    """Test updating an existing book."""
    # First, create a book to update
    response = client.post(BOOKS_PREFIX, json=sample_book_data)
    assert response.status_code == 201
    book_uid = response.json()["uid"]

    # Now, update the book
    updated_data = {
        "title": "Updated Test Book",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "published_date": "2023-01-01",
        "page_count": 100,
        "language": "en"
    }
    response = client.patch(f"{BOOKS_PREFIX}/{book_uid}", json=updated_data)
    assert response.status_code == 202
    updated_book = response.json()
    assert updated_book["title"] == updated_data["title"]

def test_update_book_not_found(client):
    """Test updating a non-existent book."""
    response = client.patch(f"{BOOKS_PREFIX}/non-existent-uid", json={
        "title": "Updated Title",
        "author": "Test Author",
        "publisher": "Test Publisher",
        "published_date": "2023-01-01",
        "page_count": 100,
        "language": "en"
    })
    assert response.status_code == 404

def test_delete_book(client):
    """Test deleting an existing book."""
    # First, create a book to delete
    response = client.post(BOOKS_PREFIX, json=sample_book_data)
    assert response.status_code == 201
    book_uid = response.json()["uid"]

    # Now, delete the book
    response = client.delete(f"{BOOKS_PREFIX}/{book_uid}")
    assert response.status_code == 204

def test_delete_book_not_found(client):
    """Test deleting a non-existent book."""
    response = client.delete(f"{BOOKS_PREFIX}/non-existent-uid")
    assert response.status_code == 404
