from pathlib import Path
from sys import argv
from shutil import rmtree, copy2, copytree, move
from datetime import datetime
from os import utime
from time import mktime
import zipfile

# __file__ in ./Script/utils/path.py, src = '.'
src = Path(__file__).absolute().parent.parent.parent
dst = Path(argv[1]).expanduser().absolute() if len(argv) > 1 else src
root = Path(dst)
while root.parent != root and root.name.lower() not in ('clover', 'oc', 'opencore', 'xps15-9550-macos'):
    root = root.parent
roottype = 'clover' if root.name.lower() == 'clover' else 'oc'

_redirects = {
    'clover': {
        'ACPI': Path('ACPI', 'patched'), 'Kexts': Path('kexts', 'Other'),
        'Drivers': Path('drivers', 'UEFI'), 'Bootloader': '',
        'Tools': Path('tools'), 'themes': 'themes'
    },
    'oc': {
        'ACPI': 'ACPI', 'Kexts': 'Kexts', 'Bootloader': '',
        'Drivers': 'Drivers', 'Tools': 'Tools'
    }
}
redirect = _redirects['clover'] if roottype == 'clover' else _redirects['oc']


def rd(folder):
    return redirect.get(folder, folder)


def Root(*args):
    if args:
        return Path(root, rd(args[0]), *args[1:])
    return Path(dst, *args)


def _get_type(d):
    d = Path(d)
    if d.name.lower() == 'clover':
        return 'clover'

    if d.name.lower() in ('oc', 'opencore', 'xps15-9550-macos'):
        return 'oc'

    if d.is_file() or d.name.endswith('.kext'):
        return 'file'

    for r in redirect.keys():
        rdr = Root(rd(r)).absolute()
        d = d.absolute()
        if str(rdr) == str(d.parent.absolute()):
            return 'file'
        if str(rdr) == str(d.absolute()) or str(rdr.parent) == str(d):
            return 'folder'

    return 'folder'


dsttype = _get_type(dst)


def Src(*args):
    return Path(src, *args)


def Dst(*args):
    if args:
        return Path(dst, rd(args[0]), *args[1:])
    return Path(dst, *args)


def rm(p):
    '''Remove file or directory
    '''
    p = Path(p)
    if not p.exists():
        return
    if p.is_file():
        p.unlink()
    elif p.is_dir():
        rmtree(p)


def cp(s, d):
    '''Copy file or directory from src to dst
    '''
    s, d = Path(s), Path(d)
    if not s.exists() or (d.exists() and s.samefile(d)):
        return
    if s.is_file():
        copy2(s, d)
    if s.is_dir():
        copytree(s, d)


def find(p, files):
    '''Find file or folder in files recursively
    '''
    results = []
    if not files:
        return []
    files = set(files)
    for path in Path(p).iterdir():
        if path.name in files:
            results.append(path)
            files.remove(path.name)
        elif path.is_dir():
            results += find(path, files)
    return results


def mv(s, d):
    '''Move file or directory from src to dst
    '''
    rm(d)
    move(s, d)


def st(p, dt: datetime):
    '''Set path creation time to dt
    '''
    t = mktime(dt.timetuple())
    utime(str(p), (t, t))


def unzip(s, d):
    # https://stackoverflow.com/questions/9813243/extract-files-from-zip-file-and-retain-mod-date
    z = zipfile.ZipFile(s, 'r')
    for info in z.infolist():
        z.extract(info, d)
        st(Path(d, info.filename), datetime(*info.date_time))
