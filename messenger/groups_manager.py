__author__ = 'rubydev'

from messenger import config
import re
from messenger import logger

logger = logger.get(__name__)

REGEX = '(?:\|?id:)?\s*(\d+)'

def get_groups():
    return config.get_key("groups")

def get_group_names():
    groups = get_groups()
    l =  list(map(get_group_name, groups))
    return l

def get_group_name(obj):
    return " %s |id: %s" % ( str(obj["name"]), str(obj["id"]) )

def get_group_id(st):
    logger.debug("Received '%s'" % st)
    p = re.compile(REGEX)
    r =  p.findall(st)[-1]
    logger.debug("Result '%s'" % r)
    return r

def make_group(id,name):
    return {
        "id": str(id),
        "name": str(name)
    }

def already_in_favourites(id, name):
    g = make_group(id, name)
    groups = get_groups()
    logger.debug("Checking if group{'id':%s, 'name':'%s'} is in %s" % (str(id), str(name), str(groups)))
    return g in groups

def remove_from_favourites(id,name=""):
    logger.debug("Trying to delete %s with id: %s" % (name, id))
    g = make_group(id, name)
    groups = get_groups()
    if g in groups:
        i = groups.index(g)
        del groups[i]
        set_groups(groups)
        return True
    else:
        return False



def set_groups(groups):
    config.set_key("groups", groups)
    return True

def add_favourite_group(id , name=""):
    list = get_groups()
    list.append(make_group(id, name))
    set_groups(list)

