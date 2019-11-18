from utils import plist, path, terminal
import plistlib
from pathlib import Path, PosixPath
from sys import argv
import uuid
import os

'''This script update config
For OpenCore config, it will update patches, SSDTs, kexts and drivers info
For Clover config, it will update patches

This script will also help to fill SN, MLB and SmUUID fields
'''


configpath = path.dst

if path.dsttype in ('oc', 'clover'):
    configpath = path.Root('config.plist')

if not configpath.exists():
    plistpath = path.Root('Plist', path.roottype + '.plist')
    path.cp(plistpath, configpath)
    print('No config.plist, use', plistpath)

print(terminal.PREFIX, 'Updating', configpath)

config = plist.load(configpath)

isclover = 'Boot' in config
isoc = not isclover

if isclover:
    smbios = config['SMBIOS']
    mapper = dict(sn='SerialNumber', mlb='BoardSerialNumber', smuuid='SmUUID')
else:
    smbios = config['PlatformInfo']['Generic']
    mapper = dict(sn='SystemSerialNumber', mlb='MLB', smuuid='SystemUUID')

oc = [
    ('DeviceProperties/Add', 'Devices/Properties'),
    ('NVRAM/Add/4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14/UIScale',
     'BootGraphics/UIScale'),
    ('NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args', 'Boot/Arguments')
]
if isclover:
    oc = [(k2, k1) for (k1, k2) in oc]

'''
Update config from another config
'''
if len(argv) > 2:
    another = argv[2]
    config2 = plist.load(another)
    if (isclover and 'Boot' in config2) or (isoc and 'Boot' not in config2):
        print('Replace everything from', another, 'to',
              configpath, 'except SN, MLB and SmUUID')
        if isclover:
            smbios2 = config2['SMBIOS']
        else:
            smbios2 = config2['PlatformInfo']['Generic']
        for k in mapper.keys():
            smbios2[mapper[k]] = smbios[mapper[k]]
        config = config2
    else:
        for (k1, k2) in oc:
            i1, k1 = plist.get(config, k1)
            i2, k2 = plist.get(config2, k2)
            print('Set', k1, 'to', i2[k2])
            i1[k1] = i2[k2]


'''
Check SN, MLB and SmUUID
'''
notfounds = [info for info in mapper.keys()
             if mapper[info] not in smbios or smbios[mapper[info]] == 'FillThis']


if notfounds and terminal.Confirm('Missing ' + ' '.join(notfounds).upper() + ', do you want to fill them?'):
    # get sn, mlb and uuid
    inp = terminal.Input(
        'Please input your own SN, MLB and SmUUID(left blank to generate new):')
    if not inp.strip():
        macserial = terminal.executable(path.Root('Tools', 'macserial'))
        result = os.popen(
            '{} -m MacBookPro13,3 -g -n 1'.format(macserial)).read()
        sn, mlb = result[:-1].split(' | ')
        smuuid = str(uuid.uuid4()).upper()
        print('New SN, MLB and SmUUID are generated:')
        print('SN:', sn)
        print('MLB:', mlb)
        print('SmUUID:', smuuid)
    else:
        sn, mlb, smuuid = inp.split()

    for k, v in zip(mapper.keys(), (sn, mlb, smuuid)):
        smbios[mapper[k]] = v

    print('SN, MLB and SmUUID are updated')


def get_patches(dsl_folder):
    '''Get patches from dsl files
    patches in .dsl file should have following pattern:
    ```
    // Patch: xxx
    // Find: ABC
    // Replace: DEF
    ```
    Return a list of patches
    '''
    patches = []
    for dsl in Path(dsl_folder).glob('*.dsl'):
        with open(dsl, 'r') as f:
            while True:
                line = f.readline()
                if line.startswith('// Patch:'):
                    patches.append(
                        {
                            'Comment': line[9:].strip(),
                            'Find': plist.data(f.readline()[8:].strip()),
                            'Replace': plist.data(f.readline()[11:].strip())
                        }
                    )
                elif not line:
                    break
    return patches


'''
Update patches
'''
acpi = path.Root('ACPI')
patches = get_patches(acpi)
if isclover:  # clover
    for patch in patches:
        patch['Disabled'] = False
    config['ACPI']['DSDT']['Patches'] = patches
else:
    for patch in patches:
        patch['Enabled'] = True
    config['ACPI']['Patch'] = patches

print('Patches updated')

for aml in path.Root('ACPI').glob('*.aml'):
    path.rm(aml)

# compile .dsl
print(terminal.PREFIX, 'Compiling dsl files to aml')
iasl = terminal.executable(path.Root('Tools', 'iasl'))
os.system('{} -oa {}'.format(iasl, path.Root('ACPI', '*.dsl')))
print()

'''
Update SSDTs, Kexts and Drivers info for OpenCore
'''

if isoc:
    # SSDT
    ssdts = []
    for aml in path.Root('ACPI').glob('*.aml'):
        ssdts.append({
            'Enabled': True,
            'Path': aml.name
        })
    config['ACPI']['Add'] = ssdts

    print('SSDTs info updated')

    # Kexts
    kexts = []
    lilu = {}
    applealc = {}
    voodooi2c = []

    for kext in path.Root('Kexts').rglob('*.kext'):
        kextinfo = {
            'Enabled': True,
            'BundlePath': kext.relative_to(path.Root('Kexts')).as_posix(),
            'PlistPath': 'Contents/Info.plist'
        }
        if Path(kext, 'Contents', 'MacOS', kext.name[:-5]).exists():
            kextinfo['ExecutablePath'] = '/'.join((
                'Contents', 'MacOS', kext.name[:-5]))
        if kext.name == 'Lilu.kext':
            lilu = kextinfo
        elif kext.name == 'AppleALC.kext':
            applealc = kextinfo
        elif 'VoodooI2C' in kextinfo['BundlePath']:
            priority = 0
            if kextinfo['BundlePath'] == 'VoodooI2C.kext':
                priority = 1
            elif kextinfo['BundlePath'] == 'VoodooI2CHID.kext':
                priority = 2
            voodooi2c.append((priority, kextinfo))
        else:
            kexts.append(kextinfo)
    voodooi2c = [x[1] for x in sorted(voodooi2c, key=lambda x: x[0])]
    config['Kernel']['Add'] = [lilu, applealc] + voodooi2c + kexts

    print('Kexts info updated')

    # UEFI
    drivers = []
    for driver in path.Root('Drivers').glob('*.efi'):
        drivers.append(driver.name)
    config['UEFI']['Drivers'] = drivers

    print('Drivers info updated')


'''
Custom your config
'''
if terminal.Confirm('Customize your config?'):
    scale = terminal.Input('Input UI scale number(1 for FHD, 2 for UHD):')
    keepv = terminal.Confirm('Boot with -v verbose argument?')

    i, v = plist.get(config, oc[1][0])
    i[v] = int(scale)
    i, v = plist.get(config, oc[2][0])
    if keepv and '-v' not in i[v]:
        i[v] += ' -v'
    else:
        i[v] = i[v].replace('-v', '').replace('  ', ' ').strip()

    '''
    Set theme
    '''
    if isclover:
        themepath = path.Root("themes")
        themes = []
        if themepath.exists():
            themes = [theme.name for theme in themepath.iterdir()
                      if theme.is_dir()]
        if themes:
            terminal.Title('Found following theme(s):')
            print(*themes)
            theme = terminal.Input('Please input one to use: ')
            config['GUI']['Theme'] = theme


plist.dump(config, configpath)
print(terminal.PREFIX, configpath, 'updated.')
