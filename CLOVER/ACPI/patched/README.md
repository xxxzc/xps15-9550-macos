| AML             | Description                | Related Patches                                              |
| --------------- | -------------------------- | ------------------------------------------------------------ |
| **SSDT-BRTC**   | Brightness control keymaps | Rename Method BRT6,2 to BRTX,2<br />Change OSID to XSID      |
| **SSDT-DGPU**   | Disable dGPU               |                                                              |
| SSDT-DMAC       | DMA controller             |                                                              |
| SSDT-HPET       | Disable HPET device        |                                                              |
| **SSDT-I2C**    | I2C Device (Interrupts)    | Change _STA to XSTA<br />Change _CRS to XCRS                 |
| SSDT-MEM2       | Add MEM2 device            |                                                              |
| **SSDT-PMCR**   | Load AppleIntelPCHPMC      |                                                              |
| **SSDT-PTSWAK** | For correct shutdown       | Change Method(\_PTS,1,N) to ZPTS<br />Change Method(\_WAK,1,N) to ZWAK |
| **SSDT-RMCF**   | Define Variables           |                                                              |
| SSDT-SATA       | SATA Controller            | Change SAT0 to SATA                                          |
| SSDT-SBUS       | Add SBUS device            |                                                              |
| **SSDT-TYPC**   | Type-C hot-plug            | Rename _RMV to XRMV                                          |
| **SSDT-UPRW**   | Disable "wake on USB"      | Rename method UPRW to XPRW<br />Rename method GPRW to YPRW   |
| **SSDT-USBX**   | Set USB current            |                                                              |
| **SSDT-XOSI**   | For VoodooI2C              | Change _OSI to XOSI                                          |
| **SSDT-YTBT**   | Fix DSDT recursion issue   | ~~Rename XTBT to YTBT~~                                      |

> **Bold** means necessary

### Credits

[KNNSpeed/guide-dell-xps-15-9560](https://www.tonymacx86.com/threads/guide-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb.224486/), [RehabMan/OS-X-Clover-Laptop-Config](https://github.com/RehabMan/OS-X-Clover-Laptop-Config) and [corenel/XPS9550-macOS](https://github.com/corenel/XPS9550-macOS)

