from aiohttp.web_response import json_response

def ok_json_response(data: dict = None):
    resp = {"status": "ok"}
    if data:
        resp.update(data)
    return json_response(resp)

def error_json_response(error: str, status: int = 400):
    return json_response({"status": error}, status=status)
