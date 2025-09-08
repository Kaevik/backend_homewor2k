
from aiohttp.web_middlewares import middleware

@middleware
async def validation_middleware(request, handler):
    # No-op validation; views will perform manual validation and raise HTTPUnprocessableEntity
    return await handler(request)
