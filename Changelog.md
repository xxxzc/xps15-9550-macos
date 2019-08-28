##  Changelog

### Aug

#### SSDTs

Thanks @daliansky for the hot patch guide, https://github.com/daliansky/OC-little/, it's awesome.

- Add `SSDT-ALCC` for ALC298 codec command. [SSDT-ALC298.dsl](https://bitbucket.org/RehabMan/os-x-eapd-codec-commander/src/master/SSDT-ALC298.dsl)

- `SSDT-BCKM > SSDT-BRT6 + SSDT-PNLF` 

  According to OC configuration, `_OSI to XOSI` patching and `SSDT-XOSI` shoud be avoid, but `SSDT-BRT6` required `OSID` and `_OSI` renaming patch and `SSDT-XOSI`.

  After digging DSDT code, I found that `BRT6` (brightness control) method is called only when `ACOS` is large than `0x20` while `ACOS` was initialized (based on `_OSI` ) and returned by `OSID` method. So we just set `ACOS` to `0x80` to avoid those patches.

-  `SSDT-DMAC + SSDT-HPET + SSDT-PMCR + SSDT-SBUS` were merged into `SSDT-PIC0`, these SSDTs are not necessary. Source: [08-添加丢失的部件](https://github.com/daliansky/OC-little/tree/master/08-%E6%B7%BB%E5%8A%A0%E4%B8%A2%E5%A4%B1%E7%9A%84%E9%83%A8%E4%BB%B6)

- Add `SSDT-EC` to load USB power manager and to remove `ECDV to EC` patch. See [SSDT-EC.dsl](https://github.com/daliansky/OC-little/blob/master/03-%E4%BB%BF%E5%86%92EC/SSDT-EC.dsl) for more information.

- Add `SSDT-PLUG` to inject `plugin-type=1`.

- Replace `SSDT-I2C` with `SSDT-TPXX`. Because `SSDT-I2C` need `_OSI to XOSI` renaming to work, but this renaming should be avoid. Instead, we can create another I2C Device, named TPXX, with custom behavior to support I2C GPIO mode, [Instruction Guide](https://github.com/daliansky/OC-little/tree/master/09-OCI2C-TPXX%E8%A1%A5%E4%B8%81%E6%96%B9%E6%B3%95).

  For XPS15, there are two extra steps:  `_SB.PCI0.GPI0._STA` should return `0x0F` and origin `GPI0._STA` method should be renamed.

- Remove `SSDT-PTSWAK` and related patches, no shutdown/wake issue found.

- Remoe `SSDT-RMCF`, because no other SSDTs need variables that defined in this file.

- Replace `SSDT-UPRW` with `SSDT-GPRW` to fix instant wake(sleep) issue in AC mode.

-  `SSDT-TYPC = SSDT-YTBT + SSDT-TYPC` 

- Remove `SSDT-XOSI` and related patches.

- Remove `SSDT-USBX`, usb current limit can be defined in `USBPorts.kext`.

### Patches

Only keep following four patches, and each patch only change one place (method) in DSDT.

- `BRT6 -> BRTX`

- `GPRW -> YPRW`

- `GPI0._STA -> GPI0.XSTA` 

- `RP15.PXSX._RMV -> XRMV`  

  This patch only change _RMV method in RP15 device, will not affect other RPXX devices.

#### Others

- Update kexts and drivers to latest
- Update Clover to r5058
- Support OpenCore v0.0.4

### July

#### Kext & Driver

- Update kexts to latest
- Update drivers to latest
- Update `Brcm*` kexts from [headkaze/OS-X-BrcmPatchRAM](https://github.com/headkaze/OS-X-BrcmPatchRAM), which works on 10.15

#### Patches

- Add `SSDT-DGPU` back, which is nessary to disable dGPU.

#### Audio

- Remove all audio-related items except layout-id in config.plist
- Modify `CodecCommander` to fix distorted audio after wake in battery mode

There are two methods to drive headphone:

1. Layout-id 30 + CodecCommander
2. Avaliable layout-id + CodecCommander + ALCPlugFix

`CodecCommander` can fix distorted audio, technically, sending `SET_PIN_WIDGET_CONTROL` command to HDA, but it cannot detect headphone plug-in, we need `ALCPlugFix` to detect headphone plug-in event and send above command.

#### Others

Update Clover to r4972

### Jun

Add `CodecCommander` , `SSDT-ALC298`, `FixHDA` to fix distorted audio after sleep

### May

#### Kext & Driver

- Update `AirportBrcmFixup`, `CPUFriend`, `Lilu`, `VirtualSMC`, `VoodooI2C` and `VoodooPS2Controller` to latest
- Update `AppleALC`, which says `Fixed rare random audio init failure on 10.14`, need more test
- Update drivers to latest

#### Patches

- Remove some patches
- Update `SSDT-BRT6`, `SSDT-HPET`
- Use `Add-PNLF` and `SetIntelBacklight + SetIntelMaxBacklight` to replace `SSDT-PNLF`
- Remove `Rename GFX0 to IGPU` and `ig-platform-id`, modify `SSDT-BRT6` and add `enable-dpcd-max-link-rate-fix` according to [FAQ.IntelHD.en](https://github.com/acidanthera/WhateverGreen/blob/master/Manual/FAQ.IntelHD.en.md) 

#### Others

- Update Clover to r4934

- Clean up config file

### Mar

#### Kext

- Update kexts
- Use VoodooI2C from [the-darkvoid/XPS9360-macOS](<https://github.com/the-darkvoid/XPS9360-macOS/tree/master/kexts/VoodooI2C.kext>)
- Delete Mouse plugin in `VoodooPS2Controller`, which is conflict with MOS app
- Add `RTCMemoryFixup`

#### Others

- Replace `SSDT-TYPC+SSDT-YTBT` with `SSDT-THBT`

- Update Clover to r4910

### Feb

#### Audio

2. Delete `CodecCommander` 
2. Change layout-id to 30 ([Overall Audio State](https://github.com/daliansky/XiaoMi-Pro/issues/96))

#### Kext

- Update kexts

- Add `NoTouchID` back

#### Clover

Update Clover to r4871

### Jan

Update `AirportBrcmFixup` to `1.1.9` and add `brcmfx-country=#a` boot arg to fix 5G WiFi speed, thanks @CyJaySong. [issues#12](https://github.com/xxxzc/xps15-9550-macos/issues/12)

#### SSDT

Update `SSDT-RMCF.aml` and `SSDT-PNLF.aml` （from [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config)）

### Nov

- Update kexts

- Change USB2.0 to 3 in USBPorts.kext, according to：

  > HSxx ports connected to USB3 ports should be set to USB3

- Delete SSDT-ALS0.aml

### Oct

- Replace `AppleBacklightInjector` with [Rehabman/AppleBacklightFixup](https://github.com/RehabMan/AppleBacklightFixup) 

- Update Clover to R4697。

- Use Nightwish256 theme。

- Update SSDT-Config to SSDT-RMCF （from [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config)）and delete IGPU and Audio related SSDTs。
- Update kexts

- Replace `SSDT-TB.aml` with `SSDT-TYPC.aml+SSDT-YTBT.aml` to solve USB-C problem

