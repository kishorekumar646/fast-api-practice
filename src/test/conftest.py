import pytest
import uuid
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.books.schemas import Book
from datetime import datetime
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def test_book():
    return Book(
        uid=uuid.uuid4(),
        title='test',
        author='test_author',
        publisher='test_publisher',
        published_date=datetime.now(),
        page_count=100,
        language='en',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )