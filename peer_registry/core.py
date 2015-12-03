from flask import current_app
from flask import Response
from flask import json
from flask import stream_with_context
import urllib
import functools


def make_app():
    from flask import Flask

    app = Flask('peer-registry')

    return app


def get_app():
    try:
        from flask import current_app

        current_app._get_current_object()

        return current_app
    except RuntimeError:
        return make_app()


def response(data=None, code=200, headers=None, raw=False):
    if data is None:
        data = True
    h = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Expires': '-1',
        'Content-Type': 'application/json'
    }
    if headers:
        h.update(headers)
    try:
        if raw is False:
            data = json.dumps(data, indent=4, sort_keys=True, skipkeys=True)
    except TypeError:
        data = str(data)
    return current_app.make_response((data, code, h))


def api_error(message, code=400, headers=None):
    return response({'error': message}, code, headers)


def gen_random_string(length=16):
    return ''.join([random.choice(string.ascii_uppercase + string.digits)
                    for x in range(length)])


def parse_repository_name(f):
    @functools.wraps(f)
    def wrapper(repository, *args, **kwargs):
        parts = repository.rstrip('/').split('/', 1)
        if len(parts) < 2:
            namespace = 'library'
            repository = parts[0]
        else:
            (namespace, repository) = parts
        repository = urllib.quote_plus(repository)
        return f(namespace, repository, *args, **kwargs)
    return wrapper
