# Development tools

This directory contains original research, validation, and test utilities.

Conventions:
- Python tools should validate explicit inputs and fail closed on malformed or ambiguous data.
- Shell scripts should use strict error handling and avoid implicit downloads or privileged operations.
- Tests must distinguish synthetic fixtures, host execution, QEMU execution, and exact-device validation.
- Every imported or generated third-party component needs provenance and license review.

A tool must not be described as proving hardware support unless it actually exercises that hardware or a faithful device model.
