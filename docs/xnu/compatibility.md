# XNU / Darwin compatibility research

This is a preliminary research matrix, not a compatibility claim. Unknown means that reliable target-specific evidence has not yet been collected.

| Area | Moto G60 Vision research status | Evidence needed |
| --- | --- | --- |
| CPU / ARM64 | ARM64 target; exact platform mapping requires verification | Vendor platform documentation and upstream XNU target support |
| Interrupt controller / timers | Unknown | Verified hardware description and XNU platform support |
| Device tree / boot interface | Unknown | Documented boot contract and supported platform implementation |
| Memory management | Unknown | SoC memory map and platform-specific initialization requirements |
| Storage | Unknown | Controller identification, driver availability, and filesystem support |
| Display / GPU | Unknown | Display pipeline and GPU driver support; Linux drivers do not imply XNU support |
| Wi-Fi | Linux CLD WLAN source/configuration is being researched separately | Exact wireless chipset, firmware provenance, and an XNU-compatible driver |
| Audio / camera | Unknown | Component IDs, interfaces, and supported drivers |
| Touchscreen / sensors | Unknown | Hardware IDs and supported input/sensor interfaces |
| Power / thermal | Unknown | PMIC, thermal sensors, charging, and power-management support |

## Interpretation

- A component working under Android/Linux does not establish that an XNU driver exists.
- A generic ARM64 kernel build does not establish support for a particular phone.
- Hardware identification and driver availability must be backed by sources specific to XT2135-2 or the verified HANOIP platform.
- Keep Wi-Fi work in the Linux driver research track until there is evidence of an XNU-compatible implementation.

Update this table only when evidence is linked in the research log.
