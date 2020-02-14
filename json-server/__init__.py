from importlib.metadata import version

try:
    __version__ = version('json-server.py')
except:
    __version__ = 'DEV'
