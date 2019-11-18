from Script.utils import path
from pathlib import Path
import os

'''Deploy to CLOVER or OC(OpenCore)
'''
print('Deploying to', path.root)

path.rm(path.Root('ACPI'))

for f in Path(__file__).parent.iterdir():
    if f.name in ('README.md', 'Changelog.md', 'deploy.py'):
        continue
    if f.name.startswith('.'):
        continue
    path.cp(f, path.Root(f.name))


path.mv(path.Root('Plist', path.roottype + '.plist'), path.Root('config.plist'))
path.rm(path.Root('Plist'))

os.system('python {}'.format(path.Root('Script', 'update_package.py')))
print()
os.system('python {}'.format(path.Root('Script', 'update_config.py')))
print()

if path.roottype == 'clover':
    os.system('python {} {}'.format(
        path.Root('Script', 'download_theme.py'), path.Root('themes', 'Nightwish')))

print('Deployed.')
