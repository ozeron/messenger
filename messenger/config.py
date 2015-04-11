import os, json

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/config.json')


def load():
    text = open(DEFAULT_CONFIG_PATH, 'r').read()
    config = json.loads(text)
    return config
