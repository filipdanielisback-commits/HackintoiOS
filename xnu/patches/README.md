# HackintoiOS XNU patches

This directory is reserved for HackintoiOS-authored patches against the exact upstream revision in [../upstream.lock](../upstream.lock).

No functional XNU patches are included yet. Do not add placeholder patches that claim hardware support. Each future patch should document:

- the upstream files and revision it changes;
- the reason the change is needed;
- whether it is generic ARM64 work or HANOIP-specific;
- how it is validated;
- known limitations and whether it has been tested on physical hardware.

Keep patches reviewable and preserve upstream copyright and license notices.
