# C++ user-space code

C++17 is available for user-space and system abstractions where it provides a clear benefit. Keep interfaces small and avoid assuming Apple's frameworks or a specific C++ standard library implementation.

The CI smoke test verifies compilation and a small host execution only; it does not validate IOKit or Darwin integration.
