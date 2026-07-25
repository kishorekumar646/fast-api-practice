from typing import Any, Callable, Awaitable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status


class BookNotFoundException(Exception):
    pass

# Alias used in routes
BookNotFound = BookNotFoundException


class BookAlreadyExists(Exception):
    pass


class AccountNotFoundException(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


class InvalidToken(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class RevokeToken(Exception):
    pass


class AccessTokenRequired(Exception):
    pass


def create_exception_handler(
    exception_class: Any, status_code: int = status.HTTP_400_BAD_REQUEST
) -> Callable[[Request, Exception], Awaitable[JSONResponse]]:
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})
    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        BookAlreadyExists,
        lambda request, exc: JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "A book with this title and author already exists in your collection"},
        ),
    )
    app.add_exception_handler(
        UserAlreadyExist,
        lambda request, exc: JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "User already exists"},
        ),
    )
    app.add_exception_handler(
        BookNotFoundException,
        lambda request, exc: JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Book not found"},
        ),
    )
    app.add_exception_handler(
        AccountNotFoundException,
        lambda request, exc: JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Account not found"},
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(InvalidToken, status_code=status.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(InvalidCredentials, status_code=status.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        RevokeToken,
        create_exception_handler(RevokeToken, status_code=status.HTTP_401_UNAUTHORIZED),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(AccessTokenRequired, status_code=status.HTTP_401_UNAUTHORIZED),
    )

    @app.exception_handler(500)
    async def internal_server_error(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )
