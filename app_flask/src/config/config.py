import os


class Config:
    DEBUG = True
    SECRET_KEY = "J6j0bPa3AXe7nILlh24TaCWo6L2jV41YtokIbExs9BMUH2EYqTYPLisZqxjIlBtMab8pYeQ8tLZrWzuvdh4Al9DxajhoBW23fUUWqeeVl9MKpODOWbENmqOE9qj2dZ6m"
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@db:5432/mydatabase"
    FASTAPI_URL = os.environ.get("FASTAPI_URL") or "http://localhost:8000"
    API_KEY = "J6j0bPa3AXe7nILlh24TaCWo6L2jV41YtokIbExs9BMUH2EYqTYPLisZqxjIlBtMab8pYeQ8tLZrWzuvdh4Al9DxajhoBW23fUUWqeeVl9MKpODOWbENmqOE9qj2dZ6m"
    WTF_CSRF_ENABLED = True
