// Type-C hotplug
// Patch: Rename RP15.PXSX._RMV to XRMV
// Find: 5F 52 4D 56 00 A4 00 14 06 5F 50 53 30 00 14 4B 05 5F 50 53 33 00 72 4D 4D 54 42 0B 48 05 60 5B 80 50 58 56 44 00 60 0A 08 5B 81 10 50 58 56 44 03 54 42 32 50 20 50 32 54 42 20 A0 2E 90 93 54 42 54 53 01 93 53 42 4E 52 54 42 55 53 41 44 42 47 0D 73 65 6E 64 69 6E 67 20 53 58 5F 53 54 41 52 54 00 70 0A 1D 50 32 54 42 14 2D 48 50 4D 45 08 A0 26 90 92 93 56 44 49 44 0C
// Replace: 58 52 4D 56 00 A4 00 14 06 5F 50 53 30 00 14 4B 05 5F 50 53 33 00 72 4D 4D 54 42 0B 48 05 60 5B 80 50 58 56 44 00 60 0A 08 5B 81 10 50 58 56 44 03 54 42 32 50 20 50 32 54 42 20 A0 2E 90 93 54 42 54 53 01 93 53 42 4E 52 54 42 55 53 41 44 42 47 0D 73 65 6E 64 69 6E 67 20 53 58 5F 53 54 41 52 54 00 70 0A 1D 50 32 54 42 14 2D 48 50 4D 45 08 A0 26 90 92 93 56 44 49 44 0C
// References:
// [1] https://www.insanelymac.com/forum/topic/324366-dell-xps-15-9560-4k-touch-1tb-ssd-32gb-ram-100-adobergb%E2%80%8B/
// [2] https://www.tonymacx86.com/threads/usb-c-hotplug-questions.211313/
// [3] https://github.com/the-darkvoid/XPS9360-macOS/issues/118

DefinitionBlock ("", "SSDT", 2, "hack", "TYPC", 0x00000000)
{
    External (_SB_.PCI0.RP15.PXSX, DeviceObj)
    External (_SB_.PCI0.RP15.PXSX.XRMV, MethodObj)

    Scope (\_SB.PCI0.RP15.PXSX)
    {
        // key method to make type-c removable
        Method (_RMV, 0, NotSerialized)  // _RMV: Removal Status
        {
            If (_OSI ("Darwin"))
            {
                Return (One)
            }
            Else
            {
                Return (XRMV ())
            }
        }

        // Remove all other methods[3]
    }
}

