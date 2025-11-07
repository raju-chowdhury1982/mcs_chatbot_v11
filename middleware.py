from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ConsigneeScopeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):  # type: ignore
        # Header has priority; body fallback handled in route.
        consignee_code = request.headers.get("X-Consignee-Code")
        request.state.consignee_code = consignee_code
        return await call_next(request)
