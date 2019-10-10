## Configuration

| Computer Model                       | XPS15-9550                                        |
| ------------------------------------ | ------------------------------------------------- |
| Processor \| Graphics                | i5-6300HQ \| HD Graphics 530                      |
| Memory \| Disk                       | Micron 2133MHz DDR4 8GB x2 \| Samsung PM961 512GB |
| Audio \| WiFi/Bluetooth              | Realtek ALC298 \| Dell Wireless 1830              |
| Internal Display \| External Monitor | Sharp LQ156D1 UHD \| HKC GF40 FHD 144Hz           |
| macOS Version \| Product Name        | 10.15 Beta 19A582a \| MacBookPro13,3              |

### Not Working 

- Thunderbolt Devices
- SD Card (Disabled in BIOS)

## Note

- **Please generate new SerialNumber, BoardSerialNumber(MLB) and SmUUID and update those fields in config.plist.**

- You may refer to [wmchris's tutorial](https://github.com/wmchris/DellXPS15-9550-OSX) for the installation guide and solutions to some common issues.

  But note that please create an issue **in my repository** if you encounter any problem when **using my files or following my tutorial** ( Please don't disturb others ). My writing in English is poooooor:(, but I can read :). 

## Issues

### Fix Sleep Issues

```shell
sudo pmset -a hibernatemode 0
sudo pmset -a autopoweroff 0
sudo pmset -a standby 0
sudo pmset -b tcpkeepalive 0 (optional)
```

`-b` - Battery, `-c` - AC Power, and `-a` means both.

Please uncheck all options (except `Prevent computer from sleeping...`, which is optional) in the `Energy Saver` panel.

### Headphone

@qeeqez found layout-id 30 is good to drive headphone without PluginFix([Overall Audio State](https://github.com/daliansky/XiaoMi-Pro/issues/96)), and it also works for me. 

If headphone is not working properly, please run following script to get [ALCPlugFix](https://github.com/daliansky/XiaoMi-Pro-Hackintosh/tree/master/ALCPlugFix):

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/daliansky/XiaoMi-Pro-Hackintosh/master/ALCPlugFix/one-key-alcplugfix.sh)"
```

### Non-Retina Display

**Font Rendering**

```shell
defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO
```

**Boot UI Scaling**

Open `config.plist` and set  `UIScale` to `1`  in `BootGraphics` section.

### Enable NTFS Writing

- If your NTFS driver contains Windows 10 partition, please run `powercfg -h off`  in Windows 10's powershell to disable hibernation first.
- Add `UUID=xxx none ntfs rw,auto,nobrowse` to `/etc/fstab`, **xxx** is the UUID of your NTFS partition.

### Avoid Tap Delay

- Turn off `Enable dragging` or use `three finger drag` to avoid one-finger tap delay.
- Turn off `Smart zoom` to avoid two-finger tap delay.

See [is-it-possible-to-get-rid-of-the-delay-between-right-clicking-and-seeing-the-context-menu](https://apple.stackexchange.com/a/218181)

## Kexts

|                             Kext                             | Description           | Version |
| :----------------------------------------------------------: | --------------------- | :------ |
| [AirportBrcmFixup](https://github.com/acidanthera/AirportBrcmFixup) | WiFi driver           | 2.0.3   |
|     [AppleALC](https://github.com/acidanthera/AppleALC)      | Audio driver          | 1.4.2   |
| [BrcmBluetoothInjector+BrcmFirmwareData+BrcmPatchRAM3](https://www.insanelymac.com/forum/topic/339175-brcmpatchram2-for-1015-catalina-broadcom-bluetooth-firmware-upload/?do=findComment&comment=2692922) | Bluetooth driver      | 2.3.0d2 |
| [CPUFriend+CPUFriendDataProvider](https://github.com/acidanthera/CPUFriend) | Better CPU PM         | 1.1.9   |
| [FakePCIID+FakePCIID_Intel_HDMI_Audio](https://bitbucket.org/RehabMan/os-x-fake-pci-id/downloads/) | Prevent audio losting | 1027    |
| [Lilu](https://github.com/acidanthera/Lilu/releases/latest)  | Patching engine       | 1.3.8   |
| [NoTouchID](https://github.com/al3xtjames/NoTouchID/releases) | Disable TouchID       | 1.0.2   |
| [RTCMemoryFixup](https://github.com/acidanthera/RTCMemoryFixup/releases) | Avoid RTC conflicts   | 1.0.4   |
| [VirtualSMC+SMCBatteryManager+SMCProcessor](https://github.com/acidanthera/VirtualSMC) | SMC emulator          | 1.0.8   |
| [USBPorts](https://www.tonymacx86.com/threads/release-intel-fb-patcher-v1-4-5.254559/) | Set USB ports info    | 2.7.6   |
| [VoodooI2C+VoodooI2CHID](https://github.com/alexandred/VoodooI2C) | Touchpad driver       | 2.2     |
| [VoodooPS2Controller](https://github.com/acidanthera/VoodooPS2/releases) | Keyborad driver       | 2.0.4   |
| [WhateverGreen](https://github.com/acidanthera/WhateverGreen) | Patches for GPU       | 1.3.3   |

**About USBPorts.kext**

This kext is generated using [Hackintool v2.7.6](https://www.tonymacx86.com/threads/release-hackintool-v2-7-6.254559/) to replace ` USBInjectAll + SSDT-UIAC.aml`

| Port      | Device          |
| --------- | --------------- |
| HS01/SS01 | Right-side USB3 |
| HS02/SS02 | Left-side USB3  |
| HS04      | Bluetooth       |
| HS09      | Touchscreen     |
| HS12      | Camera          |

## SSDTs

| AML                                                          | Description                                        | Patches/Changes                                              |
| ------------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------ |
| [SSDT-BCKM](https://github.com/daliansky/OC-little/tree/master/保留项目/X02-亮度快捷键补丁) | Brightness control key mapping                     | `Rename method BRT6 to BRTX`<br/>Set `ACOS = 0x80`<br/>`SSDT-PNLF` was included in this file. |
| [SSDT-DGPU](https://github.com/RehabMan/OS-X-Clover-Laptop-Config/blob/master/hotpatch/SSDT-DDGPU.dsl) | Disable dGPU on bootup and wake                    | `Rename method _PTS to ZPTS`<br/>`Rename method _WAK to ZWAK`<br/>`SSDT-PTSWAK` was included in this file. |
| [SSDT-EC](https://github.com/daliansky/OC-little/tree/master/03-%E4%BB%BF%E5%86%92EC) | Add EC Device to load USB power manager            |                                                              |
| [SSDT-GPRW](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486/) | Fix instant wake                                   | `Rename method GPRW to YPRW`                                 |
| [SSDT-PCI0](https://github.com/daliansky/OC-little/tree/master/08-添加丢失的部件) | Add various missing devices in PCI0, not necessary | SSDT-MCHC, SSDT-DMAC, SSDT-HPET and SSDT-SBUS were merged into this file |
| [SSDT-PLUG](https://github.com/daliansky/OC-little/tree/master/02-%E6%B3%A8%E5%85%A5X86) | Inject `plugin-type=1`                             |                                                              |
| [SSDT-TPXX](https://github.com/daliansky/OC-little/tree/master/09-OCI2C-TPXX%E8%A1%A5%E4%B8%81%E6%96%B9%E6%B3%95) | Add TPXX device to replace TPD1(Touchpad)          | `Change GPI0._STA to XSTA`<br/>Add GPI0 method to make this work |
| [SSDT-TYPC](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486/) | Type-C hotplug                                     | `Rename RP15.PXSX._RMV to XRMV`<br/>`SSDT-YTBT` was included in this file |

## Credits

- [acidanthera](https://github.com/acidanthera) for providing almost all kexts and drivers
- [alexandred](https://github.com/alexandred) for providing VoodooI2C
- [headkaze](https://github.com/headkaze) for providing the very useful Hackintool and OS-X-BrcmPatchRAM
- [daliansky](https://github.com/daliansky) for providing the awesome hotpatch guide [OC-little](https://github.com/daliansky/OC-little/) and the always up-to-date hackintosh solution [XiaoMi-Pro-Hackintosh](https://github.com/daliansky/XiaoMi-Pro-Hackintosh)
- [RehabMan](https://github.com/RehabMan) for providing OS-X-BrcmPatchRAM and [hotpatch](https://github.com/RehabMan/OS-X-Clover-Laptop-Config/tree/master/hotpatch)
- [knnspeed](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486) for providing well-explained hot patches and USB-C hotplug solution
- [wmchris](https://github.com/wmchris/DellXPS15-9550-OSX/tree/10.15) for providing the installation guide for XPS15
- And all other authors that mentioned or not mentioned in this repo