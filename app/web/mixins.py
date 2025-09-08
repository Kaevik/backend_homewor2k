from aiohttp.web_exceptions import HTTPUnauthorized
from app.web.middlewares import HTTP_ERROR_CODES
from app.web.utils import error_json_response

class AuthRequiredMixin:
    async def ensure_auth(self, request):
        session = request.cookies.get("session")
        if not session:
            raise HTTPUnauthorized(
                reason=HTTP_ERROR_CODES[401]
            )
