
import json
from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized, HTTPUnprocessableEntity
from app.web.app import View
from app.web.utils import json_response

class AdminLoginView(View):
    async def post(self):
        # Validate payload
        try:
            body = await self.request.json()
        except Exception:
            body = {}
        if "email" not in body:
            raise HTTPUnprocessableEntity(
                text='{"json": {"email": ["Missing data for required field."]}}'
            )
        if "password" not in body:
            raise HTTPUnprocessableEntity(
                text='{"json": {"password": ["Missing data for required field."]}}'
            )
        email = body["email"]
        password = body["password"]

        import hashlib
        admin = await self.store.admins.get_by_email(email)
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if not admin or admin.password != hashed:
            raise HTTPForbidden()

        # set auth cookie
        response = json_response(data={"id": admin.id, "email": admin.email})
        response.set_cookie("session", str(admin.id))
        return response

class AdminCurrentView(View):
    async def get(self):
        session_val = self.request.cookies.get("session")
        if session_val is None:
            raise HTTPUnauthorized()
        # find admin
        try:
            admin_id = int(session_val)
        except ValueError:
            raise HTTPForbidden()
        admin = next((a for a in self.store.app.database.admins if a.id == admin_id), None)
        if admin is None:
            raise HTTPForbidden()
        return json_response(data={"id": admin.id, "email": admin.email})
