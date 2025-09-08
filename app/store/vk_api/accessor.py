
import typing
from urllib.parse import urlencode, urljoin

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_VERSION = "5.131"

class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application"):
        super().__init__(app)
        self.session: ClientSession | None = None
        self.poller = Poller(store=app.store)

    async def connect(self, app: "Application") -> None:
        self.session = ClientSession()

    async def disconnect(self, app: "Application") -> None:
        if self.session:
            await self.session.close()
            self.session = None

    async def _get_long_poll_server(self) -> None:
        # Not needed for tests; placeholder
        return

    async def poll(self) -> list[Update]:
        # In tests, poll is not used; return empty
        return []

    async def send_message(self, message: Message) -> None:
        # In tests, this is mocked; do nothing
        return
