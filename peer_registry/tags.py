from peer_registry.app import app
from peer_registry.core import json
from peer_registry.core import response
from peer_registry.core import parse_repository_name
from peer_registry.lib import storage

store = storage.load()


@app.route('/v1/repositories/<path:repository>/tags', methods=['GET'])
@parse_repository_name
def get_tags(namespace, repository):
    tags = []
    tag_path = store.tag_path(namespace, repository)
    for tag_file in store.list_directory(tag_path):
        full_tag_name = tag_file.split('/')[-1]
        if not full_tag_name.startswith('tag_'):
            continue
        tag = {}
        tag_name = full_tag_name[4:]
        tag_raw = store.get_content(store.tag_path(namespace, repository, tag_name))
        tag_json = json.loads(tag_raw)
        tag['name'] = tag_name
        tag['application_id'] = tag_json['application_id']
        tags.append(tag)

    return response(tags)


@app.route('/v1/repositories/<path:repository>/tags/<tag>', methods=['GET'])
@parse_repository_name
def get_tag(namespace, repository, tag):
    return response('', 204)


@app.route('/v1/repositories/<path:repository>/tags/<tag>', methods=['PUT'])
@parse_repository_name
def put_tag(namespace, repository, tag):
    return response('', 204)


@app.route('/v1/repositories/<path:repository>/tags/<tag>', methods=['DELETE'])
@parse_repository_name
def delete_tag(namespace, repository, tag):
    return response('', 204)


@app.route('/v1/repositories/<path:repository>/tags', methods=['DELETE'])
@parse_repository_name
def delete_repository(namespace, repository):
    return response('', 204)
