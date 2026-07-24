import pytest
import uuid
from datetime import datetime
from fastapi.testclient import TestClient
from src import app
from src.books.schemas import Book


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def test_book():
    return Book(
        uid=uuid.uuid4(),
        title="test",
        author="test_author",
        publisher="test_publisher",
        published_date="2024-01-01",
        page_count=100,
        language="en",
        user_uid=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
