
from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response

def json_response(data: dict | None = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )

def error_json_response(
    http_status: int,
    status: str = "error",
    message: str | None = None,
    data: dict | None = None,
):
    if data is None:
        data = {}
    payload = {
        "status": status,
        "message": message if message is not None else "",
        "data": data,
    }
    return aiohttp_json_response(payload, status=http_status)
