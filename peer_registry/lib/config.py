# copy from docker-registry:0.5.1 (https://github.com/docker/docker-registry.git)
# file: lib/config.py

import os
import yaml


class Config(object):

    def __init__(self, config):
        self._config = config

    def __repr__(self):
        return repr(self._config)

    def __getattr__(self, key):
        if key in self._config:
            return self._config[key]

    def get(self, *args, **kwargs):
        return self._config.get(*args, **kwargs)


_config = None


def load():
    global _config
    if _config is not None:
        return _config
    data = None
    config_locs = map(os.path.abspath, [
        '/etc/peer-registry',
        os.path.expanduser('~/.peer-registry'),
        os.path.join(os.path.dirname(__file__), '..', '..')
    ])
    config_path = None
    for loc in config_locs:
        path = os.path.join(loc, 'config.yml')
        if os.path.exists(path):
            config_path = path
            break
    if config_path is None:
        raise IOError("No config.yml in {0}".format(', '.join(config_locs)))
    with open(config_path) as f:
        data = yaml.load(f)
    config = data.get('common', {})
    flavor = os.environ.get('SETTINGS_FLAVOR', 'dev')
    config.update(data.get(flavor, {}))
    config['flavor'] = flavor
    _config = Config(config)
    return _config
