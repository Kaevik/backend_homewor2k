from aiohttp import web
from app.web.utils import json_response, error_json_response


class AdminLoginView(web.View):
    async def post(self):
        data = await self.request.json()

        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return error_json_response(
                http_status=400,
                status="bad_request",
                message="email and password are required",
                data={"email": ["Missing data."]} if not email else {"password": ["Missing data."]}
            )

        admin = await self.store.admins.get_by_email(email)
        if not admin or not self.store.admins.verify_password(password, admin.password):
            raise web.HTTPForbidden(reason="invalid credentials")

        response = json_response({"id": admin.id, "email": admin.email})
        response.set_cookie("session", str(admin.id))
        return response


class AdminCurrentView(web.View):
    async def get(self):
        session_id = self.request.cookies.get("session")
        if not session_id:
            raise web.HTTPUnauthorized(reason="no session provided")

        admin = await self.store.admins.get_by_id(int(session_id))
        if not admin:
            raise web.HTTPForbidden(reason="invalid session")

        return json_response({"id": admin.id, "email": admin.email})
