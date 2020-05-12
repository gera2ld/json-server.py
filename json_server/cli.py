import sys
import platform
import urllib
import logging
import asyncio
import click
from gera2ld.pyserve import serve_aiohttp
from aiohttp.log import server_logger
from .handlers import Handler
from . import __version__

@click.command()
@click.option('-b', '--bind', default=':3000', help='the address to bind, default as `:3000`')
@click.argument('filename', default='db.json')
def main(bind, filename):
    logging.basicConfig(level=logging.INFO)
    server_logger.info(
        'JSON Server v%s/%s %s - by Gerald',
        __version__, platform.python_implementation(), platform.python_version())
    handle = Handler(filename)
    serve_aiohttp(handle, bind)
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
