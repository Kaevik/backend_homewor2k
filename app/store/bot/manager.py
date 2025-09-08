import typing

from app.store.vk_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application

class BotManager:
    def __init__(self, app: "Application"):
        self.app = app

    async def handle_updates(self, updates: list[Update]):
        if not updates:
            return
        for upd in updates:
            try:
                user_id = upd.object.message.from_id
            except Exception:
                continue
            await self.app.store.vk_api.send_message(
                Message(user_id=user_id, text="Hello from quiz-bot!")
            )
