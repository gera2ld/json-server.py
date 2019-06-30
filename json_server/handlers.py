import json
import asyncio
import secrets
from aiohttp import web
from aiohttp.log import server_logger

FIELD_ID = 'id'

class IdGenerator:
    cache = {}

    def __init__(self, data = None):
        self.id_type = int
        self.id_max = 0
        self.id_set = set()
        if data is not None:
            self.update_items(data)

    def generate_id(self):
        if self.id_type is int:
            return self.id_max + 1
        for i in range(100):
            key = secrets.token_urlsafe(8)
            if key not in self.id_set:
                return key
        else:
            raise ValueError('Cannot generate unique ID')

    def update(self, item):
        item_id = item.get(FIELD_ID)
        if self.id_type is int:
            if isinstance(item_id, int):
                self.id_max = max(self.id_max, item_id)
            else:
                self.id_type = str
        self.id_set.add(str(item_id))

    def update_items(self, data):
        for item in data:
            self.update(item)

    @classmethod
    def load(cls, data):
        key = id(data)
        gen = cls.cache.get(key)
        if gen is None:
            gen = cls(data)
            cls.cache[key] = gen
        return gen

class DataWrapper:
    def __init__(self, filename):
        self.filename = filename
        try:
            data = json.load(open(filename, encoding='utf-8'))
        except FileNotFoundError:
            data = {}
        self.data = data

    def get(self, keys):
        data = self.data
        for key in keys:
            if isinstance(data, dict):
                child = data.get(key)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and str(item.get(FIELD_ID)) == key:
                        child = item
                        break
                else:
                    return
            else:
                return
            data = child
        return data

    def set(self, keys, value=None):
        keys = list(keys)
        last_key = keys.pop()
        parent = self.get(keys)
        if isinstance(parent, list):
            for index, item in enumerate(parent):
                if str(item.get(FIELD_ID)) == last_key:
                    break
            else:
                return
            if value is None:
                del parent[index]
            else:
                parent[index] = value
        else:
            if value is None:
                parent.pop(last_key, None)
            else:
                parent[last_key] = value

    def append(self, keys, item):
        array = self.get(keys)
        array.append(item)

    def dump(self):
        json.dump(self.data, open(self.filename, 'w', encoding='utf-8'))

class Handler:
    def __init__(self, filename):
        self.data = DataWrapper(filename)
        self.timer = None

    async def __call__(self, request):
        method = getattr(self, f'do_{request.method}', None)
        if method is None:
            raise web.HTTPNotImplemented()
        keys = request.path[1:].split('/')
        result = method(request, keys)
        if asyncio.iscoroutine(result):
            result = await result
        return result

    def dump(self):
        self.timer = None
        self.data.dump()
        server_logger.info('data dumped')

    def schedule_dump(self):
        loop = asyncio.get_event_loop()
        if self.timer is not None:
            self.timer.cancel()
        self.timer = loop.call_later(1, self.dump)

    def do_GET(self, request, keys):
        data = self.data.get(keys)
        if data is None:
            return web.json_response({}, status=404)
        return web.json_response(data)

    async def do_POST(self, request, keys):
        data = self.data.get(keys)
        if data is None:
            return web.json_response({}, status=404)
        body = await request.json()
        item = body.copy()
        if isinstance(data, list):
            # Plural
            if FIELD_ID not in item:
                gen = IdGenerator.load(data)
                item[FIELD_ID] = gen.generate_id()
            gen.update(item)
            self.data.append(keys, item)
        else:
            # Singular
            self.data.set(keys, item)
        self.schedule_dump()
        return web.json_response(item, status=201)

    async def do_PUT(self, request, keys):
        body = await request.json()
        item = body.copy()
        self.data.set(keys, item)
        self.schedule_dump()
        return web.json_response(item)

    async def do_PATCH(self, request, keys):
        body = await request.json()
        patch = body.copy()
        item = self.data.get(keys)
        item.update(patch)
        self.schedule_dump()
        return web.json_response(item)

    def do_DELETE(self, request, keys):
        self.data.set(keys)
        self.schedule_dump()
        return web.HTTPNoContent()
