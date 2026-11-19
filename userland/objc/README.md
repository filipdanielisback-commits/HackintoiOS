# Objective-C (reserved user-space layer)

Objective-C is reserved for future application-facing or framework-facing user-space work if a compatible runtime and framework environment becomes available.

It is not required for XNU kernel code or hardware drivers. The Linux CI check for language-smoke.m is syntax-only: it does not link an Objective-C runtime, Foundation, Cocoa, UIKit, or any Apple framework.
