from peer_registry.app import app


@app.route('/v1/search', methods=['GET'])
def get_search():
    return response('', 204)
