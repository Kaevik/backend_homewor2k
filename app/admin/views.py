from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from app.web.app import View
from app.web.utils import json_response

class AdminLoginView(View):
    async def post(self):
        payload = await self.request.json()
        email = payload.get("email")
        password = payload.get("password")
        admin = await self.store.admins.get_by_email(email)
        if not admin or not await self.store.admins.verify_password(admin, password):
            raise HTTPForbidden()
        response = json_response(data={"id": admin.id, "email": admin.email})
        response.set_cookie("session", str(admin.id))
        return response

class AdminCurrentView(View):
    async def get(self):
        session = self.request.cookies.get("session")
        if not session:
            raise HTTPUnauthorized()
        try:
            admin_id = int(session)
        except ValueError:
            raise HTTPForbidden()
        admin = next((a for a in self.database.admins if a.id == admin_id), None)
        if not admin:
            raise HTTPForbidden()
        return json_response({"id": admin.id, "email": admin.email})
