from peer_registry.common.options import OPTIONS
from peer_registry.app import app

def start_server(host, port):
    from peer_registry import applications
    from peer_registry import index
    from peer_registry import search
    from peer_registry import tags

    app.run(host=host, port=port, debug=True)


def main():
    start_server(host=OPTIONS['host'], port=OPTIONS['port'])
