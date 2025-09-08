
import pytest
from aiohttp.test_utils import TestServer, TestClient

@pytest.fixture
def aiohttp_client(event_loop):
    async def maker(app):
        server = TestServer(app)
        await server.start_server()
        client = TestClient(server)
        await client.start_server()
        return client
    return maker
