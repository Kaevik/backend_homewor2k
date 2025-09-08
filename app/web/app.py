from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from typing import Any

from app.admin.models import Admin
from app.store import Store, setup_store
from app.store.database.database import Database
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes

class Application(AiohttpApplication):
    config: Config
    store: Store
    database: Database

    def __init__(self):
        super().__init__()
        self.database = Database()

class Request(AiohttpRequest):
    @property
    def app(self) -> Application:  # type: ignore[override]
        return super().app  # type: ignore

class View(AiohttpView):
    @property
    def app(self) -> Application:  # type: ignore[override]
        return self.request.app  # type: ignore

    @property
    def store(self) -> Store:
        return self.app.store

    @property
    def database(self) -> Database:
        return self.app.database

    @property
    def config(self) -> Config:
        return self.app.config

    @property
    def data(self) -> dict:
        return self.request.get("data", {})

app = Application()

def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_routes(app)
    setup_middlewares(app)
    setup_store(app)
    return app
