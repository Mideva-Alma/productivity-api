# Productivity API

A Flask REST API for a productivity application where users can securely sign up, log in, and manage their personal notes.

## Features

* User registration
* JWT authentication
* Secure password hashing with Flask-Bcrypt
* Current user/session endpoint
* Create, read, update, and delete notes
* User-owned notes
* Protected routes
* Pagination for notes
* Input validation with Marshmallow
* Database migrations with Flask-Migrate
* Database seeding

## Technologies

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-RESTful
* Flask-Bcrypt
* Flask-JWT-Extended
* Marshmallow
* SQLite
* Pipenv

## Installation

Clone the repository:

```bash
git clone https://github.com/Mideva-Alma/productivity-api.git
cd productivity-api
```

Install the dependencies:

```bash
pipenv install
pipenv install --dev pytest
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

Initialize the database migrations:

```bash
pipenv run flask db init
```

Create a migration:

```bash
pipenv run flask db migrate -m "create users and notes tables"
```

Apply the migration:

```bash
pipenv run flask db upgrade
```

## Running the Application

Start the Flask development server:

```bash
pipenv run python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

You can also test the API status endpoint:

```http
GET /
```

Example response:

```json
{
  "message": "Productivity API is running"
}
```

## Authentication

The API uses JSON Web Tokens (JWT) for authentication.

### Signup

Create a new user:

```http
POST /signup
```

Request body:

```json
{
  "username": "alma",
  "password": "password123"
}
```

Successful response:

```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "alma"
  }
}
```

### Login

Log in with an existing account:

```http
POST /login
```

Request body:

```json
{
  "username": "alma",
  "password": "password123"
}
```

The response contains an access token:

```json
{
  "access_token": "YOUR_JWT_TOKEN",
  "user": {
    "id": 1,
    "username": "alma"
  }
}
```

Use the returned token in the `Authorization` header when accessing protected endpoints:

```text
Authorization: Bearer YOUR_JWT_TOKEN
```

### Current User

Get the currently authenticated user:

```http
GET /me
```

This endpoint requires a valid JWT token.

Example response:

```json
{
  "id": 1,
  "username": "alma"
}
```

## Notes Endpoints

All note endpoints require authentication.

### Get Notes

Retrieve the authenticated user's notes:

```http
GET /notes
```

Pagination can be controlled using `page` and `per_page`:

```http
GET /notes?page=1&per_page=5
```

Example response:

```json
{
  "notes": [
    {
      "id": 1,
      "title": "Study Plan",
      "content": "Complete Flask authentication and CRUD.",
      "user_id": 1
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 5,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### Create a Note

Create a new note:

```http
POST /notes
```

Request body:

```json
{
  "title": "Study Plan",
  "content": "Complete Flask authentication and CRUD."
}
```

Example response:

```json
{
  "id": 1,
  "title": "Study Plan",
  "content": "Complete Flask authentication and CRUD.",
  "user_id": 1
}
```

### Update a Note

Update an existing note:

```http
PATCH /notes/<id>
```

Example:

```http
PATCH /notes/1
```

Request body:

```json
{
  "title": "Updated Study Plan"
}
```

### Delete a Note

Delete an existing note:

```http
DELETE /notes/<id>
```

Example:

```http
DELETE /notes/1
```

A successful deletion returns:

```text
204 No Content
```

## Authorization

Users can only access and modify their own notes.

The authenticated user's ID is obtained from the JWT token. Note queries are filtered using the user's ID to prevent users from accessing another user's notes.

## Validation

Marshmallow is used to validate incoming data.

Usernames must:

* Be between 3 and 80 characters
* Be unique

Passwords must:

* Be at least 6 characters long

Note titles must:

* Be between 1 and 120 characters

Note content must:

* Not be empty

## Password Security

Passwords are never stored as plain text.

Flask-Bcrypt is used to hash passwords before they are stored in the database.

Passwords are checked using a secure password hash comparison during login.

## Database Models

### User

The `User` model contains:

* `id`
* `username`
* `password`

A user can have multiple notes.

### Note

The `Note` model contains:

* `id`
* `title`
* `content`
* `user_id`

Each note belongs to one user.

## Database Migrations

Flask-Migrate is used to manage database schema changes.

Create a migration:

```bash
pipenv run flask db migrate -m "migration message"
```

Apply migrations:

```bash
pipenv run flask db upgrade
```

## Seeding

The project includes a `seed.py` file that creates sample users and notes.

Run the seed file with:

```bash
pipenv run python seed.py
```

The seed file creates:

* Two users
* Three sample notes

The seeded users use the following password:

```text
password123
```

## API Status Codes

| Status Code | Meaning                                        |
| ----------- | ---------------------------------------------- |
| 200         | Request successful                             |
| 201         | Resource created                               |
| 204         | Resource deleted successfully                  |
| 400         | Invalid request or validation error            |
| 401         | Authentication required or invalid credentials |
| 404         | Resource not found                             |
| 409         | Username already exists                        |

## Project Structure

```text
productivity-api/
│
├── app.py
├── models.py
├── schemas.py
├── seed.py
├── Pipfile
├── Pipfile.lock
├── README.md
├── migrations/
│   ├── versions/
│   └── ...
└── .gitignore
```

## API Endpoint Summary

| Method | Endpoint      | Authentication | Description                      |
| ------ | ------------- | -------------- | -------------------------------- |
| GET    | `/`           | No             | Check API status                 |
| POST   | `/signup`     | No             | Create a user                    |
| POST   | `/login`      | No             | Log in and receive JWT           |
| GET    | `/me`         | Yes            | Get current user                 |
| GET    | `/notes`      | Yes            | Get user's notes with pagination |
| POST   | `/notes`      | Yes            | Create a note                    |
| PATCH  | `/notes/<id>` | Yes            | Update a note                    |
| DELETE | `/notes/<id>` | Yes            | Delete a note                    |

## Authentication Header

Protected endpoints require the JWT access token:

```text
Authorization: Bearer YOUR_JWT_TOKEN
```

JWT access tokens are temporary. A new token is issued when the user logs in again.

## Project Status

The Productivity API provides authenticated user management and CRUD operations for user-owned notes with validation, password protection, pagination, database migrations, and seed data.
