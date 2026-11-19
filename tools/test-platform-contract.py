#!/usr/bin/env python3
"""Synthetic tests for the HANOIP evidence-only platform contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_platform_contract", ROOT / "tools/check-platform-contract.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class PlatformContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(
            (ROOT / "drivers/platform/hanoip-platform.json").read_text(encoding="utf-8")
        )

    def test_repository_contract_is_valid(self):
        self.assertEqual(MODULE.validate(self.data), [])

    def test_rejects_guessed_memory_address(self):
        data = copy.deepcopy(self.data)
        data["runtime_contract"]["fields"]["device_tree_handoff_address"] = "0x80000000"
        self.assertTrue(any("must remain null" in item for item in MODULE.validate(data)))

    def test_rejects_assuming_exact_board_revision(self):
        data = copy.deepcopy(self.data)
        data["target"]["exact_board_revision"] = "DVT2"
        self.assertTrue(any("board revision must remain null" in item for item in MODULE.validate(data)))

    def test_rejects_unpinned_or_non_github_evidence(self):
        data = copy.deepcopy(self.data)
        data["evidence_facts"][0]["source_url"] = "https://example.com/device-tree"
        self.assertTrue(any("source_url must be a GitHub HTTPS URL" in item for item in MODULE.validate(data)))

    def test_rejects_linux_evidence_used_as_runtime_enablement(self):
        data = copy.deepcopy(self.data)
        data["evidence_facts"][0]["runtime_use_allowed"] = True
        self.assertTrue(any("cannot directly enable runtime code" in item for item in MODULE.validate(data)))


if __name__ == "__main__":
    unittest.main()
