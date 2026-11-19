# Audio drivers

Target: Moto G60 XT2135-2 (HANOIP).

This directory is reserved for original XNU-facing audio support: codec/DSP discovery, audio routing, playback/capture interfaces, and power dependencies.

Current status: research required. The exact audio codec, DSP firmware requirements, transport, clocks, regulators, and board routing are not yet verified. No audio driver or firmware is included.

Implementation gate: identify the exact audio components and trace their board connections from authoritative HANOIP sources before defining register access or initialization.
