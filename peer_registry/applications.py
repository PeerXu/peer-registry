from peer_registry.app import app
from peer_registry.core import response
from peer_registry.core import Response
from peer_registry.core import stream_with_context
from peer_registry.lib import storage


store = storage.load()


@app.route('/v1/applications/<application_id>/layer', methods=['GET'])
def get_application_layer(application_id):
    return Response(stream_with_context(store.stream_read(store.application_layer_path(application_id))))


@app.route('/v1/applications/<application_id>/layer', methods=['PUT'])
def put_application_layer(application_id):
    return response('', 204)


@app.route('/v1/applications/<application_id>/json', methods=['GET'])
def get_application_json(application_id):
    return response(store.get_content(store.application_json_path(application_id)), raw=True)


@app.route('/v1/applications/<application_id>/json', methods=['PUT'])
def put_application_json(application_id):
    return response('', 204)


@app.route('/v1/applications/<application_id>/checksum', methods=['PUT'])
def put_application_checksum(application_id):
    return response('', 204)


@app.route('/v1/applications/<application_id>/checksum', methods=['GET'])
def get_application_checksum(application_id):
    return response(store.get_content(store.application_checksum_path(application_id)), raw=True)


@app.route('/v1/applications/<application_id>/ancestry', methods=['GET'])
def get_application_ancestry(application_id):
    return response(store.get_content(store.application_ancestry_path(application_id)), raw=True)
