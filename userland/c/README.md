# C user-space code

C is the primary language for portable user-space utilities and host-side smoke tests. Existing userland code is a host test harness, not Darwin user space or an iOS application.

Compiler baseline: C11. Keep platform-specific APIs behind explicit interfaces so host tests do not pretend to validate Darwin behavior.
