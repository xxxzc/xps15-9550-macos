# run in EFI folder
python ./Scripts/replace_SMBIOS.py FillThis FillThis FillThis

rm -rf ./OC/ACPI
rm -rf ./OC/Kexts

cp -r ./CLOVER/ACPI/patched ./OC/ACPI
cp -r ./CLOVER/kexts/Other ./OC/Kexts

rm -rf ../.Trashes

dot_clean .
