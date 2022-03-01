import asyncio
import json
from typing import Any, Dict, List, Union
import uuid

from aiohttp import web
from aiohttp.log import server_logger

FIELD_ID = 'id'

DataKey = Union[int, str]
DataObject = Dict[DataKey, Any]
DataArray = List[DataObject]


class IdGenerator:
    cache = {}

    def __init__(self, array: DataArray):
        self.id_type = int
        self.id_max = 0
        self.update_items(array)

    def generate_id(self):
        if self.id_type is int:
            return self.id_max + 1
        return str(uuid.uuid4())

    def update(self, item: DataObject) -> DataObject:
        item_id = item.get(FIELD_ID)
        if item_id is None:
            item_id = self.generate_id()
            item = {**item, FIELD_ID: item_id}
        if self.id_type is int:
            if isinstance(item_id, int):
                self.id_max = max(self.id_max, item_id)
            else:
                self.id_type = str
        return item

    def update_items(self, array: DataArray):
        return [self.update(item) for item in array]

    @classmethod
    def load(cls, array: DataArray):
        key = id(array)
        gen = cls.cache.get(key)
        if gen is None:
            gen = cls(array)
            cls.cache[key] = gen
        return gen


class DataWrapper:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            data = json.load(open(filename, encoding='utf-8'))
        except FileNotFoundError:
            data = {}
        self.data = data

    def get(self, keys: List[DataKey]):
        data = self.data
        for key in keys:
            if isinstance(data, dict):
                child = data.get(key)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and str(
                            item.get(FIELD_ID)) == key:
                        child = item
                        break
                else:
                    return
            else:
                return
            data = child
        return data

    def set(self, keys: List[DataKey], value: DataObject = None):
        keys = list(keys)
        last_key = keys.pop()
        parent = self.get(keys)
        if isinstance(parent, list):
            for index, item in enumerate(parent):
                if str(item.get(FIELD_ID)) == last_key:
                    break
            else:
                index = -1
            if value is not None:
                try:
                    item_id = int(last_key)
                except ValueError:
                    item_id = last_key
                if str(item_id) != last_key:
                    item_id = last_key
                value = {
                    **value,
                    FIELD_ID: item_id,
                }
                value = IdGenerator.load(parent).update(value)
                if index < 0:
                    parent.append(value)
                else:
                    parent[index] = value
            elif index >= 0:
                del parent[index]
        elif isinstance(parent, dict):
            if value is None:
                parent.pop(last_key, None)
            else:
                parent[last_key] = value
        return value

    def append(self, keys: List[DataKey], item: DataObject):
        array = self.get(keys)
        assert isinstance(array, list)
        item = IdGenerator.load(array).update(item)
        array.append(item)
        return item

    def dump(self):
        json.dump(self.data, open(self.filename, 'w', encoding='utf-8'))


class Handler:
    def __init__(self, filename: str):
        self.data = DataWrapper(filename)
        self.timer = None

    async def __call__(self, request):
        method = getattr(self, f'do_{request.method}', None)
        if method is None:
            raise web.HTTPNotImplemented()
        keys = request.path.rstrip('/').split('/')[1:]
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

    def do_GET(self, request, keys: List[DataKey]):
        data = self.data.get(keys)
        if data is None:
            return web.json_response({}, status=404)
        return web.json_response(data)

    async def do_POST(self, request, keys: List[DataKey]):
        data = self.data.get(keys)
        if data is None:
            return web.json_response({}, status=404)
        body = await request.json()
        if isinstance(data, list):
            # Plural
            item = self.data.append(keys, body)
        else:
            # Singular
            item = self.data.set(keys, body)
        self.schedule_dump()
        return web.json_response(item, status=201)

    async def do_PUT(self, request, keys: List[DataKey]):
        body = await request.json()
        item = self.data.set(keys, body)
        self.schedule_dump()
        return web.json_response(item)

    async def do_PATCH(self, request, keys: List[DataKey]):
        body = await request.json()
        item = self.data.get(keys)
        assert isinstance(item, dict)
        item.update(body)
        self.schedule_dump()
        return web.json_response(item)

    def do_DELETE(self, request, keys: List[DataKey]):
        self.data.set(keys)
        self.schedule_dump()
        return web.HTTPNoContent()
