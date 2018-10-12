from aiohttp import web

from .http_handlers import delete_handler
from .http_handlers import error_handler
from .http_handlers import get_handler
from .http_handlers import put_handler


class Server:
    def __init__(self, database, port):
        self.database = database
        self.port = port
        self.app = web.Application(middlewares=[error_handler.wrap_request])
        self.setup_routes()
        self.get_handler = get_handler.GetHandler(self.database)
        self.put_handler = put_handler.PutHandler(self.database)

        self.delete_handler = delete_handler.DeleteHandler(self.database)

    def setup_routes(self):
        # Just send the entire document down
        route_path = '/api/v1alpha/{path:.*}'
        # Rocksdb isn't asyncio by nature. May want to
        # consider making this async by wrapping the request
        # in something, making some server threads, queuing, etc.
        routes = [
            web.get(route_path, self.handle_get),
            web.put(route_path, self.handle_put),
            web.delete(route_path, self.handle_delete)
        ]
        self.app.add_routes(routes)

    async def handle_get(self, request):
        status, data = self.get_handler.handle_request(request.match_info['path'].encode())

        return web.Response(status = status, body = data)

    async def handle_put(self, request):
        data = await request.read()
        status = self.put_handler.handle_request(request.match_info['path'].encode(), data)
        return web.Response(status = status)

    async def handle_delete(self, request):
        status, data = self.delete_handler.handle_request(request.match_info['path'].encode())

        return web.Response(status = status, body = data)

    def run(self):
        web.run_app(self.app, port = self.port)
