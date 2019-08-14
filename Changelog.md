##  Changelog

### 8.14

- Update kexts and drivers
- Update Clover to r5045

### 7.7

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

`CodecCommander` can fix distorted audio, technically, sending `SET_PIN_WIDGET_CONTROL` command to HDA. `CodecCommander` can work during boot, upon sleep or at wake, but it cannot detect headphone plug-in. 

For layout-id 30, headphone works properly except wake from sleep in battery mode, `CodecCommander` with custom patch can fix this problem - simply sending a signal at wake. 

But other layout-ids are not so lucky - headphone is distorted inherently, which means fixing is need every time you plug-in a headphone, so we need `ALCPlugFix` to detect headphone plug-in event and send above command.

#### Others

Update Clover to r4972

### 6.1

Add `CodecCommander` , `SSDT-ALC298`, `FixHDA` to fix distorted audio after sleep

### 5.31

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

Update Clover to r4934

Clean up config file

### 5.4

#### Kext

更新 `AppleALC`、`WhateverGreen`、`Lilu`、`VoodooI2C`

#### 其他

更新 Clover 到 4920

修改 config.plist 以尝试减少偶尔发生的 Display Flickering

### 3.31

#### Kext

更新 `AppleALC`、`WhateverGreen`、`Lilu`

使用 [the-darkvoid/XPS9360-macOS](<https://github.com/the-darkvoid/XPS9360-macOS/tree/master/kexts/VoodooI2C.kext>) 的 `VoodooI2C`

删除 `VoodooPS2Controller` 的鼠标插件，会与 MOS 冲突，导致鼠标滚动卡顿

#### 其他

使用 `SSDT-THBT` 代替 `SSDT-TYPC+SSDT-YTBT`

更新 Clover 到 4910

更新 `AptioMemeoryFix`

### 3.7

更新 `Lilu`，增加 `RTCMemoryFixup`

更新 Clover 到 4895

### 2.11

#### Audio

1. 参考 [Overall Audio State](https://github.com/daliansky/XiaoMi-Pro/issues/96) 将 layout-id 改为 30 以解决耳机失真
2. 删除 `CodecCommander` 

现在你可以卸载 `ALC298PluginFix` 看看耳机是否能正常工作。

#### Kext

更新 `Lilu`、`AppleALC` 和 `CPUFriend`

加回 `NoTouchID`，13,3 在安装的时候还是会出现 TouchID 设置

#### SSDT

将 `SSDT-GPRW` 换成 `SSDT-UPRW` （据 [issue#14](https://github.com/xxxzc/xps15-9550-macos/issues/14)）

加回 `SSDT-HPET`和 `SSDT-MEM2` 

#### Clover

更新 Clover 到 4871，更新 drivers

### 1.16

更新 `AirportBrcmFixup` 到 `1.1.9` 并加上 `brcmfx-country=#a` 以解决 WiFi 5G 速度问题，见 [issues#12](https://github.com/xxxzc/xps15-9550-macos/issues/12)，感谢 @CyJaySong 。

### 1.4

#### Kext

更新 `Lilu`、`WhateverGreen`、`AirportBrcmFixup`

更新 `CPUFriend` 和 `CPUFriendDataProvider`。我才发现之前用的 CPUFriend 居然是 `1.1.3`。。难怪需要启动参数才能 enable。现在这些 kext 都默认支持 10.14，不需要 `-lilubetaall` 了。 

删除 `NoTouchID`，因为 MacBookPro 13,3 模型没有 Touch ID，不需要这个 kext。

#### SSDT

更新 `SSDT-RMCF.aml` 和 `SSDT-PNLF.aml` （from [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config)）

#### Theme

更新 Nightwish(256)（from `CloverThemeManager`）

### 12.23

更新 `Lilu`、`AppleALC`、`VirtualSMC`、`WhateverGreen`、`AirportBrcmFixup`

删除 `AppleBacklightFixup`，已经集成到了 WhateverGreen 里

更新 Clover 到 4813，但是 Clover Configurator 里还是显示 4603

修改了一点 `config.plist` 配置

- 删除 Framebuffer Connectors，之前没有这些连不了外接显示器，现在不知道为什么删了还可以，所以删了
- 去掉了 AppleRTC 和 KernelPM，似乎没啥用

### 11.2

更新 Lilu、AppleALC、VirtualSMC、WhateverGreen

修正 USBPorts.kext 里两个 USB2.0 的值为 3，根据如下：

```
HSxx ports connected to USB3 ports should be set to USB3
```

（希望我没有会错意= =）

删除 SSDT-ALS0.aml

### 10.15

使用 [Rehabman/AppleBacklightFixup](https://github.com/RehabMan/AppleBacklightFixup) 代替 `AppleBacklightInjector` 

### 10.10

将 Clover 更新到 Rehabman 版本的 R4697。

尝试修复唤醒无声的问题，还需要多测试。

将主题换成了 Nightwish(256)，默认使用 Nightwish256。

更新了一些 SSDT 和 kexts。

- 将 SSDT-Config 更新为 SSDT-RMCF （from [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config)），并更新一些相关的 SSDT。主要是删除了所有 IGPU 和 Audio 的 Injection。
- 更新 `AirportBrcmFixup` ， `CodecCommander`，  `VoodooPS2Controller` 以及 `BT4LEContiunityFixup`

删除提高 VRAM 的 patching。

另外发现将 `brcmfx-country` 设置成 `CN` 会导致一些 WiFi 连不上。

### 10.4

将 `SSDT-TB.aml` 换为 `SSDT-TYPC.aml+SSDT-YTBT.aml` 以解决 type-c 的连接问题 。

### 10.3

使用 [Intel FB-Patcher v1.4.5](https://www.tonymacx86.com/threads/release-intel-fb-patcher-v1-4-5.254559/) 重新生成 Framebuffer Patching 和 `USBPort.kext`。之前 Patching 的 `ig-platform-id` 是错误的，这应该是导致 4K 屏直接睡死的主要原因。之前用的 `USBPort.kext` 也是错误的。

- 删除了一些无用的 DSDT/SSDT，同时添加了每个 DSDT 的简单描述信息。
- 使用 `USBPort.kext` 替代之前的 `SSDT-XHC.aml`

改用 [wmchris/DellXPS15-9550-OSX](https://github.com/wmchris/DellXPS15-9550-OSX) 中的 `AppleBacklightInjector.kext`和亮度相关的 dsdt。现在最低亮度比之前低了很多。

### 10.2

改用 [corenel/XPS9550-macOS](https://github.com/corenel/XPS9550-macOS) 的 SSDT/DSDT，其他基本保持不变，主要做了如下修改：

- 删除 `SSDT-ALC298a` ，现在是用 `config.plist` 中注入
- 删除 `SSDT-pr.aml`，现在使用 `CPUFriend` 实现
- 替换 `SSDT-XOSI.aml` 以支持 `VoodooI2C`
- 删除 `USBPort.kext` ，他应该是在 `SSDT-XHC.aml` 里实现了 USB 接口注入
- 增加 `SSDT_IGPU_Syspref.aml` 配合 `agdpmod=vit9696` 以实现外接显示器

换用这个的主要原因之前的 USB 接口有问题。

