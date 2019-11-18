import plistlib
from base64 import b64decode


def load(plistfile):
    with open(plistfile, 'rb') as f:
        return plistlib.load(f)


def dump(plist, dst):
    with open(dst, 'wb') as f:
        plistlib.dump(plist, f)


def data(b64str):
    return b64decode(b64str)


def get(plist, keys):
    '''Get item from keys
    '''
    ks = keys.split('/')
    item = plist
    for k in ks[:-1]:
        item = item[k]
    return item, ks[-1]
