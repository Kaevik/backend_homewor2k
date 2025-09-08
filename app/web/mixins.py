
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden

class AuthRequiredMixin:
    def require_auth(self):
        # minimal cookie-based auth: expect 'session' cookie with value '1'
        session_val = self.request.cookies.get("session")
        if session_val is None:
            raise HTTPUnauthorized()
        if session_val != "1":
            raise HTTPForbidden()
