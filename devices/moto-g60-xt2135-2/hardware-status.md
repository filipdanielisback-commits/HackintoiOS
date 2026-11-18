# XT2135-2 hardware bring-up status

**Status: inventory only. No HackintoiOS hardware feature is currently working or validated.**

Target baseline: Motorola Moto G60 Vision, model XT2135-2, Android 12, build `S2RIS32.32-20-9-9-2-3`, channel `reteu`, device-family name HANOIP.

| Feature | What must be identified | Status |
|---|---|---|
| Power button | Device-tree input node, GPIO/interrupt path, event mapping | Unknown |
| Volume down | Device-tree input node and event mapping | Unknown |
| Volume up | Device-tree input node and event mapping | Unknown |
| Display | Display controller, DSI/panel details, framebuffer handoff | Unknown |
| Touchscreen | Exact controller, bus, interrupt and reset configuration | Unknown |
| Battery | Gauge / fuel-gauge interface and read-only capacity reporting | Unknown |
| Charging | Charger and PMIC status interfaces | Unknown |
| Boot handoff | Existing boot chain, memory map, device-tree handoff and a supported test path | Unknown |
| GPU | Exact Adreno identity, firmware requirements and display integration | Partially identified at family level only; no XNU support |

## Evidence policy

Record source paths, device-tree properties and confidence for each finding. Prefer the exact target firmware and matching HANOIP sources. Do not infer that a feature works because Android supports it or because another Qualcomm phone has a similar component.

## First validation goals

1. Build a source-backed inventory without changing the phone.
2. Define QEMU/host tests for input event translation and display abstractions.
3. Only after a kernel and loader can safely run in an isolated test environment, validate one hardware subsystem at a time.
4. Keep all initial power, battery and storage probes read-only.
