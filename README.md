# BookStore API

A production-ready RESTful API for managing a digital bookstore — built with **FastAPI**, **SQLModel**, and **async SQLite**. Supports books, reviews, tags, and user account management with JWT-based authentication and role-based access control.

---

## Features

- **JWT Authentication** — Access & refresh token flow with token revocation via Redis blocklist
- **Role-Based Access Control** — `admin` and `user` roles enforced per endpoint
- **Books** — Full CRUD with duplicate prevention (title + author per user)
- **Reviews** — Create, read, update, and delete reviews per book with rating validation (1–5)
- **Tags** — Tag management with many-to-many book associations
- **Accounts** — User profile management with admin controls
- **Dependency Inversion** — All services injected via FastAPI `Depends()` against abstract interfaces
- **Async** — Fully async database access via `aiosqlite` + `SQLAlchemy` async engine
- **Interactive Docs** — Swagger UI and ReDoc out of the box

---

## Tech Stack

| Layer       | Technology                              |
| ----------- | --------------------------------------- |
| Framework   | FastAPI 0.116                           |
| ORM         | SQLModel 0.0.39 + SQLAlchemy 2.0        |
| Database    | SQLite (async via aiosqlite)            |
| Auth        | JWT (`python-jose`) + bcrypt            |
| Blocklist   | Redis                                   |
| Validation  | Pydantic v2                             |
| Testing     | pytest + in-memory SQLite               |

---

## Project Structure

```
src/
├── auth/           # Signup, login, logout, token refresh
│   ├── interfaces.py
│   ├── routes.py
│   ├── schemas.py
│   ├── service.py
│   └── utils.py
├── accounts/       # User profile management
│   ├── dependencies.py   # AccessTokenBearer, RoleChecker
│   ├── interfaces.py
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
├── books/          # Book CRUD + duplicate prevention
│   ├── interfaces.py
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
├── reviews/        # Book reviews with rating validation
│   ├── interfaces.py
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
├── tags/           # Tag management + book-tag associations
│   ├── interfaces.py
│   ├── routes.py
│   ├── schemas.py
│   └── service.py
├── db/
│   ├── db.py       # Async engine + session factory
│   ├── models.py   # SQLModel table definitions
│   └── redis.py    # Token blocklist
├── errors.py       # Global exception classes + handlers
├── middleware.py
└── config.py       # Settings via pydantic-settings
test/
├── conftest.py     # In-memory SQLite test client
└── test_book.py
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Redis (for token blocklist)

### Installation

```bash
# Clone the repository
git clone https://github.com/kishorekumar646/bookstore-api.git
cd bookstore-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite+aiosqlite:///./bookstore.db
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRY=3600
REFRESH_TOKEN_EXPIRY=604800
REDIS_URL=redis://localhost:6379/0
```

### Running the Server

```bash
fastapi dev src/ --reload
```

The API will be available at `http://localhost:8000`.

---

## API Documentation

| URL                                          | Description      |
| -------------------------------------------- | ---------------- |
| `http://localhost:8000/api/v1/docs`          | Swagger UI       |
| `http://localhost:8000/api/v1/redocs`        | ReDoc            |
| `http://localhost:8000/api/v1/openapi.json`  | OpenAPI schema   |

---

## API Reference

### Auth — `/api/v1/auth`

| Method | Endpoint   | Description                   | Auth          |
| ------ | ---------- | ----------------------------- | ------------- |
| POST   | `/signup`  | Register a new user           | Public        |
| POST   | `/login`   | Login and receive tokens      | Public        |
| GET    | `/refresh` | Get a new access token        | Refresh token |
| POST   | `/logout`  | Revoke current token          | Access token  |

### Books — `/api/v1/books`

| Method | Endpoint            | Description                        | Role              |
| ------ | ------------------- | ---------------------------------- | ----------------- |
| GET    | `/`                 | List all books (with reviews/tags) | `user`, `admin`   |
| GET    | `/{book_uid}`       | Get a single book                  | `user`, `admin`   |
| GET    | `/user/{user_uid}`  | Get books by user                  | `user`, `admin`   |
| POST   | `/`                 | Create a book                      | `user`, `admin`   |
| PATCH  | `/{book_uid}`       | Update a book                      | `user`, `admin`   |
| DELETE | `/{book_uid}`       | Delete a book                      | `user`, `admin`   |

### Reviews — `/api/v1/reviews`

| Method | Endpoint              | Description                    | Role            |
| ------ | --------------------- | ------------------------------ | --------------- |
| GET    | `/`                   | List all reviews               | `user`, `admin` |
| GET    | `/book/{book_uid}`    | Get reviews for a book         | `user`, `admin` |
| GET    | `/{review_uid}`       | Get a single review            | `user`, `admin` |
| POST   | `/book/{book_uid}`    | Create a review (rating 1–5)   | `user`, `admin` |
| PATCH  | `/{review_uid}`       | Update a review                | `user`, `admin` |
| DELETE | `/{review_uid}`       | Delete a review                | `user`, `admin` |

### Tags — `/api/v1/tags`

| Method | Endpoint                        | Description           | Role            |
| ------ | ------------------------------- | --------------------- | --------------- |
| GET    | `/`                             | List all tags         | `user`, `admin` |
| POST   | `/`                             | Create a tag          | `user`, `admin` |
| DELETE | `/{tag_uid}`                    | Delete a tag          | `admin`         |
| POST   | `/book/{book_uid}/{tag_uid}`    | Add tag to book       | `user`, `admin` |
| DELETE | `/book/{book_uid}/{tag_uid}`    | Remove tag from book  | `user`, `admin` |

### Accounts — `/api/v1/accounts`

| Method | Endpoint       | Description          | Role            |
| ------ | -------------- | -------------------- | --------------- |
| GET    | `/`            | List all accounts    | `admin`         |
| GET    | `/me`          | Get own account      | `user`, `admin` |
| GET    | `/{user_uid}`  | Get account by UID   | `user`, `admin` |
| PATCH  | `/{user_uid}`  | Update account       | `user`, `admin` |
| DELETE | `/{user_uid}`  | Delete account       | `admin`         |

---

## Authentication Flow

```
POST /api/v1/auth/signup      →  Create account
POST /api/v1/auth/login       →  { access_token, refresh_token }
GET  /api/v1/auth/refresh     →  New access_token  (send refresh_token as Bearer)
POST /api/v1/auth/logout      →  Revoke token
```

All protected endpoints require:

```
Authorization: Bearer <access_token>
```

---

## Running Tests

```bash
pytest test/ -v
```

Tests use an isolated **in-memory SQLite** database — the real database is never touched during test runs.

---

## License

This project is licensed under the terms of **IIIT RGUKT RK Valley**.  
Contact: [Kishore Kumar](https://github.com/kishorekumar646/)
