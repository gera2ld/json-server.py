import sys
import platform
import urllib
import logging
import asyncio
import click
from gera2ld.pyserve import run_forever, start_server_aiohttp
from aiohttp.log import server_logger
from .handlers import Handler
from . import __version__


@click.command()
@click.version_option(__version__)
@click.option('-b',
              '--bind',
              default=':3000',
              help='Set address to bind, default as `:3000`')
@click.argument('filename', default='db.json')
def main(bind, filename):
    '''Start a JSON server.

    FILENAME refers to the JSON file where your data is stored.
    `db.json` will be used if not specified.
    '''

    logging.basicConfig(level=logging.INFO)
    server_logger.info('JSON Server v%s/%s %s - by Gerald', __version__,
                       platform.python_implementation(),
                       platform.python_version())
    handle = Handler(filename)
    run_forever(start_server_aiohttp(handle, bind))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
