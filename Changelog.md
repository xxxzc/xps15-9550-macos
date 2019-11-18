# Changelog

Only keep some meaningful changes. Kexts, drivers and Clover/OC will be updated to latest version if not specified.

## [1911](https://github.com/xxxzc/xps15-9550-macos/releases/tag/1911)

- Use AppleALC 1.4.2 rather than 1.4.3 because the later will cause audio distorted after few minutes on battery mode
- Disable TPD0(I2C0) in `SSDT-TPDX` to fix kernel_task high cpu usage. Credit @regae [issue/26](https://github.com/xxxzc/xps15-9550-macos/issues/26#issuecomment-546838295)
- Replace `SSDT-EC` with `ECDV to EC renaming` to not brake battery statistics for laptop according to [Should I have the native EC﻿DV in my ioreg or disable it and add a fake EC ?](https://www.insanelymac.com/forum/topic/338516-opencore-discussion/?page=53&tab=comments#comment-2685513)
- Set `GPEN=1` to activate GPIO in `SSDT-TPDX` to remove `GPI0._STA to XSTA renaming`
- Remove _PTS and _WAK renaming patches, no issue found after a long time of observation

### Repository

- Clean up my repo to only keep readable files
- Add comments to .dsl files
- Write script to download and update kexts and drivers
- Write script to update config
- Write script to upgrade CLOVER/OC

## 1910

- Remove `force to load IOGraphicsFamily` patch, this bug was fixed
- Add `FakePCIID` and `FakePCIID_Intel_HDMI_Audio` to prevent audio losting at boot
- Repalce `BrcmPatchRAM2` with `BrcmPatchRAM3` from [here](https://www.insanelymac.com/forum/topic/339175-brcmpatchram2-for-1015-catalina-broadcom-bluetooth-firmware-upload/?do=findComment&comment=2692922)

## 1909

- Add `SSDT-PTSWAK` back and put it in `SSDT-DGPU` file, since both have the same purpose that is to disable discrete GPU and add `_PTS` and `_WAK` renaming back for `SSDT-PTSWAK` to work

- Add `force to load IOGraphicsFamily` patch to make trackpad work on 10.15 Beta 8(19A558d). See [VoodooI2C/issues/214](https://github.com/alexandred/VoodooI2C/issues/214)

### Audio

- Remove `CodecCommander` and `SSDT-ALCC`, because `AppleALC` has the same function to send `SET_PIN_WIDGET_CONTROL` command to HDA at wake
- Modify `AppleALC`. Change `WakeConfigData` field in `ALC298 with LayoutID 30` to `AYcHIg==`(represent command `0x18 SET_PIN_WIDGET_CONTROL 0x22`)

## 1908

- Add OpenCore

### SSDTs

Thanks @daliansky for the hot patch guide, https://github.com/daliansky/OC-little/, it's awesome.

- Add `SSDT-ALCC` for ALC298 codec command. [SSDT-ALC298.dsl](https://bitbucket.org/RehabMan/os-x-eapd-codec-commander/src/master/SSDT-ALC298.dsl)

- `SSDT-BCKM > SSDT-BRT6 + SSDT-PNLF`

  According to OC configuration, `_OSI to XOSI` patching and `SSDT-XOSI` shoud be avoid, but `SSDT-BRT6` require `OSID` and `_OSI` renaming patch and `SSDT-XOSI`

  After digging DSDT code, I found that `BRT6` (brightness control) method is called only when `ACOS` is large than `0x20` and `ACOS` was initialized based on `_OSI` and was returned by `OSID` method. If we set `ACOS` to `0x80` (the value that was initialized on Windows 2015) directly in root scope, the initialization process will not be excuted and `OSID` method is working properly. In this way, `OSID` and `_OSI` renaming are not needed

- `SSDT-DMAC + SSDT-HPET + SSDT-PMCR + SSDT-SBUS` were merged into `SSDT-PIC0`, these SSDTs are not necessary. [08-添加丢失的部件](https://github.com/daliansky/OC-little/tree/master/08-%E6%B7%BB%E5%8A%A0%E4%B8%A2%E5%A4%B1%E7%9A%84%E9%83%A8%E4%BB%B6)

- Add `SSDT-EC` to load USB power manager and then we can remove `ECDV to EC` patch. See [SSDT-EC.dsl](https://github.com/daliansky/OC-little/blob/master/03-%E4%BB%BF%E5%86%92EC/SSDT-EC.dsl) for more information

- Add `SSDT-PLUG` to inject `plugin-type=1`

- Replace `SSDT-I2C` with `SSDT-TPXX`. Because `SSDT-I2C` need `_OSI to XOSI` renaming to simulate Windows, but this renaming should be avoid. Instead, we can create another I2C Device, named TPXX, with custom `_CRS` method to support I2C GPIO mode. [Instruction Guide](https://github.com/daliansky/OC-little/tree/master/09-OCI2C-TPXX%E8%A1%A5%E4%B8%81%E6%96%B9%E6%B3%95)

  For XPS15, there are two extra steps: `_SB.PCI0.GPI0._STA` should return `0x0F` to activate GPI0 and origin `GPI0._STA` method should be renamed

- Remove `SSDT-RMCF`, because no other SSDTs need variables that defined in this file

- Replace `SSDT-UPRW` with `SSDT-GPRW` to fix instant wake(sleep) issue in AC mode

- `SSDT-TYPC = SSDT-YTBT + SSDT-TYPC`

- Remove `SSDT-XOSI` and related patches

- Remove `SSDT-USBX`, because usb-current limitation is defined in `USBPorts.kext` now

## 1907

- Update `Brcm*` kexts from [headkaze/OS-X-BrcmPatchRAM](https://github.com/headkaze/OS-X-BrcmPatchRAM), which works on 10.15

- Add `SSDT-DGPU` back, which is nessary to disable dGPU

### Audio

- Remove all audio-related items except layout-id in config.plist
- Modify `CodecCommander` to fix distorted audio after wake in battery mode

There are two methods to drive headphone:

1. Layout-id 30 + CodecCommander
2. Avaliable layout-id + CodecCommander + ALCPlugFix(for headphone)

`CodecCommander` can fix distorted audio, technically, sending `SET_PIN_WIDGET_CONTROL` command to HDA, but it cannot detect headphone plug-in event, we need `ALCPlugFix` to detect it and send above command.

## 1906

- Add `CodecCommander` , `SSDT-ALC298`, `FixHDA` to fix distorted audio after sleep

## 1905

- Update `SSDT-BRT6`, `SSDT-HPET` to remove `Rename GFX0 to IGPU`
- Remove `Rename GFX0 to IGPU` and `ig-platform-id`
- Add `enable-dpcd-max-link-rate-fix` for 4K display according to [FAQ.IntelHD.en](https://github.com/acidanthera/WhateverGreen/blob/master/Manual/FAQ.IntelHD.en.md)

## 1903

- Use VoodooI2C from [the-darkvoid/XPS9360-macOS](https://github.com/the-darkvoid/XPS9360-macOS/tree/master/kexts/VoodooI2C.kext)
- Delete Mouse plugin in `VoodooPS2Controller`, which is conflict with [MOS](https://github.com/Caldis/Mos) app
- Add `RTCMemoryFixup`

## 1902

- Delete `CodecCommander`

- Change layout-id to 30 ([Overall Audio State](https://github.com/daliansky/XiaoMi-Pro/issues/96))

- Add `NoTouchID` back

## 1901

Update `AirportBrcmFixup` to `1.1.9` and add `brcmfx-country=#a` boot arg to fix 5GHz WiFi speed, thanks @CyJaySong. [issues#12](https://github.com/xxxzc/xps15-9550-macos/issues/12)

Update `SSDT-RMCF.aml` and `SSDT-PNLF.aml` （from [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config)）

## 1811

- Change USB2.0 to 3 in USBPorts.kext, according to:

  > HSxx ports connected to USB3 ports should be set to USB3

- Delete SSDT-ALS0.aml

## 1810

- Replace `AppleBacklightInjector` with [Rehabman/AppleBacklightFixup](https://github.com/RehabMan/AppleBacklightFixup)

- Update SSDT-Config to SSDT-RMCF（from [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config)）and delete IGPU and Audio related SSDTs

- Replace `SSDT-TB` with `SSDT-TYPC+SSDT-YTBT` to solve USB-C problem

- Replace `SSDT-UIAC+USBInjectAll` with `USBPorts` (using [Hackintool](https://www.tonymacx86.com/threads/release-hackintool-v2-7-6.254559/)):

  | Port      | Device          | Port          | Device         |
  | --------- | --------------- | ------------- | -------------- |
  | HS01/SS01 | Right-side USB3 | HS02/SS02     | Left-side USB3 |
  | HS04      | Bluetooth       | HS09          | Touchscreen    |
  | HS12      | Camera          | ~~UB21/UB31~~ | ~~Type-C~~     |

  > Type-C on XPS15 is not in XHC