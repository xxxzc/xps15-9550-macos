## Kexts

|                             Kext                             | Version |
| :----------------------------------------------------------: | ------- |
| [AirportBrcmFixup](https://github.com/acidanthera/AirportBrcmFixup) | 2.0.3   |
|     [AppleALC](https://github.com/acidanthera/AppleALC)      | 1.4.1   |
| [BrcmBluetoothInjector+BrcmFirmwareData+BrcmPatchRAM2](https://github.com/headkaze/OS-X-BrcmPatchRAM/releases) | 2.2.12  |
| [BT4LEContinuityFixup](https://github.com/acidanthera/BT4LEContinuityFixup) | 1.1.4   |
| [CodecCommander](https://bitbucket.org/RehabMan/os-x-eapd-codec-commander/downloads/) | 1003    |
| [CPUFriend+CPUFriendDataProvider](https://github.com/acidanthera/CPUFriend) | 1.1.9   |
| [Lilu](https://github.com/acidanthera/Lilu/releases/latest)  | 1.3.8   |
| [NoTouchID](https://github.com/al3xtjames/NoTouchID/releases) | 1.0.2   |
| [RTCMemoryFixup](https://github.com/acidanthera/RTCMemoryFixup/releases) | 1.0.4   |
| [VirtualSMC+SMCBatteryManager+SMCProcessor](https://github.com/acidanthera/VirtualSMC) | 1.0.7   |
| [USBPorts](https://www.tonymacx86.com/threads/release-intel-fb-patcher-v1-4-5.254559/) | 2.7.6   |
| [VoodooI2C+VoodooI2CHID](https://github.com/alexandred/VoodooI2C) | 2.2     |
| [VoodooPS2Controller](https://github.com/acidanthera/VoodooPS2/releases) | 2.0.3   |
| [WhateverGreen](https://github.com/acidanthera/WhateverGreen) | 1.3.2   |

#### About USBPorts.kext

This kext is generated using [Hackintool v2.7.6](https://www.tonymacx86.com/threads/release-hackintool-v2-7-6.254559/) to replace ` USBInjectAll + SSDT-UIAC.aml`

| Port      | Device          |
| --------- | --------------- |
| HS01/SS01 | Right-side USB3 |
| HS02/SS02 | Left-side USB3  |
| HS04      | Bluetooth       |
| HS09      | Touchscreen     |
| HS12      | Camera          |

## SSDTs

| AML                                                          | Description                                      | Patches/Changes                                              |
| ------------------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------ |
| [SSDT-ALCC](https://bitbucket.org/RehabMan/os-x-eapd-codec-commander/src/master/SSDT-ALC298.dsl) | ALC298 command to fix distorted audio after wake |                                                              |
| [SSDT-BCKM](https://github.com/daliansky/OC-little/tree/master/保留项目/X02-亮度快捷键补丁) | Brightness control key mapping                   | `Rename method BRT6 to BRTX`<br/>Set `ACOS = 0x80`<br/>`SSDT-PNLF` was included in this file. |
| [SSDT-DGPU](https://github.com/RehabMan/OS-X-Clover-Laptop-Config/blob/master/hotpatch/SSDT-DDGPU.dsl) | Disable dGPU on bootup and on wake               | `Rename method _PTS to ZPTS`<br/>`Rename method _WAK to ZWAK`<br/>`SSDT-PTSWAK` was included in this file. |
| [SSDT-EC](https://github.com/daliansky/OC-little/tree/master/03-%E4%BB%BF%E5%86%92EC) | Add EC Device to load USB power manager          |                                                              |
| [SSDT-GPRW](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486/) | Fix instant wake                                 | `Rename method GPRW to YPRW`                                 |
| [SSDT-PCI0](https://github.com/daliansky/OC-little/tree/master/08-添加丢失的部件) | Add various missing devices, not necessary       | SSDT-MCHC, SSDT-DMAC, SSDT-HPET and SSDT-SBUS were merged into this file |
| [SSDT-PLUG](https://github.com/daliansky/OC-little/tree/master/02-%E6%B3%A8%E5%85%A5X86) | Inject `plugin-type=1`                           |                                                              |
| [SSDT-TPXX](https://github.com/daliansky/OC-little/tree/master/09-OCI2C-TPXX%E8%A1%A5%E4%B8%81%E6%96%B9%E6%B3%95) | Add TPXX device to replace TPD1(Touchpad)        | `Change GPI0._STA to XSTA`<br/>Add GPI0 method to make this work |
| [SSDT-TYPC](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486/) | Type-C hotplug                                   | `Rename RP15.PXSX._RMV to XRMV`<br/>`SSDT-YTBT` was included in this file |

## Credits

- [acidanthera](https://github.com/acidanthera) for providing almost all kexts and drivers
- [alexandred](https://github.com/alexandred) for providing VoodooI2C
- [headkaze](https://github.com/headkaze) for providing the very useful Hackintool and OS-X-BrcmPatchRAM
- [daliansky](https://github.com/daliansky) for providing the awesome hotpatch guide [OC-little](https://github.com/daliansky/OC-little/) and the always up-to-date hackintosh solution [XiaoMi-Pro-Hackintosh](https://github.com/daliansky/XiaoMi-Pro-Hackintosh)
- [RehabMan](https://github.com/RehabMan) for providing CodecCommander, OS-X-BrcmPatchRAM and [hotpatch](https://github.com/RehabMan/OS-X-Clover-Laptop-Config/tree/master/hotpatch)
- [knnspeed](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486) for providing well-explained hot patches and USB-C hotplug solution
- [wmchris](https://github.com/wmchris/DellXPS15-9550-OSX/tree/10.15) for providing the installation guide for XPS15
- And all other authors that mentioned or not mentioned in this repo

