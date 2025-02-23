from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import pathlib
try:
    from db.database import Database_Connection
except Exception:
    from api.db.database import Database_Connection
class DBConnectionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, db_path: str = "cookbook.db"):
        super().__init__(app)
        self.db_path = pathlib.Path(db_path).absolute()

    async def dispatch(self, request: Request, call_next):
        # Create a DB connection and attach it to the request's state
        request.state.db = Database_Connection(dbPath=self.db_path)
        response = await call_next(request)
        return response