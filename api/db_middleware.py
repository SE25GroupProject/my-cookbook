"""Middleware for handling database connections in FastAPI applications."""
import pathlib
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
try:
    from api.db.database import DatabaseConnection
except ImportError:
    from db.database import DatabaseConnection

class DBConnectionMiddleware(BaseHTTPMiddleware): # pylint: disable=too-few-public-methods
    """Middleware for handling database connections in FastAPI applications."""
    def __init__(self, app: FastAPI, db_path: str = "db/cookbook.db"):
        super().__init__(app)
        self.db_path = pathlib.Path(db_path).absolute()

    async def dispatch(self, request: Request, call_next):
        # Create a DB connection and attach it to the request's state
        request.state.db = DatabaseConnection(db_path=self.db_path)
        response = await call_next(request)

        request.state.db.conn.close()
        return response
