import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application

@dataclass
class SessionConfig:
    key: str

@dataclass
class AdminConfig:
    email: str
    password: str

@dataclass
class BotConfig:
    token: str
    group_id: int

@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig | None = None
    bot: BotConfig | None = None

def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    admin = raw_config.get("admin", {})
    session = raw_config.get("session", {})
    bot = raw_config.get("bot", {})

    app.config = Config(
        admin=AdminConfig(
            email=admin.get("email", ""),
            password=admin.get("password", ""),
        ),
        session=SessionConfig(key=session.get("key", "")) if session else None,
        bot=BotConfig(token=bot.get("token", ""), group_id=int(bot.get("group_id", 0))) if bot else None,
    )
