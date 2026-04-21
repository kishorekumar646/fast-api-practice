from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas import Book, BookCreateModel, BookUpdateModel
from .service import BookService
from src.errors import BookNotFoundException

book_router = APIRouter()
book_service = BookService()

@book_router.get(path='/', response_model=List[Book])
async def get_all_books():
    try:
        books = await book_service.get_all_books()
        return books
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@book_router.post(path='/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel):
    try:
        new_book = await book_service.add_book(book_data)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@book_router.patch(path='/{book_uid}', response_model=Book, status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_uid: str, book_data: BookUpdateModel):
    try:
        updated_book = await book_service.update_book(book_uid=book_uid, book_update=book_data)
        return updated_book
    except BookNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str):
    try:
        await book_service.delete_book(book_uid=book_uid)
    except BookNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")