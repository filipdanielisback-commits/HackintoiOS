#!/usr/bin/env python3
"""Synthetic tests for tools/audit-hanoip-dts.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("audit-hanoip-dts.py")
SPEC = importlib.util.spec_from_file_location("audit_hanoip_dts", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class HanoipDtsAuditTests(unittest.TestCase):
    def make_tree(self, root: Path) -> None:
        qcom = root / "arch/arm64/boot/dts/qcom"
        qcom.mkdir(parents=True)
        (qcom / "Makefile").write_text(
            "dtbo-$(CONFIG_HANOIP_DTB) +=\\n"
            + "".join(f"\\tsdmmagpie-hanoip-{v}-overlay.dtbo \\\\n" for v in ("evt1", "dvt1", "dvt2"))
            + "".join(f"sdmmagpie-camera-sensor-mot-hanoip-{v}-overlay.dtsi\\n" for v in ("evt1", "dvt1", "dvt2")),
            encoding="utf-8",
        )
        (qcom / "sdmmagpie.dtsi").write_text(
            '/ { model = "Qualcomm Technologies, Inc. SDMMAGPIE";\\n'
            'compatible = "qcom,sdmmagpie";\\n'
            'interrupt-parent = <&pdc>;\\n};\\n',
            encoding="utf-8",
        )
        (qcom / "sdmmagpie-hanoip-common-overlay.dtsi").write_text(
            '#include "sdmmagpie-moto-common-overlay.dtsi"\\n'
            '#include "hanoi-panel.dtsi"\\n'
            '#include "sdmmagpie-hanoi-touchscreen.dtsi"\\n'
            '#include "sdmmagpie-hanoip-sensor-overlay.dtsi"\\n',
            encoding="utf-8",
        )
        for name, board in (("evt1", "0xA100"), ("dvt1", "0xB100"), ("dvt2", "0xB200")):
            (qcom / f"sdmmagpie-hanoip-{name}-overlay.dts").write_text(
                '/ { model = "hanoip";\\n'
                'qcom,msm-id = <365 0x0>;\\n'
                f'qcom,board-id = <0x4C {board}>;\\n}};\\n'
                '#include "sdmmagpie-hanoip-common-overlay.dtsi"\\n'
                f'#include "sdmmagpie-camera-sensor-mot-hanoip-{name}-overlay.dtsi"\\n',
                encoding="utf-8",
            )
            (qcom / f"sdmmagpie-camera-sensor-mot-hanoip-{name}-overlay.dtsi").write_text(
                "/* synthetic camera overlay */\\n", encoding="utf-8"
            )

    def test_reports_three_variants_without_claiming_exact_board(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_tree(root)
            report = MODULE.audit(root, "test-commit")
            self.assertEqual(report["shared_soc_tree"]["compatible"], '"qcom,sdmmagpie"')
            self.assertEqual(set(report["engineering_variants"]), {"evt1", "dvt1", "dvt2"})
            self.assertEqual(report["exact_xt2135_2_board_revision"], "unknown")

    def test_rejects_wrong_board_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_tree(root)
            overlay = root / "arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-evt1-overlay.dts"
            overlay.write_text(overlay.read_text(encoding="utf-8").replace('"hanoip"', '"other"'), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "identity fields"):
                MODULE.audit(root, "test-commit")

    def test_rejects_missing_common_overlay_include(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_tree(root)
            common = root / "arch/arm64/boot/dts/qcom/sdmmagpie-hanoip-common-overlay.dtsi"
            common.write_text('#include "sdmmagpie-moto-common-overlay.dtsi"\\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing expected includes"):
                MODULE.audit(root, "test-commit")


if __name__ == "__main__":
    unittest.main()
