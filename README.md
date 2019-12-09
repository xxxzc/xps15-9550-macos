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

> update.py requires python version >= 3.5

### Release

The simplest and most stable way is just using [the latest release](https://github.com/xxxzc/xps15-9550-macos/releases/latest).

Or use `python update.py --release`：

```shell
python update.py --release # get latest CLOVER and OC
python update.py CLOVER --release # get latest CLOVER only
python update.py --release 1911 # get version 1911
```

### Update

You can use `update.py` to update kexts, drivers and bootloader that are list in package.csv.

```sh
python update.py CLOVER/CLOVERX64.efi # update CLOVER bootloader
python update.py OC/Kexts/Lilu.kext # update this kext
python update.py CLOVER # update kexts, drivers and bootloader
```

Run `python update.py --self` to get the latest files from this repo.

### Customize

You can run `python update.py --set k1=v1 k2=v2...` to customize your config.plist.

**SMBIOS**

```sh
python update.py --set sn=xxx mlb=yyy smuuid=zzz
```

Run `sh ./Script/gen_smbios.sh` to generate one and set to config.plist：

```sh
python update.py --set $(sh Script/gen_smbios.sh)
```

**BOOT**

Use `bootarg+xxx` to add/change bootarg, use `bootarg-xxx` to remove a bootarg:

```sh
python update.py --set bootarg--v # remove -v
											 bootarg+darkwake=1 # set darkwake=1
											 uiscale=1 # for FHD display, default to 2(for UHD)
											 timeout=-1 # set boot ui timeout
```

**THEME**

```shell
python update.py CLOVER/themes/xxx # download theme xxx (need git)
python update.py CLOVER --set theme=xxx # set theme to xxx
```

## Issues

You may refer to [wmchris's tutorial](https://github.com/wmchris/DellXPS15-9550-OSX) for the installation guide and solutions to some common issues. 

But note that please create an issue **in this repository** if you encounter any problem when **using this config** (Please don't disturb others). My writing in English is poooooor:(, but I can read :).

### Sleep Wake

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

### FHD Display

```shell
# Font Rendering
defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO
# Boot UI Scaling
python update.py --set uiscale=1
```

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