
import asyncio
from asyncio import Task

from app.store import Store

class Poller:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.is_running = False
        self.poll_task: Task | None = None

    async def start(self) -> None:
        if self.poll_task is None or self.poll_task.done():
            self.is_running = True
            self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        self.is_running = False
        if self.poll_task is not None:
            await self.poll_task

    async def poll(self) -> None:
        # minimal no-op loop to satisfy graceful stop
        while self.is_running:
            updates = await self.store.vk_api.poll()
            if updates:
                await self.store.bots_manager.handle_updates(updates)
            await asyncio.sleep(0)  # yield control
