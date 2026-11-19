# Early console

This directory is reserved for a minimal early-boot diagnostic console.

Current status: not implemented for XNU/HANOIP. The Linux reference device tree contains a serial alias, but that alone does not prove the port is enabled or available at the custom loader handoff. Verify the exact UART resources and handoff before writing a driver.
