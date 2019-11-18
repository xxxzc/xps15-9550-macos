import os
from utils import path, terminal
from utils.package import Package

'''Upgrade from https://github.com/xxxzc/xps15-9550-macos/releases/latest
'''

terminal.Title('Checking upgrade...')
_type = path.roottype.upper()
package = Package(items=[_type],
                  folder=path.Root('.'),
                  url='https://github.com/xxxzc/xps15-9550-macos',
                  pattern='.*-{}'.format(_type))

package.has_update()  # update info

print('Version:', package.remote_version, 'Changelog:')
print(package.remote.changelog)

if terminal.Confirm('Do you want to upgrade?'):
    print('Upgrading...')
    package.update()

    for folder in ('ACPI', 'Kexts', 'Drivers'):
        path.rm(path.Root(folder))

    path.mv(path.Root(_type, 'config.plist'),
            path.Root(_type, _type + '.plist'))
    os.system('cp -r {}/* {}'.format(path.Root(_type), path.root))

    os.system('python {} {} {}'.format(
        path.Root('Script', 'update_config.py'),
        path.Root('config.plist'),
        path.Root(_type + '.plist')
    ))
    path.rm(path.Root(_type + '.plist'))
    path.rm(path.Root(_type))
