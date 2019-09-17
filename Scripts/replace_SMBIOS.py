""" 
Replace SMBIOS field with given SerialNumber, MLB and SmUUID

Usage:

python replace_SMBIOS.py SN MLB SMUUID
"""

import sys
import plistlib
from shutil import copyfile
from os import path


def config_path(dirpath):
    return path.join(dirpath, 'config.plist')


def get_config(source):
    config_file = config_path(source)
    copyfile(config_file, config_file + '.bak')

    with open(config_file, 'rb') as inp:
        return plistlib.load(inp)
    return {}


def save_config(plist, source):
    with open(config_path(source), 'wb') as out:
        plistlib.dump(plist, out)


sn, mlb, uuid = sys.argv[1:]
efipath = path.join(path.dirname(__file__), '..')

clover = path.join(efipath, 'CLOVER')
config = get_config(clover)
config['SMBIOS']['SerialNumber'] = sn
config['SMBIOS']['BoardSerialNumber'] = mlb
config['SMBIOS']['SmUUID'] = uuid
save_config(config, clover)

oc = path.join(efipath, 'OC')
config = get_config(oc)
config['PlatformInfo']['Generic']['SystemSerialNumber'] = sn
config['PlatformInfo']['Generic']['MLB'] = mlb
config['PlatformInfo']['Generic']['SystemUUID'] = uuid
save_config(config, oc)
