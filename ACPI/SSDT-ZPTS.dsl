// Fix shutdown to restart issue
// Patch: Rename _PTS to ZPTS
// Find: 5F 50 54 53 01
// Replace: 5A 50 54 53 01
// Reference:
// [1] https://github.com/xxxzc/xps15-9550-macos/issues/45
// [2] https://github.com/RehabMan/OS-X-Clover-Laptop-Config/blob/master/hotpatch/SSDT-PTSWAK.dsl

DefinitionBlock ("", "SSDT", 2, "hack", "PTSWAK", 0x00000000)
{
    External (_SB_.PCI0.XHC_.PMEE, FieldUnitObj)
    External (ZPTS, MethodObj)    // 1 Arguments

    Method (_PTS, 1, NotSerialized)  // _PTS: Prepare To Sleep
    {
        ZPTS (Arg0)
        If (_OSI ("Darwin") && (0x05 == Arg0))
        {
            \_SB.PCI0.XHC.PMEE = Zero // [2]
        }
    }
}

