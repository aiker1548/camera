from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, session_maker):
        super().__init__(app)
        self.session_maker = session_maker

    async def dispatch(self, request: Request, call_next):
        async with self.session_maker() as session:
            request.state.db = session
            response = await call_next(request)
        return response