import sys
import platform
import urllib
import logging
import asyncio
import click
from gera2ld.pyserve import serve_forever
from aiohttp import web
from aiohttp.log import server_logger
from . import __version__
from .handlers import Handler

def parse_addr(host, default=('', 80)):
    result = urllib.parse.urlparse('//' + host)
    hostname = result.hostname
    if hostname is None: hostname = default[0]
    port = result.port
    if port is None: port = default[0]
    return hostname, port

async def start_server(loop, bind, filename):
    host, port = parse_addr(bind)
    handle = Handler(filename)
    web_server = web.Server(handle)
    server = await loop.create_server(web_server, host, port)
    return server

@click.command()
@click.option('-b', '--bind', default=':3000', help='the address to bind, default as `:3000`')
@click.argument('filename', default='db.json')
def main(bind, filename):
    logging.basicConfig(level=logging.INFO)
    server_logger.info(
        'JSON Server v%s/%s %s - by Gerald',
        __version__, platform.python_implementation(), platform.python_version())
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(start_server(loop, bind, filename))
    serve_forever(server, loop)
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
