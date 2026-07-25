from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.books.routes import book_router
from src.accounts.routes import account_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tag_router
from src.db.db import init_db
from src.errors import register_all_errors
from src.middleware import register_middleware

version = "v1"
version_prefix = f"/api/{version}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """

    :type app: object
    """
    await init_db()
    yield


app = FastAPI(
    title="My Book Store",
    version=version,
    lifespan=lifespan,
    license_info={
        "name": "IIIT RGUKT RK Valley",
        "url": "https://www.iiitrgv.ac.in",
    },
    contact={
        "name": "Kishore Kumar",
        "email": "kishore.kumar@example.com",
        "url": "https://github.com/kishorekumar646/",
    },
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redocs",
    openapi_url=f"{version_prefix}/openapi.json",
)

register_all_errors(app)
register_middleware(app)

app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["Auth"])
app.include_router(book_router, prefix=f"{version_prefix}/books", tags=["Books"])
app.include_router(review_router, prefix=f"{version_prefix}/reviews", tags=["Reviews"])
app.include_router(tag_router, prefix=f"{version_prefix}/tags", tags=["Tags"])
app.include_router(account_router, prefix=f"{version_prefix}/accounts", tags=["Accounts"])
