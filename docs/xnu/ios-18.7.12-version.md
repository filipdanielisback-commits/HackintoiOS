# iOS 18.7.12 XNU / Darwin version mapping

**Research status: Darwin version family established; public source candidate resolved; exact iOS 18.7.12 kernel build string still unconfirmed.**

## Target release identity

| Field | Verified value | Evidence |
|---|---|---|
| OS release | iOS 18.7.12 | Apple Developer release listing |
| OS build | `22H390` | Apple Developer release listing |
| Release date | 2026-11-09 | Apple Developer release listing |
| Reference device | iPhone XR, `iPhone11,8` | Apple security release listing / IPSW catalog |
| Darwin kernel version family | `24.6.0` | Public XNU version table maps the iOS 18.7 release train to Darwin 24.6.0 |
| Exact XNU build suffix for `22H390` | **Unconfirmed** | Public version table does not populate the 18.7.12 row |

## Public XNU source candidate

The Apple open-source repository contains the annotated tag:

- Repository: https://github.com/apple-oss-distributions/xnu
- Tag: `xnu-11417.140.69`
- Annotated tag object: `32a255dfa3a269f90931ec2f6e5d0bb9cb7e217d`
- Peeled commit: `43a90889846e00bfb5cf1d255cdc0a701a1e05a4`
- Tag object message: `Imported from xnu-11417.140.69.tar.gz`
- Tag object is unsigned according to GitHub's tag metadata.

The peeled commit is a reproducible **public upstream candidate** in the Darwin 24.6.0 family. It is not proof that this exact revision built the iOS 18.7.12 iPhone XR kernel. Device builds can contain additional configuration, platform code, and build-specific changes.

## Why the previous pin is not suitable

The previous pin was:

- Tag: `xnu-11215.1.10`
- Commit: `8d741a5de7ff4191bf97d57b9f54c2f6d4a15585`
- Generation: iOS 18.0 / Darwin 24.0.0

That is earlier than the iOS 18.7.12 target's Darwin 24.6.0 family and must not be presented as the final target baseline.

## Baseline decision

1. Record Darwin `24.6.0` as the best-supported version family for the iOS 18.7.12 target.
2. Record `xnu-11417.140.69` at peeled commit `43a90889846e00bfb5cf1d255cdc0a701a1e05a4` as the public upstream candidate.
3. Keep `xnu/upstream.lock` unchanged until stronger evidence ties build `22H390` to an exact XNU build suffix or confirms that this public tag is the intended source baseline.
4. If exact public evidence is unavailable, label the candidate as family-matched rather than exact-build-matched. Do not invent a suffix.
5. Keep generic upstream XNU, Apple device-specific kernel configuration, and the original HANOIP port as separate layers.

## Sources

- Apple Developer, iOS 18.7.12 (22H390), November 9, 2026: https://developer.apple.com/news/releases/?id=11092026h
- Apple Support, Apple security releases: https://support.apple.com/en-us/100100
- IPSW Downloads, iPhone XR firmware list: https://ipsw.me/iPhone11%2C8/
- The Apple Wiki, XNU kernel-version table: https://theapplewiki.com/wiki/XNU
- Apple open-source XNU tag: https://github.com/apple-oss-distributions/xnu/tree/xnu-11417.140.69
- GitHub tag object API: https://api.github.com/repos/apple-oss-distributions/xnu/git/tags/32a255dfa3a269f90931ec2f6e5d0bb9cb7e217d

This is a version-mapping research note, not a kernel build, port, or bootability result.
