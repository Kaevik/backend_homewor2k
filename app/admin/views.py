from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp_apispec import docs
from aiohttp.web import View
from app.web.utils import ok_json_response, error_json_response
from app.admin.schemes import AdminSchema

class AdminLoginView(View):
    @docs(tags=["admin"], summary="Admin login")
    async def post(self):
        data = await self.request.json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return error_json_response("bad_request", status=400)

        admin = await self.request.app.store.admins.get_by_email(email)
        if not admin or admin.password != password:
            raise HTTPUnauthorized

        self.request.session["admin"] = admin.id
        return ok_json_response({"data": AdminSchema().dump(admin)})

class AdminCurrentView(View):
    @docs(tags=["admin"], summary="Get current admin")
    async def get(self):
        admin_id = self.request.session.get("admin")
        if not admin_id:
            raise HTTPUnauthorized

        admin = await self.request.app.store.admins.get_by_id(admin_id)
        return ok_json_response({"data": AdminSchema().dump(admin)})
