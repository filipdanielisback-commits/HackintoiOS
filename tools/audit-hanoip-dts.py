#!/usr/bin/env python3
"""Audit the pinned HANOIP device-tree sources without building or touching a device."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

QCOM_DTS = Path("arch/arm64/boot/dts/qcom")
VARIANTS = {
    "evt1": ("sdmmagpie-hanoip-evt1-overlay.dts", "sdmmagpie-camera-sensor-mot-hanoip-evt1-overlay.dtsi"),
    "dvt1": ("sdmmagpie-hanoip-dvt1-overlay.dts", "sdmmagpie-camera-sensor-mot-hanoip-dvt1-overlay.dtsi"),
    "dvt2": ("sdmmagpie-hanoip-dvt2-overlay.dts", "sdmmagpie-camera-sensor-mot-hanoip-dvt2-overlay.dtsi"),
}


def read_text(root: Path, relative: Path) -> str:
    path = root / relative
    if not path.is_file():
        raise ValueError(f"required source file is missing: {relative}")
    return path.read_text(encoding="utf-8")


def property_value(source: str, name: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*(.+?);", source, re.MULTILINE)
    return match.group(1).strip() if match else None


def include_names(source: str) -> list[str]:
    return re.findall(r'^\s*#include\s+"([^"]+)"', source, re.MULTILINE)


def audit(root: Path, source_commit: str) -> dict:
    makefile = read_text(root, QCOM_DTS / "Makefile")
    soc = read_text(root, QCOM_DTS / "sdmmagpie.dtsi")
    common = read_text(root, QCOM_DTS / "sdmmagpie-hanoip-common-overlay.dtsi")

    if "dtbo-$(CONFIG_HANOIP_DTB)" not in makefile:
        raise ValueError("QCOM Makefile does not register CONFIG_HANOIP_DTB")
    if property_value(soc, "compatible") != '"qcom,sdmmagpie"':
        raise ValueError("shared SoC tree does not declare qcom,sdmmagpie")
    if property_value(soc, "interrupt-parent") != "<&pdc>":
        raise ValueError("shared SoC interrupt-parent differs from the audited value")

    variants = {}
    for name, (overlay_name, camera_name) in VARIANTS.items():
        overlay = read_text(root, QCOM_DTS / overlay_name)
        read_text(root, QCOM_DTS / camera_name)
        board_id = property_value(overlay, "qcom,board-id")
        msm_id = property_value(overlay, "qcom,msm-id")
        model = property_value(overlay, "model")
        includes = include_names(overlay)
        if model != '"hanoip"' or msm_id != "<365 0x0>" or not board_id:
            raise ValueError(f"{name} overlay identity fields are incomplete or unexpected")
        if "sdmmagpie-hanoip-common-overlay.dtsi" not in includes:
            raise ValueError(f"{name} overlay does not include the HANOIP common overlay")
        if camera_name not in includes:
            raise ValueError(f"{name} overlay does not include its matching camera overlay")
        if overlay_name.replace(".dts", ".dtbo") not in makefile:
            raise ValueError(f"{name} HANOIP overlay is not referenced by the audited Makefile")
        variants[name] = {
            "overlay": overlay_name,
            "camera_overlay": camera_name,
            "model": model.strip('"'),
            "qcom_msm_id": msm_id,
            "qcom_board_id": board_id,
            "includes": includes,
            "camera_overlay_present": True,
        }

    common_includes = include_names(common)
    required_common = {
        "sdmmagpie-moto-common-overlay.dtsi",
        "hanoi-panel.dtsi",
        "sdmmagpie-hanoi-touchscreen.dtsi",
        "sdmmagpie-hanoip-sensor-overlay.dtsi",
    }
    missing = sorted(required_common.difference(common_includes))
    if missing:
        raise ValueError("HANOIP common overlay is missing expected includes: " + ", ".join(missing))

    return {
        "schema": 1,
        "source_repository": "motorola-sm6150-devs/android_kernel_motorola_sm6150",
        "source_branch": "lineage-20",
        "source_commit": source_commit or "not-supplied",
        "target_family": "HANOIP",
        "shared_soc_tree": {
            "file": str(QCOM_DTS / "sdmmagpie.dtsi"),
            "model": property_value(soc, "model"),
            "compatible": property_value(soc, "compatible"),
            "interrupt_parent": property_value(soc, "interrupt-parent"),
        },
        "board_common_overlay": {
            "file": str(QCOM_DTS / "sdmmagpie-hanoip-common-overlay.dtsi"),
            "includes": common_includes,
        },
        "engineering_variants": variants,
        "exact_xt2135_2_board_revision": "unknown",
        "limitations": [
            "This is a source-text audit, not a compiled or merged device tree.",
            "Engineering overlay IDs do not identify which overlay matches a particular XT2135-2 unit.",
            "Linux device-tree properties are hardware evidence, not XNU configuration or drivers.",
            "No phone, firmware, partition, or boot configuration is accessed or changed.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="root of the pinned Linux kernel source tree")
    parser.add_argument("--source-commit", default="", help="audited kernel source commit")
    parser.add_argument("--output", type=Path, help="optional JSON report path")
    args = parser.parse_args()

    try:
        report = audit(args.source.resolve(), args.source_commit)
    except (OSError, ValueError) as exc:
        print(f"HANOIP DTS audit failed: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
