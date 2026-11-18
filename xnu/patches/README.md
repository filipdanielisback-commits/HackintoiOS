# HackintoiOS XNU patches

This directory contains original HackintoiOS patch files against the exact upstream revision in [../upstream.lock](../upstream.lock).

## Rules

- Add a patch only for a specific, evidence-backed HANOIP requirement.
- Keep patches small and independently reviewable.
- Record the reason, affected subsystem, upstream files, and test evidence in each patch description.
- Never copy a HakiOS/POCO-specific patch and assume it applies to HANOIP.
- Run the patch-series check against the pinned source before proposing a patch.
- No functional patch is currently included. Do not interpret the empty series as a patched or ported kernel.
