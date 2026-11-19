# HackintoiOS language policy

HackintoiOS uses languages according to the layer being implemented. HakiOS is an architectural reference; its device-specific code and assumptions are not copied.

| Language | Intended use | Current status |
|---|---|---|
| C | XNU kernel code, low-level platform code, hardware drivers, boot interfaces and portable testable logic | Primary implementation language |
| C++ | IOKit-oriented components and carefully bounded graphics/system abstractions where C++ is appropriate | Supported; use conservative, explicit interfaces |
| Objective-C | Future user-space APIs and application-facing components when a real Objective-C runtime/framework environment is available | Reserved; not a kernel requirement |
| Python 3 | Source audits, metadata tools, generators and host-side tests | Build and research tooling |
| Bash | Reproducible host setup and build orchestration | Build tooling |
| Make | Upstream XNU and native project build orchestration | Build tooling |

## Rules

1. Keep kernel and early-boot code in C unless a specific upstream XNU subsystem requires another language.
2. Use C++ only where object-oriented interfaces provide a concrete benefit. Keep C ABI boundaries explicit when C and C++ interact.
3. Do not introduce Objective-C into XNU or hardware drivers merely to match the language list. Objective-C user-space work depends on a compatible runtime and frameworks; Linux CI syntax checks do not provide those.
4. Do not assume Apple's private frameworks, UIKit, Metal, or SDKs are available.
5. Prefer portable host tests for pure logic. A passing host test is not evidence of hardware operation.
6. Keep third-party source, generated files, licenses and provenance documented. Do not copy HakiOS implementation code.
7. Add compiler warnings and treat relevant warnings as errors in project-owned code.

## Current compiler baseline

- C: C11.
- C++: C++17.
- Objective-C: syntax-only smoke check where Clang supports it; no Foundation link or runtime claim.
- Python: Python 3.
- Shell: Bash with bash -n validation.

The C and C++ compiler checks run on Linux CI. Objective-C is checked for syntax only and is not linked or executed. A future macOS workflow may be needed when actual Foundation-based user-space development begins.
