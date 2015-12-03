# copy from docker-registry:0.5.1 (https://github.com/docker/docker-registry.git)
# file: lib/config.py

import os
import shutil

from peer_registry.lib import config


class Storage(object):

    """ Storage is organized as follow:
    $ROOT/applications/<application_id>/json
    $ROOT/applications/<application_id>/layer
    $ROOT/repositories/<namespace>/<repository_name>/<tag_name>
    """

    # Useful if we want to change those locations later without rewriting
    # the code which uses Storage
    repositories = 'repositories'
    applications = 'applications'
    buffer_size = 4096

    def applications_list_path(self, namespace, repository):
        return '{0}/{1}/{2}/_applications_list'.format(self.repositories,
                                                 namespace,
                                                 repository)

    def application_json_path(self, application_id):
        return '{0}/{1}/json'.format(self.applications, application_id)

    def application_mark_path(self, application_id):
        return '{0}/{1}/_inprogress'.format(self.applications, application_id)

    def application_checksum_path(self, application_id):
        return '{0}/{1}/_checksum'.format(self.applications, application_id)

    def application_layer_path(self, application_id):
        return '{0}/{1}/layer'.format(self.applications, application_id)

    def application_ancestry_path(self, application_id):
        return '{0}/{1}/ancestry'.format(self.applications, application_id)

    def repository_json_path(self, namespace, repository):
        return '{0}/{1}/{2}/json'.format(self.repositories, namespace, repository)

    def tag_path(self, namespace, repository, tagname=None):
        if not tagname:
            return '{0}/{1}/{2}'.format(self.repositories,
                                        namespace,
                                        repository)
        return '{0}/{1}/{2}/tag_{3}'.format(self.repositories,
                                            namespace,
                                            repository,
                                            tagname)

    def index_applications_path(self, namespace, repository):
        return '{0}/{1}/{2}/_index_applications'.format(self.repositories,
                                                  namespace,
                                                  repository)

    def get_content(self, path):
        raise NotImplemented

    def put_content(self, path, content):
        raise NotImplemented

    def stream_read(self, path):
        raise NotImplemented

    def stream_write(self, path, fp):
        raise NotImplemented

    def list_directory(self, path=None):
        raise NotImplemented

    def exists(self, path):
        raise NotImplemented

    def remove(self, path):
        raise NotImplemented

    def get_size(self, path):
        raise NotImplemented


class LocalStorage(Storage):

    def __init__(self):
        self._config = config.load()
        self._root_path = self._config.storage_path

    def _init_path(self, path=None, create=False):
        path = os.path.join(self._root_path, path) if path else self._root_path
        if create is True:
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        return path

    def get_content(self, path):
        path = self._init_path(path)
        with open(path, mode='r') as f:
            return f.read()

    def put_content(self, path, content):
        path = self._init_path(path, create=True)
        with open(path, mode='w') as f:
            f.write(content)
        return path

    def stream_read(self, path):
        path = self._init_path(path)
        with open(path, mode='rb') as f:
            while True:
                buf = f.read(self.buffer_size)
                if not buf:
                    break
                yield buf

    def stream_write(self, path, fp):
        # Size is mandatory
        path = self._init_path(path, create=True)
        with open(path, mode='wb') as f:
            while True:
                try:
                    buf = fp.read(self.buffer_size)
                    if not buf:
                        break
                    f.write(buf)
                except IOError:
                    break

    def list_directory(self, path=None):
        path = self._init_path(path)
        prefix = path[len(self._root_path) + 1:] + '/'
        exists = False
        for d in os.listdir(path):
            exists = True
            yield prefix + d
        if exists is False:
            # Raises OSError even when the directory is empty
            # (to be consistent with S3)
            raise OSError('No such directory: \'{0}\''.format(path))

    def exists(self, path):
        path = self._init_path(path)
        return os.path.exists(path)

    def remove(self, path):
        path = self._init_path(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
            return
        os.remove(path)

    def get_size(self, path):
        path = self._init_path(path)
        return os.path.getsize(path)


_storage = {}


def load(kind=None):
    """ Returns the right storage class according to the configuration """
    global _storage
    if not kind:
        kind = config.load().storage.lower()
    if kind in _storage:
        return _storage[kind]
    if kind == 'local':
        store = LocalStorage()
    else:
        raise ValueError('Not supported storage \'{0}\''.format(kind))
    _storage[kind] = store
    return store
