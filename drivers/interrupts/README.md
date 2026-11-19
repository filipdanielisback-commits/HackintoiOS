# Interrupt-controller support

This directory is reserved for ARM64 interrupt-controller and HANOIP interrupt-routing integration.

Current status: not implemented. Source research identifies interrupt-parent relationships in the Linux device tree, but the XNU interrupt interface, delivered controller state, routing, and target-board mapping remain open. No interrupt controller is initialized here.
