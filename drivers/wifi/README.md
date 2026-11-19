# HANOIP Wi-Fi driver research

The first milestone is source-backed hardware identification, not a pretend functional driver.

See [HANOIP Wi-Fi hardware research](../../docs/architecture/HANOIP_WIFI_RESEARCH.md) for the pinned Linux/device-tree evidence, confirmed Qualcomm CLD3/ICNSS stack, WLAN reserved memory and SMP2P entry, separate WCN3990 Bluetooth description, and unresolved radio/transport requirements.

**Current state:** Qualcomm CLD3 WLAN module is present in the HANOIP Linux configuration. Exact Wi-Fi silicon, bus transport, firmware contract, radio resources and XNU integration remain unverified. No HANOIP XNU Wi-Fi driver is implemented.

Do not add guessed chipset IDs, register offsets, firmware names, GPIOs, or bus resources. Do not bundle proprietary firmware or calibration data.
