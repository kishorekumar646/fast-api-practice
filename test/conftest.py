import pytest
import uuid
import asyncio
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src import app
from src.books.schemas import Book
from src.db.db import get_session


async def _init_test_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture(scope="module")
def client():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    asyncio.run(_init_test_db(engine))

    async def override_get_session():
        Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        async with Session() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


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