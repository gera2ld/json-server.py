# json_server.py

[![PyPI](https://img.shields.io/pypi/v/json_server.py.svg)](https://pypi.org/project/json-server.py/)

Fake REST API with zero coding.

This project is heavily inspired by [json-server](https://github.com/typicode/json-server) in JavaScript.

Requires Python 3.5+.

## Usage

```
Usage: json_server [OPTIONS] [FILENAME]

Options:
  -b, --bind TEXT  the address to bind, default as `:3000`
  --help           Show this message and exit.
```

## Examples

```sh
# Start with default config
$ json_server

# Listen on port 3000
$ json_server -b :3000

# Specify a json file
$ json_server db.json
```
