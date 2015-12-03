from peer_registry.core import get_app
from peer_registry.core import response
from peer_registry.lib import config


app = get_app()


@app.route('/_ping')
def ping():
    return response()


@app.route('/')
def root():
    cfg = config.load()
    return response('Peer Registry ({0})'.format(cfg.flavor))
