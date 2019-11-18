## Configuration

| Model     | XPS15 9550/MBP13,3         | Version        | 10.15.1 19B88       |
| --------- | :------------------------- | -------------- | ------------------- |
| Processor | Intel Core i5-6300HQ       | Graphics       | HD Graphics 530     |
| Memory    | Micron 2133MHz DDR4 8GB x2 | Disk           | Samsung PM961 512GB |
| Audio     | Realtek ALC298             | WiFi/Bluetooth | Dell Wireless 1830  |
| Display   | Sharp LQ156D1 UHD          | Monitor        | HKC GF40 FHD 144Hz  |

### Not Working 

- Thunderbolt Devices
- SD Card (Disabled in BIOS)

## Installation

### Release

The simplest and most stable way is just using [the latest release](https://github.com/xxxzc/xps15-9550-macos/releases/latest).

### Build

I don't recommend, but if u want, you can clone this repo and run `python deploy.py path`. `path` should be a folder with name CLOVER, OC or OpenCore (case insensitive).

### Scripts

Scripts (including `deploy.py`) require python version ≥  3.5, these scripts may work on Windows, not fully tested yet.

Use `Script/upgrade.py` to replace your current CLOVER/OC with **the latest release** from this repo.

Use `Script/update_package.py` to download and update kexts and drivers.

```sh
python ./Script/update_package.py # update all the packages list in packages.csv
python ./Script/update_package.py ./Kexts # update all the kexts list in packages.csv
python ./Script/update_package.py ./OpenCore.efi # update OpenCore
```

Use `Script/update_config.py` to update config (patches, UI scale and especially for OpenCore to get SSDTs, kexts and drivers info), can also generate SN, MLB and SmUUID.

Use `Script/download_theme.py` to download Clover theme from [Clover Theme Repo](https://sourceforge.net/p/cloverefiboot/themes/ci/master/tree/themes/)

```sh
python ./Script/download_theme.py ./themes/XXX # XXX is the name of theme, e.g. Nightwish
```

## Issues

You may refer to [wmchris's tutorial](https://github.com/wmchris/DellXPS15-9550-OSX) for the installation guide and solutions to some common issues. 

But note that please create an issue **in this repository** if you encounter any problem when **using this config** (Please don't disturb others). My writing in English is poooooor:(, but I can read :).

### SMBIOS

You should fill SN, MLB and SmUUID filelds in config.plist. You can use `Script/update_config.py` to help you input your own values or to generate new one. ([Hackintool](https://www.tonymacx86.com/threads/release-hackintool-v2-8-6.254559/), [MacInfoPkg](https://github.com/acidanthera/MacInfoPkg) and [Clover Configurator](https://mackie100projects.altervista.org/download-clover-configurator/) can do the same job). SmUUID is just a random sequence, run `uuidgen` in Terminal or use online generate tool  to get one.

### Sleep

```shell
sudo pmset -a hibernatemode 0
sudo pmset -a autopoweroff 0
sudo pmset -a standby 0
sudo pmset -a proximitywake 0
sudo pmset -b tcpkeepalive 0 (optional)
```

> `-b` - Battery `-c` - AC Power `-a` - Both

Please uncheck all options (except `Prevent computer from sleeping...`, which is optional) in the `Energy Saver` panel.

### Headphone

@qeeqez found layout-id 30 is good to drive headphone without PluginFix([Overall Audio State](https://github.com/daliansky/XiaoMi-Pro/issues/96)), and it also works for me. If not, you have to install [ALCPlugFix](https://github.com/daliansky/XiaoMi-Pro-Hackintosh/tree/master/ALCPlugFix).

### Non-Retina Display

**Font Rendering**

```shell
defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO
```

**Boot UI Scaling**

Open `config.plist` and set  `UIScale` to `1`.

### NTFS Writing

Add `UUID=xxx none ntfs rw,auto,nobrowse` to `/etc/fstab`, **xxx** is the UUID of your NTFS partition. 

If your NTFS partition has Windows installed, you need to run `powercfg -h off`  in powershell in Windows to disable hibernation.

### Tap Delay

- Turn off `Enable dragging` or use `three finger drag` to avoid one-finger tap delay.
- Turn off `Smart zoom` to avoid two-finger tap delay.

See [is-it-possible-to-get-rid-of-the-delay-between-right-clicking-and-seeing-the-context-menu](https://apple.stackexchange.com/a/218181)

## Credits

- [acidanthera](https://github.com/acidanthera) for providing almost all kexts and drivers
- [alexandred](https://github.com/alexandred) for providing VoodooI2C
- [headkaze](https://github.com/headkaze) for providing the very useful Hackintool and OS-X-BrcmPatchRAM
- [daliansky](https://github.com/daliansky) for providing the awesome hotpatch guide [OC-little](https://github.com/daliansky/OC-little/) and the always up-to-date hackintosh solution [XiaoMi-Pro-Hackintosh](https://github.com/daliansky/XiaoMi-Pro-Hackintosh)
- [RehabMan](https://github.com/RehabMan) for providing OS-X-BrcmPatchRAM and [hotpatch](https://github.com/RehabMan/OS-X-Clover-Laptop-Config/tree/master/hotpatch)
- [knnspeed](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486) for providing well-explained hot patches and USB-C hotplug solution
- [wmchris](https://github.com/wmchris/DellXPS15-9550-OSX/tree/10.15) for providing the installation guide for XPS15
- And all other authors that mentioned or not mentioned in this repo