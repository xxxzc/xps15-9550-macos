from pathlib import Path
from datetime import date, datetime
from os import stat, utime
from shutil import rmtree, move
from urllib import request
from utils import Bunch, path
import json
import time
import re
import zipfile
from base64 import b64decode

# access only, 5000/hr
GITHUB_TOKEN = 'NWFhNjIyNzc0ZDM2NzU5NjM3NTE2ZDg3MzdhOTUyOThkNThmOTQ2Mw=='


class Package:
    def __init__(self, items, folder, url,
                 description='', version='latest', pattern='.*'):
        if type(items) == str:
            items = items.split('+')

        self.items = items
        self.description = description
        self.link = url
        self.folder = folder
        self.local = Bunch(url=None, version=chr(0), date=date(1970, 1, 1))
        self.remote = Bunch(url=url, version=version, date=date.today(),
                            pattern=pattern, changelog='')
        self.checked = False

    def _check_update(self):
        # update local info if exist
        for item in self.items:
            itempath = Path(self.folder, item)
            if itempath.exists():
                self.local.url = itempath
                self.local.date = path.ct(itempath)

                if item.endswith('.kext'):
                    infoplist = Path(itempath, 'Contents', 'Info.plist')
                    self.local.date = path.ct(infoplist)
                    with open(infoplist, 'r') as f:
                        for line in f:
                            if 'CFBundleShortVersionString' in line:
                                break
                        # <string>xxx</string>
                        self.local.version = f.readline().strip()[8:-9]

            else:
                self.local.url = None
                self.local.date = date(1970, 1, 1)
                self.local.version = chr(0)
                break

        # update remote info
        domain, user, repo = self.link.split('/')[-3:]
        version = self.remote.version
        api_server = {
            'github.com': 'https://api.github.com/repos/{}/{}/releases',
            'bitbucket.org': 'https://api.bitbucket.org/2.0/repositories/{}/{}/downloads'
        }

        if 'github' in domain:
            if version != 'latest':
                version = 'tags/' + version
            api = 'https://api.github.com/repos/{}/{}/releases/{}'.format(
                user, repo, version)
            req = request.Request(api, headers={
                'Authorization': 'token {}'.format(b64decode(GITHUB_TOKEN).decode('utf8'))
            })

            info = json.loads(request.urlopen(req).read())

            for asset in info['assets']:
                if re.match(self.remote.pattern, asset['name'], re.I):
                    self.remote.url = asset['browser_download_url']
                    self.remote.version = info['tag_name']
                    self.remote.date = date.fromisoformat(
                        info['published_at'][:10])
                    self.remote.changelog = info['body']
                    break
        elif 'bitbucket' in domain:
            api = 'https://api.bitbucket.org/2.0/repositories/{}/{}/downloads'.format(
                user, repo)

            info = json.loads(request.urlopen(api).read())

            for asset in info['values']:
                if re.match(self.remote.pattern, asset['name'], re.I):
                    asset_date = asset['created_on'][:10]
                    if version == 'latest' or version == asset_date:
                        self.remote.url = asset['links']['self']['href']
                        self.remote.date = date.fromisoformat(asset_date)
                        break

        if not self.remote.date:
            # Get date from remote file
            with request.urlopen(self.remote.url) as response:
                last_modified = response.info()['last-modified']
                self.remote.date = datetime.strptime(last_modified,
                                                     '%a, %d %b %Y %H:%M:%S %Z').date()
        return

    @property
    def path(self):
        # may not exist
        return Path(self.folder, self.items[0])

    def _version(self, info):
        v = str(info.date).replace('-', '')
        if info.version not in (chr(0), 'latest'):
            v += '({})'.format(info.version)
        return v

    @property
    def local_version(self):
        if not self.local.url:
            return 'NotInstalled'
        return self._version(self.local)

    @property
    def remote_version(self):
        return self._version(self.remote)

    @property
    def name(self):
        if len(self.items) > 1:
            return self.link.split('/')[-1]
        return self.items[0]

    def exists(self):
        for item in self.items:
            if not Path(self.folder, item).exists():
                return False
        return True

    def has_update(self):
        if not self.checked:
            self._check_update()
            self.checked = True

        if not self.local.url:
            return True

        return self.local.version != self.remote.version and abs((self.remote.date - self.local.date).days) > 1

    def update(self):
        # wants to print package.name in hook
        def hook(count, block, total):
            percent = min(count * block / total, 1)
            width = 25
            length = int(percent * width)
            print("{:<32} {:>8.1f}K [{}{}] {:.0%}".format(self.name, total / 1024,
                                                          '#' * length,
                                                          ' ' *
                                                          (width - length),
                                                          percent),
                  end='\r' if percent < 1 else '\n')

        tmpfile, message = request.urlretrieve(
            self.remote.url, reporthook=hook)

        Path(self.folder).mkdir(exist_ok=True, parents=True)

        if '.zip' in self.remote.url:
            tmpfolder = Path(tmpfile).parent.joinpath('unzip')
            tmpfolder.mkdir(exist_ok=True, parents=True)
            path.unzip(tmpfile, tmpfolder)
            for f in path.find(tmpfolder, self.items):
                path.cp(f, Path(self.folder, f.name))
            path.rm(tmpfolder)
        else:
            path.st(tmpfile,
                    datetime.strptime(message['last-modified'],
                                      '%a, %d %b %Y %H:%M:%S %Z'))
            path.mv(tmpfile, self.path)

        self.local.url = self.path
