# iOS 18.7.12 XNU / Darwin version mapping

**Research status: Darwin version family established; exact iOS 18.7.12 kernel build string not yet independently confirmed.**

## Target release identity

| Field | Verified value | Evidence |
|---|---|---|
| OS release | iOS 18.7.12 | Apple Developer release listing |
| OS build | `22H390` | Apple Developer release listing |
| Release date | 2026-11-09 | Apple Developer release listing |
| Reference device | iPhone XR, `iPhone11,8` | IPSW catalog / firmware metadata |
| Darwin kernel version family | `24.6.0` | The Apple Wiki XNU kernel-version table maps iOS 18.7 releases to Darwin 24.6.0; later iOS 18.7.x entries remain on this kernel train |
| Exact XNU build suffix for `22H390` | **Unconfirmed** | The public version table has no kernel build string populated for the 18.7.12 row |

## Public XNU source reference

The Apple open-source repository contains the tag:

- Repository: https://github.com/apple-oss-distributions/xnu
- Public tag: `xnu-11417.140.69`
- This tag is in the Darwin `24.6.0` source family.
- The tag was independently checked as an existing ref by fetching its README from that ref.

The tag is a sensible **public source baseline candidate** for Darwin 24.6.0. It is not proof that it is byte-for-byte the XNU source revision used to build iOS 18.7.12 on the iPhone XR. Apple device kernels may include build-specific revisions, configuration, and platform changes not represented by the generic public source tag.

## Why the current pin is not suitable as the final baseline

The repository previously pinned:

- Tag: `xnu-11215.1.10`
- Commit: `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`
- Version family: Darwin `24.0.0`, associated with the iOS 18.0 generation.

That is substantially earlier than the iOS 18.7.12 target's Darwin 24.6.0 family. It must not be described as the exact target baseline.

## Baseline decision

1. Record Darwin `24.6.0` as the verified version family for the iOS 18.7.12 research target.
2. Record `xnu-11417.140.69` as the public upstream candidate for that Darwin family.
3. Do **not** change `xnu/upstream.lock` to the candidate until the tag's commit SHA has been resolved and the exact `22H390` kernel build string has been checked against stronger evidence where available.
4. If the exact iOS build's XNU suffix cannot be established from public metadata, retain that uncertainty in the lockfile and documentation. Do not invent a suffix or claim an exact source match.
5. Keep the generic upstream XNU source, any device-specific Apple kernel configuration, and HackintoiOS's HANOIP port as three separate concepts.

## Sources

- Apple Developer, iOS 18.7.12 (22H390), November 9, 2026: https://developer.apple.com/news/releases/?id=09142026e
- Apple Support, Apple security releases (lists iOS 18.7.12 for iPhone XR): https://support.apple.com/en-us/100100
- IPSW Downloads, iPhone XR firmware list: https://ipsw.me/iPhone11%2C8/
- The Apple Wiki, XNU kernel-version table: https://theapplewiki.com/wiki/XNU
- Apple open-source XNU repository: https://github.com/apple-oss-distributions/xnu/tree/xnu-11417.140.69

This is a version-mapping research note, not a kernel build, port, or bootability result.
