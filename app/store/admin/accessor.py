
import typing
import hashlib

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application

class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        # create initial admin from config.yml
        cfg = app.config.admin
        if not any(a.email == cfg.email for a in app.database.admins):
            await self.create_admin(cfg.email, cfg.password)

    async def disconnect(self, app: "Application") -> None:
        # nothing special
        return

    async def get_by_email(self, email: str) -> Admin | None:
        for a in self.app.database.admins:
            if a.email == email:
                return a
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        admin = Admin(id=self.app.database.next_admin_id, email=email, password=hashed)
        self.app.database.admins.append(admin)
        return admin
