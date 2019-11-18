from utils import plist, path
from pathlib import Path


def patch_applealc(applealc):
    path = Path(applealc, 'Contents', 'Info.plist')
    info = plist.load(path)
    info['IOKitPersonalities']['HDA Hardware Config Resource']['HDAConfigDefault'] = [{
        'AFGLowPowerState': plist.data('AwAAAA=='),
        'Codec': 'Constanta - Realtek ALC298 for Xiaomi Mi Notebook Air 13.3 Fingerprint 2018',
        'CodecID': 283902616,
        'ConfigData': plist.data('ASccMAEnHQABJx6gAScfkAF3HEABdx0AAXceFwF3H5ABdwwCAYcccAGHHRABhx6BAYcfAAIXHCACFx0QAhceIQIXHwA='),
        'FuncGroup': 1,
        'LayoutID': 30,
        'WakeConfigData': plist.data('AYcHIg=='),  # send pinconfig at wake
        'WakeVerbReinit': True
    }]
    plist.dump(info, path)
    print(applealc, 'is patched')
    return


def delete_voodoops2_plugins(voodoops2):
    plugins = Path(voodoops2, 'Contents', 'PlugIns')
    for kext in ('VoodooPS2Mouse.kext', 'VoodooPS2Mouse.kext.dSYM',
                 'VoodooPS2Trackpad.kext', 'VoodooPS2Trackpad.kext.dSYM'):
        path.rm(Path(plugins, kext))

    print('VoodooPS2Mouse.kext and VoodooPS2Trackpad.kext in',
          voodoops2, 'are deleted')


if __name__ == "__main__":
    patch_applealc(path.Root('Kexts', 'AppleALC.kext'))
    delete_voodoops2_plugins(path.Root('Kexts', 'AppleALC.kext'))
