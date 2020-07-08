try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

try:
    __version__ = metadata.version('json-server.py')
except:
    __version__ = 'DEV'
