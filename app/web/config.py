
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

    session = raw_config.get("session") or {}
    bot = raw_config.get("bot") or {}

    app.config = Config(
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        session=SessionConfig(key=session.get("key", "secret")) if session else None,
        bot=BotConfig(token=bot.get("token", ""), group_id=int(bot.get("group_id", 0))) if bot else None,
    )
