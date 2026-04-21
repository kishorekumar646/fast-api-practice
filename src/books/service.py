from src.errors import BookNotFoundException
from datetime import datetime
import uuid
from .schemas import BookCreateModel, BookUpdateModel, Book

book_list = [
    Book(
        uid=uuid.uuid4(),
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        publisher="Scribner",
        published_date=datetime(1925, 4, 10).date(),
        page_count=218,
        language="English",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    Book(
        uid=uuid.uuid4(),
        title="To Kill a Mockingbird",
        author="Harper Lee",
        publisher="J.B. Lippincott & Co.",
        published_date=datetime(1960, 7, 11).date(),
        page_count=281,
        language="English",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]

class BookService:

    async def get_all_books(self):
        return book_list

    async def add_book(self, book: BookCreateModel):
        book_data = {
            "uid": uuid.uuid4(),
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "published_date": book.published_date,
            "page_count": book.page_count,
            "language": book.language,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        new_book = Book(**book_data)
        book_list.append(new_book)
        return new_book
    
    async def update_book(self, book_uid: str, book_update: BookUpdateModel):
        for book in book_list:
            if str(book.uid) == book_uid:
                book.title = book_update.title
                book.author = book_update.author
                book.publisher = book_update.publisher
                book.published_date = book_update.published_date
                book.page_count = book_update.page_count
                book.language = book_update.language
                book.updated_at = datetime.now()
                return book
        return None
    
    async def delete_book(self, book_uid: str):
        for book in book_list:
            if str(book.uid) == book_uid:
                book_list.remove(book)
                return
        raise BookNotFoundException(f"Book with uid {book_uid} not found.")