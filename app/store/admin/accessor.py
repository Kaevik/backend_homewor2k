import typing
import hashlib
from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application

def _hash_password(p: str) -> str:
    return hashlib.sha256(p.encode('utf-8')).hexdigest()

class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        # create initial admin from config if not exists
        cfg = app.config.admin
        existing = await self.get_by_email(cfg.email)
        if existing is None:
            await self.create_admin(cfg.email, cfg.password)

    async def get_by_email(self, email: str) -> Admin | None:
        for a in self.app.database.admins:
            if a.email == email:
                return a
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = Admin(
            id=self.app.database.next_admin_id,
            email=email,
            password=_hash_password(password),
        )
        self.app.database.admins.append(admin)
        return admin

    async def verify_password(self, admin: Admin, password: str) -> bool:
        if admin.password is None:
            return False
        return admin.password == _hash_password(password)
