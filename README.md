# json-server.py

[![PyPI](https://img.shields.io/pypi/v/json-server.py.svg)](https://pypi.org/project/json-server.py/)

Fake REST API with zero coding.

This project is heavily inspired by [json-server](https://github.com/typicode/json-server) in JavaScript.

Requires Python 3.6+.

## Installation

It's highly recommended to install with [pipx](https://pipxproject.github.io/pipx/).

```sh
$ pipx install json-server.py
```

Or install with pip at your own risk:

```sh
$ pip3 install json-server.py
```

## Get Started

Create a `db.json` file with following content:

```json
{
  "posts": []
}
```

Start a server:

```sh
$ json-server db.json
```

Create a post:

```sh
$ curl -H 'content-type: application/json' -d '{"content":"blablabla"}' http://localhost:3000/posts
```

List all posts:

```sh
$ curl http://localhost:3000/posts
```

## Usage

```
Usage: json-server [OPTIONS] [FILENAME]

  Start a JSON server.

  FILENAME refers to the JSON file where your data is stored. `db.json` will
  be used if not specified.

Options:
  --version        Show the version and exit.
  -b, --bind TEXT  Set address to bind, default as `:3000`
  --help           Show this message and exit.
```

**Note:**

- Collections must be contained in your data file before starting the server, otherwise the server cannot decide the type of resources.

### Examples

```sh
# Start with default config
$ json-server

# Listen on port 3000
$ json-server -b :3000

# Specify a json file
$ json-server db.json
```
