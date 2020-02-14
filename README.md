# json-server.py

[![PyPI](https://img.shields.io/pypi/v/json-server.py.svg)](https://pypi.org/project/json-server.py/)

Fake REST API with zero coding.

This project is heavily inspired by [json-server](https://github.com/typicode/json-server) in JavaScript.

Requires Python 3.5+.

## Usage

```
Usage: json-server [OPTIONS] [FILENAME]

Options:
  -b, --bind TEXT  the address to bind, default as `:3000`
  --help           Show this message and exit.
```

## Examples

```sh
# Start with default config
$ json-server

# Listen on port 3000
$ json-server -b :3000

# Specify a json file
$ json-server db.json
```
