## Laptop Specs

`XPS15-9550`  `i5-6300HQ`  `16GB`  `PM961 512G`  `4K Display`  `1080P Monitor`

`10.15 Beta 19A536g`  `MacBookPro13,3 `

### Not Working 

- Thunderbolt devices
- SD Card (Disabled in BIOS)

## Note

You may refer to [wmchris's tutorial](https://github.com/wmchris/DellXPS15-9550-OSX) for the installation guide and solutions to some common issues. 

But note that please create an issue **in my repository** if you encounter any problem when **using my files or following my tutorial** ( Please don't disturb others ). My writing in English is poooooor:(, but I can read :). 

### Important

Please use **Clover Configurator** or other tool to **generate new SerialNumber, BoardSerialNumber(MLB) and SmUUID**, and replace those values in config.plist.

## Issues

### Disable Hibernation and Fix Sleep Issues

```shell
sudo pmset -a hibernatemode 3
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

#### Font Rendering

```shell
defaults write -g CGFontRenderingFontSmoothingDisabled -bool NO
```

#### Boot UI Scaling

Open `config.plist` and set  `UIScale` to `1`  in `BootGraphics` section.

### Enable NTFS Writing

- If your NTFS driver contains Windows 10 partition, please run `powercfg -h off`  in Windows 10's powershell to disable hibernation first.
- Add `UUID=xxx none ntfs rw,auto,nobrowse` to `/etc/fstab`, **xxx** is the UUID of your NTFS partition.

### Avoid Tap Delay

- Turn off `Enable dragging` or use `three finger drag` to avoid one-finger tap delay.
- Turn off `Smart zoom` to avoid two-finger tap delay.

See [is-it-possible-to-get-rid-of-the-delay-between-right-clicking-and-seeing-the-context-menu](https://apple.stackexchange.com/a/218181)

