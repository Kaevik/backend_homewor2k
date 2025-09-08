import json
import typing

from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
try:
    from aiohttp_apispec import validation_middleware  # type: ignore
except Exception:
    async def validation_middleware(app, handler=None):
        # dummy passthrough when aiohttp_apispec is not installed
        async def _middleware(request, h=handler):
            return await (h or (lambda r: r))(request)
        return _middleware

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}

@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPException as e:
        status = HTTP_ERROR_CODES.get(e.status, HTTP_ERROR_CODES[500])
        return error_json_response(
            http_status=e.status,
            status=status,
            message=e.reason,
            data={},
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=str(e),
            data={},
        )

    return response

def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    # validation_middleware in aiohttp_apispec is a factory
    try:
        app.middlewares.append(validation_middleware)
    except Exception:
        pass
