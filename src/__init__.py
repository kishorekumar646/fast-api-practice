from fastapi import FastAPI
from src.books.routes import book_router
from src.accounts.routes import account_router

version = 'v1'
version_prefix = f'/api/{version}'
app = FastAPI(
    title='My Book Store',
    version=version,
    license_info={
        "name": "IIIT RGUKT RK Valley",
        "url": "https://www.iiitrgv.ac.in"
    },
    contact={
        "name": "Kishore Kumar",
        "email": "kishore.kumar@example.com",
        "url": "https://github.com/kishorekumar646/"
    },
    docs_url=f'{version_prefix}/docs',
    redoc_url=f'{version_prefix}/redocs',
    openapi_url=f'{version_prefix}/openapi.json'
)

app.include_router(book_router, prefix=f'{version_prefix}/books', tags=['Books'])
app.include_router(account_router, prefix=f'{version_prefix}/accounts', tags=['Accounts'])