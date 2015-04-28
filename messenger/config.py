import os, json

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/config.json')

def read():
    f = open(DEFAULT_CONFIG_PATH, 'r')
    text = f.read()
    f.close()
    return text

def write(str):
    f = open(DEFAULT_CONFIG_PATH, 'w')
    f.write(str)
    f.close
    return True


def load():
    config = json.loads(read())
    return config


def get_key(key):
    c = load()
    if key in c:
        return c[key]
    else:
        return {}

def set_key(key, data):
    dict = load()
    dict[key] = data
    write(json.dumps(dict))
    return True
