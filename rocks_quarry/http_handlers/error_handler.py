import json
from aiohttp import web

@web.middleware
async def wrap_request(request, handler):
    response = await handler(request)
    if response.status == 200:
        return response
    message = response.body
    return web.json_response(data = {"error" : message.decode("utf-8")}, status = response.status)
