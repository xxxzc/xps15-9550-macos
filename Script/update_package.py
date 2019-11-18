from utils.package import Package
from utils import Bunch, path, terminal
from pathlib import Path
from download_theme import download_theme
from modify_kexts import patch_applealc, delete_voodoops2_plugins
import os

'''This script can update packages list in packages.csv
this script accepts one parameter `dst` as destination folder/package

If dst is a package, this script will update this package,
    regardless of whether it exists or not.
e.g. `python update_package.py /path/to/CLOVER/kexts/Other/AppleALC.kext`

If dst is a folder, this script will update all the packages in that folder
    if list in packages.csv
e.g. `python update_package.py /path/to/Kexts` will update kexts
     `python update_package.py /path/to/Clover` will update packages in Clover
'''
fg = terminal.fg

formats = Bunch(checkupdate="({}/{}) {:<46}",
                listupdate="[{}] {:<46} {} -> {}")

'''
Get and filter packages
'''

packages = []
with open(Path(path.root, 'packages.csv'), 'r') as f:
    keys = f.readline()[:-1].lower().split(',')
    packages = [
        Package(**dict(zip(keys, x[:-1].split(',')))) for x in f
    ]

if path.dsttype == 'file':
    for package in packages:
        if path.dst.name in package.items:
            package.folder = path.dst.parent
            packages = [package]
            break
else:
    _packages = []
    dst_lower = str(path.dst).lower()
    for package in packages:
        if path.dsttype == 'folder' and str(package.folder).lower() not in dst_lower:
            continue
        if path.roottype == 'oc':
            if package.items[0] in ('AptioMemoryFix.efi', 'CLOVERX64.efi'):
                continue
        if path.roottype == 'clover':
            if package.items[0] == 'OpenCore.efi':
                continue
            if 'FwRuntimeServices.efi' in package.items:
                package.items.remove('FwRuntimeServices.efi')

        if not terminal.iswin:
            for item in package.items:
                if item.endswith('.exe'):
                    package.items.remove(item)
            if not package.items:
                continue

        package.folder = path.Root(package.folder)
        _packages.append(package)
    packages = _packages

'''
Update CLOVER theme
'''
if path.dsttype == 'clover' or path.dst.name == 'themes':
    themes = path.Root('themes')
    if themes.exists() and terminal.Confirm('Update themes in {}?'.format(themes)):
        for theme in themes.iterdir():
            if theme.is_dir():
                download_theme(themes, theme.name)


if packages and (len(packages) == 1 or terminal.Confirm('Do packages update?')):
    '''
    Check updates
    '''
    terminal.Title('Checking updates...')
    _updates = []
    for i, package in enumerate(packages, 1):
        print(formats.checkupdate.format(
            i, len(packages), package.name), end='\r')

        if package.has_update():
            _updates.append(package)

    packages = _updates

    if not packages:
        terminal.Exit('Everything are up-to-date.')

    '''
    Show updates
    '''
    terminal.Title(len(packages), 'packages to update')
    for i, package in enumerate(packages, 1):
        print(formats.listupdate.format(fg(i, 'idx'),
                                        '/'.join((fg(package.folder,
                                                     'path'), package.name)),
                                        fg(package.local_version, 'lv'),
                                        fg(package.remote_version, 'rv')))
        print(fg(package.remote.url, 'info'))
        if package.remote.changelog:
            print(fg(package.remote.changelog, 'info'))

    '''
    Select updates
    '''
    if len(packages) == 1 and not packages[0].exists():
        pass
    else:
        not_update = terminal.Input(
            'Enter package(s) you don\'t want to update (e.g. 1 3):').split()

        packages = [package for i, package in enumerate(packages, 1)
                    if str(i) not in not_update]

        if not packages:
            terminal.Exit('Nothing to do.')

    '''
    Update
    '''
    terminal.Title('Updating...')
    for package in packages:
        package.update()

'''
Patch AppleALC
and
Delete VoodooPS2Mouse.kext and VoodooPS2Trackpad.kext
'''
print()
for package in packages:
    if package.items[0] == 'AppleALC.kext':
        # if terminal.Confirm('Patch AppleALC for XPS15-9550?'):
        patch_applealc(package.path)

    if package.items[0] == 'VoodooPS2Controller.kext':
        delete_voodoops2_plugins(package.path)


terminal.Title('Done')
