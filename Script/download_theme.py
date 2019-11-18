import os
from utils import terminal, path
from sys import argv
from pathlib import Path

'''Download clover theme
python download_theme.py path/to/themes/theme_name
'''


def download_theme(_path, name):
    _path = Path(_path)
    _path.mkdir(parents=True, exist_ok=True)

    terminal.Title('Downloading theme {}...'.format(name))

    zipfile = Path(_path, name + '.zip')
    os.system('git archive --remote=git://git.code.sf.net/p/cloverefiboot/themes HEAD themes/{} -o {}'.format(name, zipfile))
    path.unzip(zipfile, _path.parent)
    path.rm(zipfile)

    terminal.Title('Theme {} downloaded into {}'.format(
        name, _path))


if __name__ == "__main__":
    download_theme(path.dst.parent, path.dst.name)
