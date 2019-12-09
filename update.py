import argparse
from pathlib import Path
import plistlib
from os.path import join
from os import system as sh
from datetime import datetime, date
from base64 import b64decode
from subprocess import check_output
from urllib.request import urlopen, Request, urlretrieve
import json
import re

root = Path(__file__).absolute().parent

def R(*args):
    return Path(root, args[0], *args[1:])

tmp = R('tmp') # cache downloaded files
sh('rm -rf {}'.format(tmp))
tmp.mkdir()

'''
Arguments
'''
parser = argparse.ArgumentParser(description='''
Update(download if not exist) kexts, drivers, bootloaders,
    patches, themes and config.''', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('p', default=root, metavar='PATH/PACKAGE/CONFIG', nargs='?',
                    help='update/download package or packages in this path, e.g. Kexts/ config.plist OpenCore.efi themes/NightWish')
parser.add_argument('--force', default=False,
                    action='store_true',
                    help='force to update without prompt')
parser.add_argument('--release', nargs='?', const='latest',
                    help='replace all the things with https://github.com/xxxzc/xps15-9550-macos/releases')
parser.add_argument('--config', metavar='path/to/config.plist',
                    help='update config from another config')
parser.add_argument('--set', nargs='*', metavar='k=v',
                    help='update config.plist with `k=v` pairs')
parser.add_argument('--self', default=False, action='store_true',
    help='update from https://github.com/xxxzc/xps15-9550-macos/archive/master.zip')

args = parser.parse_args()

path = Path(args.p).absolute()
clover = R('CLOVER')
oc = R('OC')

iasl = R('Tool', 'iasl')

folders = []
if path.name == root.name or path.name in ('ACPI'):
    folders = [clover, oc]
    if not clover.exists():
        folders.remove(clover)
    if not oc.exists():
        folders.remove(oc)
    if not folders:
        exit()
if clover.name == path.name or clover in path.parents:
    folders = [clover]
    if not clover.exists() and not args.release:
        print('Please run `python update.py CLOVER --release` to get CLOVER configuration.')
        exit(1)
if oc.name == path.name or oc in path.parents:
    folders = [oc]
    if not oc.exists() and not args.release:
        print('Please run `python update.py OC --release` to get OpenCore configuration.')
        exit(1)


mappers = dict(CLOVER={
        'ACPI': join('ACPI', 'patched'),
        'Kexts': join('kexts', 'Other'),
        'Drivers': join('drivers', 'UEFI')
    }, OC={})

def c(text, color):
    # colored output https://stackoverflow.com/a/56774969
    return "\33[38;5;{}m{}\33[0m".format(color, text)


PREFIX = c('::', 75)
ARROW = c('==>', 40)

def Title(*args):
    print(PREFIX, *args)

def Prompt(msg: str):
    if args.force:
        return ''
    return input(ARROW + ' ' + msg)


def Confirm(msg: str) -> bool:
    if args.force:
        return True
    r = Prompt(msg + '?(Y/n)')
    return r != 'n'

def Done(msg: str='Done'):
    print(msg)
    exit()

def shout(cmd):
    return check_output(cmd, shell=True, encoding='utf-8').strip()


class Plist:
    clover_keywords = dict(
        sn='SMBIOS>SerialNumber',
        mlb='SMBIOS>BoardSerialNumber',
        smuuid='SMBIOS>SmUUID',
        uiscale='BootGraphics>UIScale',
        theme='GUI>Theme',
        bootarg='Boot>Arguments',
        timeout='Boot>Timeout',
        defaultvolume='Boot>DefaultVolume',
        layoutid='Devices>Properties>PciRoot(0x0)/Pci(0x1f,0x3)>layout-id'
    )
    oc_keywords = dict(
        sn='PlatformInfo>Generic>SystemSerialNumber',
        mlb='PlatformInfo>Generic>MLB',
        smuuid='PlatformInfo>Generic>SystemUUID',
        uiscale='NVRAM>Add>4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14>UIScale',
        bootarg='NVRAM>Add>7C436110-AB2A-4BBB-A880-FE41995C9F82>boot-args',
        timeout='Misc>Boot>Timeout',
        layoutid='DeviceProperties>Add>PciRoot(0x0)/Pci(0x1f,0x3)>layout-id'
    )
    mapper = [
        ('DeviceProperties/Add', 'Devices/Properties'),
        ('NVRAM/Add/4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14/UIScale',
            'BootGraphics/UIScale'),
        ('NVRAM/Add/7C436110-AB2A-4BBB-A880-FE41995C9F82/boot-args', 'Boot/Arguments')
    ]

    def __init__(self, file):
        self.file = Path(file).absolute()
        self.plist = self.load()
        self.type = 'clover' if 'Boot' in self.plist else 'oc'
        if self.type == 'oc':
            self.keywords = self.oc_keywords
        else:
            self.keywords = self.clover_keywords
            self.mapper = [(k2, k1) for (k1, k2) in self.mapper]

    def load(self):
        with open(self.file, 'rb') as f:
            return plistlib.load(f)

    def save(self):
        with open(self.file, 'wb') as f:
            plistlib.dump(self.plist, f)

    def keyword(self, key):
        return self.keywords.get(key, key)

    @staticmethod
    def data(b64str):
        return b64decode(b64str)

    def get(self, key, value=False):
        key = self.keyword(key)
        ks = key.split('>')
        item = self.plist
        for k in ks[:-1]:
            item = item[k]
        return item[ks[-1]] if value else (item, ks[-1])

    def set(self, key, value):
        item, key = self.get(key)
        if type(item[key]) is bytes:
            if type(value) is not bytes:
                value = Plist.data(value)
        else:
            value = type(item[key])(value)
        item[key] = value

    def copy(self, another):
        if self.type == another.type:
            Title('Replace everything from',
                  another.file, '\nExcept:')
            for key in self.keywords.values():
                value = self.get(key, True)
                another.set(key, value)
                print('{}={}'.format(key, value))
            self.plist = another.plist
        else:
            Title('Replace following fields from', another.file)
            for k1, k2 in self.mapper:
                i1, k1 = self.get(k1)
                value = another.get(k2)
                print('Set {} to {}'.format(k1, value))
                i1[k1] = value

remote_infos = dict() # cache remote info

class Package:
    # access only, 5000/hr
    GITHUB_TOKEN = 'NWFhNjIyNzc0ZDM2NzU5NjM3NTE2ZDg3MzdhOTUyOThkNThmOTQ2Mw=='

    def __init__(self, **kargs):
        self.__dict__.update(kargs)
        if type(self.items) is str:
            self.items = self.items.split('+')
        self.name = self.items[0] if len(
            self.items) == 1 else self.url.split('/')[-1]
        self.changelog = ''

    def check_update(self):
        # get local info
        lurl, lver, ldat = None, '', None
        if all(Path(self.folder, i).exists() for i in self.items):
            lurl = Path(self.folder, self.items[0])
            ldat = date.fromtimestamp(get_timestamp(lurl))
            if lurl.name.endswith('.kext'):
                lver = shout(
                    "grep -A1 -m 2 'CFBundleShortVersionString' " + str(Path(lurl, 'Contents', 'Info.plist')) + " | awk -F '[<,>]' 'NR>1{print $3}'")
        self.__dict__.update(dict(lver=lver, ldat=ldat))

        # get remote info
        rurl, rver, rdat = self.url, self.version, date.today()

        if self.items[0] in remote_infos:
            rurl, rver, rdat = remote_infos[self.items[0]]
        elif 'github' in self.url or 'bitbucket' in self.url:
            domain, user, repo = rurl.split('/')[-3:]
            isgithub = 'github' in domain
            if isgithub:
                req = Request('https://api.github.com/repos/{}/{}/releases/{}'.format(
                    user, repo, 'tags/' + rver if rver != 'latest' else rver),
                    headers={'Authorization': 'token {}'.format(
                        b64decode(self.GITHUB_TOKEN).decode('utf8'))})
            else:
                req = 'https://api.bitbucket.org/2.0/repositories/{}/{}/downloads'.format(
                    user, repo)
            info = json.loads(urlopen(req).read())
            for asset in info['assets' if isgithub else 'values']:
                if re.match(self.pattern, asset['name'], re.I):
                    if isgithub:
                        rurl = asset['browser_download_url']
                        rver = info['tag_name']
                        rdat = date.fromisoformat(info['published_at'][:10])
                        self.changelog = info['body']
                    else:
                        adat = asset['created_on'][:10]
                        if rver in ('latest', adat):
                            rurl = asset['links']['self']['href']
                            rdat = date.fromisoformat(adat)
                    break
        self.__dict__.update(dict(rurl=rurl, rver=rver, rdat=rdat))

        remote_infos[self.items[0]] = (rurl, rver, rdat)

        if not ldat:
            return True
        return lver != rver and abs((rdat - ldat).days) > 1

    def update(self):
        def hook(count, block, total):
            percent, width = min(count * block / total, 1), 25
            length = int(percent * width)
            print("{:<32} {:>8.1f}K [{}{}] {:.0%}".format(
                self.name, total / 1024, '#' * length, ' ' *
                (width - length), percent), end='\r' if percent < 1 else '\n')

        tmpfile = self.rurl.split('/')[-1]  # with ext
        filename = tmpfile.split('.')[0]
        tmpfolder = tmp.joinpath(filename)
        tmpfolder.mkdir(exist_ok=True)
        tmpfile = tmpfolder.joinpath(tmpfile)
        if not tmpfile.exists():
            tmpfile, message = urlretrieve(
                self.rurl, tmpfile, reporthook=hook
            )
            if self.rurl.endswith('.zip'):
                sh('unzip -qq -o {} -d {}'.format(tmpfile, tmpfolder))

        self.folder.mkdir(exist_ok=True, parents=True)
        for item in self.items:
            itempath = self.folder.joinpath(item)
            sh('rm -rf {}'.format(itempath))
            sh(' '.join((
                'find', str(tmpfolder), '-name', item, '-type', 'd' if item.endswith('.kext') or item in ('OC', 'CLOVER') else 'f',
                "| xargs -I '{}'",
                'cp -r {}', str(self.folder))))


def set_config(configfile: Path, kvs: list):
    '''Update config.plist with key=value pairs
    e.g. 
    'uiscale=1' for FHD display
    'theme=Nightwish' to set Clover theme
    'bootarg--v' to remove -v in bootarg
    'bootarg+darkwake=1' to set darkwake to 1
    '''
    if not configfile.exists() or not configfile.name.endswith('.plist'):
        return False
    
    Title('Setting', configfile)

    config = Plist(configfile)
    # process bootargs
    bootargs = []
    for kv in kvs:
        if kv.startswith('bootarg'):
            bootargs.append(kv)
        else:
            k, v = kv.split('=', 1)
            if k not in config.keywords:
                print(k, 'field not found.')
                continue
            config.set(k, v)
            print('Set', config.keyword(k), 'to', v)

    if bootargs:
        boot, key = config.get('bootarg')
        argdict = dict((ba.split('=')[0], ba) for ba in boot[key].split())
        for ba in bootargs:
            arg = ba[8:].split('=')[0]
            if ba[7] == '-':
                argdict.pop(arg, 0)
            else:
                argdict[arg] = ba[8:]
        boot[key] = ' '.join(argdict.values())
        print('Boot Args:', boot[key])

    config.save()
    return True


def download_theme(theme: Path):
    if not theme.exists() or Confirm('Theme {} exists, do you want to update it'.format(theme.name)):
        Title('Downloading theme', theme.name)
        sh('cd {} && git archive --remote=git://git.code.sf.net/p/cloverefiboot/themes HEAD themes/{} | tar -x -v'.format(
            theme.parent.parent, theme.name))
        Title('Theme', theme.name, 'downloaded into', theme.parent)
        print()


def update_themes(themes):
    if themes.exists():
        [download_theme(theme) for theme in Path(themes).iterdir()
         if theme.is_dir()]
    else:
        themes.mkdir()
        download_theme(Path(themes, 'Nightwish'))


def get_choices(choice: str) -> set:
    choices = set()
    for c in choice.split(' '):
        c = c.split('-')
        if len(c) == 1:
            if c[0].isdigit():
                choices.add(int(c[0]))
        else:
            choices.update(range(
                int(c[0]), int(c[1]) + 1))
    return choices


def update_packages(packages):
    '''Updating packages
    '''
    Title('Checking updates...')
    updates = []
    for i, package in enumerate(packages, 1):
        print('({}/{}) {:<46}'.format(
            i, len(packages), package.name), end='\r')
        if package.check_update():
            updates.append(package)
    packages = updates
    if not packages:
        print('Everything is up-to-date')
        return []
    '''
    Show updates
    '''
    def ver_dat(ver, dat):
        if not dat:
            return 'NotInstalled'
        v = str(dat).replace('-', '')
        if ver not in ('', 'latest'):
            v += '({})'.format(ver)
        return v

    Title(len(packages), 'packages to update')
    for i, p in enumerate(packages, 1):
        print('[{}] {:<46} {} -> {}'.format(
            c(i, 172), '/'.join((c(p.folder, 39), p.name)),
            c(ver_dat(p.lver, p.ldat), 204), c(ver_dat(p.rver, p.rdat), 70)))
        print(c(p.rurl, 245))
        print(c(p.changelog.strip(), 245))

    if not args.force:
        notupdate = Prompt(
            'Enter package(s) number you don\'t want to update (e.g. 1 3 4-7):')
        notupdate = get_choices(notupdate)
        packages = [p for i, p in enumerate(
            packages, 1) if i not in notupdate]

    if not packages:
        print('Nothing to do')
        return []

    Title('Updating...')
    [p.update() for p in packages]
    print()
    return packages


def patching(packages):
    '''
    Patch AppleALC for XPS15-9550 and
    Delete VoodooPS2Mouse.kext and VoodooPS2Trackpad.kext
    '''
    for package in packages:
        if 'AppleALC.kext' in package.items:  # XPS15 only
            plist = Plist(Path(package.folder, 'AppleALC.kext',
                               'Contents', 'Info.plist'))
            plist.plist['IOKitPersonalities']['HDA Hardware Config Resource']['HDAConfigDefault'] = [
                dict(AFGLowPowerState=Plist.data('AwAAAA=='),
                     Codec='Constanta - Realtek ALC298 for Xiaomi Mi Notebook Air 13.3 Fingerprint 2018',
                     CodecID=283902616, FuncGroup=1, LayoutID=30, WakeVerbReinit=True,
                     ConfigData=Plist.data(
                         'ASccMAEnHQABJx6gAScfkAF3HEABdx0AAXceFwF3H5ABdwwCAYcccAGHHRABhx6BAYcfAAIXHCACFx0QAhceIQIXHwA='),
                     WakeConfigData=Plist.data('AYcHIg=='))
            ]
            plist.save()
            Title('AppleALC.kext is patched')

        if package.items[0] == 'VoodooPS2Controller.kext':
            for kext in ('VoodooPS2Mouse.kext', 'VoodooPS2Trackpad.kext'):
                sh('rm -rf {}*'.format(Path(package.folder, package.items[0],
                                            'Contents', 'PlugIns', kext)))
            Title('VoodooPS2Mouse.kext and VoodooPS2Trackpad.kext are deleted')


def replace_with_release(folder, version='latest'):
    # backup your config
    originconfig = folder.joinpath('config.plist')
    backupconfig = R(folder.name + '.plist')
    originthemes = folder.joinpath('themes')
    backupthemes = R('themes')
    if originconfig.exists():
        sh('mv {} {}'.format(originconfig, backupconfig))
    if originthemes.exists():
        sh('mv {} {}'.format(originthemes, backupthemes))

    sh('rm -rf {}'.format(folder))
    if update_packages([Package(
            items=folder.name, folder=root,
            url='https://github.com/xxxzc/xps15-9550-macos',
            description=folder.name + ' Configuration for XPS15-9550',
            version=version, pattern='.*-' + folder.name)]):
        if backupconfig.exists():
            originconfig = Plist(originconfig)
            Plist(backupconfig).copy(originconfig)
            originconfig.save()
        if backupthemes.exists():
            sh('rm -rf {}'.format(originthemes))
            sh('mv {} {}'.format(backupthemes, originthemes))

    sh('rm -f {}'.format(backupconfig))
    sh('rm -f {}'.format(backupthemes))


def get_timestamp(p, f='B'):
    # 'm' is modified time, 'B' is birth time 
    return int(shout('stat -f%{} {}'.format(f, p)))

def compile_ssdts(folder: Path):
    # compile if .aml not exist
    dsls = []
    for dsl in folder.rglob('*.dsl'):
        aml = Path(dsl.parent, dsl.name.replace('.dsl', '.aml'))
        if not aml.exists():
            dsls.append((dsl, aml))
        else:
            aml_mtime = get_timestamp(aml, 'm')
            dsl_mtime = get_timestamp(dsl, 'm')
            if dsl_mtime > aml_mtime:
                dsls.append((dsl, aml))
    for (dsl, aml) in dsls:
        Title('Compiling {} to aml'.format(dsl))
        sh('{} -oa {}'.format(iasl, dsl))
    return dsls

def update_patches_kexts_drivers(folder: Path):
    '''Updating patches, kexts and drivers info
    in config.plist
    '''
    def get_patches(dsl_folder):
        '''Get patches from dsl files
        // Patch: xxx
        // Find: ABC
        // Replace: DEF
        '''
        patches = []
        results = shout(
            "awk -F : '/^\\/\\/ (Patch|Find|Replace)/{print $1,$2}' OFS='\t' " + str(dsl_folder) + "/*.dsl").split('\n')
        for i in range(0, len(results), 3):
            patch = {}
            for j in range(3):
                k, v = results[i + j].split('\t')
                k, v = k[3:].strip(), v.strip()
                if j == 0:
                    patch['Comment'] = v
                else:
                    patch[k] = Plist.data(v)
            patches.append(patch)
        return patches

    config = Plist(folder.joinpath('config.plist'))

    '''
    Update patches
    '''
    isclover = config.type == 'clover'
    acpi = folder.joinpath(mappers[folder.name].get('ACPI', 'ACPI'))
    if not acpi.exists() or len(list(acpi.iterdir())) < 4:
        acpi.mkdir(exist_ok=True, parents=True)
        sh('cp -r {}/* {}'.format(R('ACPI'), acpi))
    patches = get_patches(acpi)
    if isclover:  # clover
        for patch in patches:
            patch['Disabled'] = False
        config.plist['ACPI']['DSDT']['Patches'] = patches
    else:
        for patch in patches:
            patch['Enabled'] = True
        config.plist['ACPI']['Patch'] = patches

    print('Patches updated')

    if folder.name == 'CLOVER':
        return

    config.plist['ACPI']['Add'] = [dict(Enabled=True, Path=aml.name)
        for aml in folder.joinpath('ACPI').glob('*.aml')]

    kexts = []
    kextpath = folder.joinpath('Kexts')
    for kext in kextpath.rglob('*.kext'):
        kextinfo = {
            'Enabled': True,
            'BundlePath': kext.relative_to(kextpath).as_posix(),
            'PlistPath': 'Contents/Info.plist'
        }
        if Path(kext, 'Contents', 'MacOS', kext.name[:-5]).exists():
            kextinfo['ExecutablePath'] = '/'.join((
                'Contents', 'MacOS', kext.name[:-5]))
        # correct the order of kexts
        priority = 100
        if kext.name == 'Lilu.kext':
            priority = 0
        elif kext.name == 'VirtualSMC.kext':
            priority = 10
        elif kext.name == 'AppleALC.kext':
            priority = 20
        elif 'VoodooI2C' in kextinfo['BundlePath']:
            priority = 30
            if kextinfo['BundlePath'] == 'VoodooI2C.kext':
                priority = 40
            elif kextinfo['BundlePath'] == 'VoodooI2CHID.kext':
                priority = 50
        kexts.append((priority, kextinfo))
    
    config.plist['Kernel']['Add'] = [x[1] for x in sorted(
            kexts, key=lambda x: x[0])]
    print('Kexts info updated')

    config.plist['UEFI']['Drivers'] = [
        driver.name for driver in folder.joinpath('Drivers').glob('*.efi')
    ]
    print('Drivers info updated')

    config.save()
    return

if __name__ == '__main__':
    if not iasl.exists():
        Title('Downloading iasl...')
        sh('curl -LOk https://bitbucket.org/RehabMan/acpica/downloads/iasl.zip')
        sh('unzip iasl.zip iasl -d {} && rm iasl.zip'.format(iasl.parent))
        sh('chmod a+x {}'.format(iasl))

    if args.self:
        sh('curl -LOk https://github.com/xxxzc/xps15-9550-macos/archive/master.zip')
        sh('unzip {}'.format(R('master.zip')))
        master = R('xps15-9550-macos-master')
        for folder in folders:
            config = folder.joinpath('config.plist')
            if config.exists():
                masterconfig = Plist(master.joinpath(folder.name, 'config.plist'))
                config = Plist(config)
                config.copy(masterconfig)
                config.save()
                sh('rm -rf {}'.format(masterconfig.file))
        sh('cp -r {}/* {}'.format(master, root))
        sh('rm -rf {}'.format(R('master.zip')))
        sh('rm -rf {}'.format(master))
        Done()

    isplist = path.name.endswith('.plist')
    if args.set: # set config
        if isplist:
            set_config(path, args.set)
        else:
            for folder in folders:
                set_config(folder.joinpath('config.plist'), args.set)
        Done()

    if args.config: # copy config from src to dst
        if not isplist:
            Done('First argument should be a plist file')
        src = Plist(args.p)
        src.copy(Plist(args.config))
        src.save()
        Done()

    if args.release:
        for folder in folders:
            replace_with_release(folder, args.release)
        Done()

    if path.name == 'themes':
        update_themes(path)
        Done()
    elif path.parent.name == 'themes':
        download_theme(path)
        Done()
    elif clover in folders:
        update_themes(clover.joinpath('themes'))

    lowerpath = str(path).lower()
    packages = []
    
    for folder in folders:
        mapper = mappers[folder.name]
        a, b = ('OC/', 'CLOVER/') if folder.name == 'CLOVER' else ('CLOVER/', 'OC/')
        with open(R('packages.csv'), 'r') as f:
            keys = f.readline()[:-1].lower().split(',')
            for x in f:
                package = Package(**dict(zip(keys, x[:-1].split(','))))
                pf = package.folder

                if pf.startswith(a):
                    continue
                elif 'kext' in lowerpath and 'kext' not in pf.lower():
                    continue
                elif 'driver' in lowerpath and 'driver' not in pf.lower():
                    continue

                if pf.startswith(b):
                    pf = pf[len(b):]
                elif x[0] == '#':
                    pf = pf[1:]

                package.folder = folder.joinpath(mapper.get(pf, pf))

                if path.name in package.items:
                    packages = [package]
                    break

                if x[0] == '#':
                    for item in package.items:
                        sh('rm -rf {}'.format(package.folder.joinpath(item)))
                    continue

                packages.append(package)

    if packages and Confirm('Do packages update'):
        packages = update_packages(packages)
        patching(packages)

    ssdtpath = ''
    if path.name == root.name:
        ssdtpath = R('ACPI')
    elif path.name in ('CLOVER', 'OC'):
        ssdtpath = path.joinpath('ACPI')
    elif path.name in ('ACPI', 'patched'):
        ssdtpath = path
    
    if ssdtpath:
        if compile_ssdts(ssdtpath) and ssdtpath.parent.name == root.name:
            for folder in folders:
                acpi = folder.joinpath(
                    mappers[folder.name].get('ACPI', 'ACPI'))
                acpi.mkdir(exist_ok=True, parents=True)
                sh('cp -r {}/* {}'.format(ssdtpath, acpi))
                print('SSDTs in {} are updated from {}'.format(acpi, ssdtpath))

    for folder in folders:
        update_patches_kexts_drivers(folder)

    sh('rm -rf {}'.format(tmp))
