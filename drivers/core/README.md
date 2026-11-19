# Driver core

This directory will hold device-neutral XNU driver support shared by individual subsystems.

Planned responsibilities:
- common device lifecycle and state conventions;
- resource-descriptor validation;
- bounded logging and error reporting interfaces;
- explicit ownership rules for memory, interrupts, and device resources.

No XNU kernel ABI is defined here yet. Interfaces must be based on the selected XNU source revision and tested independently before hardware drivers depend on them.

Current status: architecture placeholder; no common XNU driver framework is implemented.
