#!/usr/bin/env python3
"""Validate the evidence-only HANOIP platform contract without inventing runtime data."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

CONTRACT = Path("drivers/platform/hanoip-platform.json")
REQUIRED_FACTS = {
    "shared_soc_compatible",
    "board_model",
    "qualcomm_platform_id",
    "engineering_variants",
    "cpu_enable_method",
    "interrupt_parent",
    "serial_alias",
}
REQUIRED_RUNTIME_FIELDS = {
    "cpu_topology",
    "psci_conduit",
    "memory_regions",
    "reserved_memory_regions",
    "device_tree_handoff_address",
    "interrupt_controller_instance",
    "interrupt_routing",
    "architectural_timer_frequency",
    "console_enabled_at_handoff",
    "console_registers",
    "board_revision_match",
}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("document_type") != "evidence-only-platform-contract":
        errors.append("document_type must identify an evidence-only contract")

    target = data.get("target", {})
    if target.get("model") != "XT2135-2" or target.get("family") != "HANOIP":
        errors.append("target must remain the documented XT2135-2 HANOIP")
    if target.get("exact_board_revision") is not None:
        errors.append("exact board revision must remain null until verified")
    if target.get("exact_board_revision_status") != "unresolved":
        errors.append("exact board revision status must remain unresolved")

    baseline = data.get("source_baseline", {})
    commit = baseline.get("commit")
    if commit != "5b04fac0cb2a8311ae69c8644384426e838d91fe":
        errors.append("source baseline must use the reviewed pinned kernel commit")

    facts = data.get("evidence_facts", [])
    fact_ids = {fact.get("id") for fact in facts}
    if fact_ids != REQUIRED_FACTS:
        errors.append("evidence fact IDs differ from the reviewed required set")
    for fact in facts:
        parsed = urlparse(fact.get("source_url", ""))
        if parsed.scheme != "https" or parsed.netloc != "github.com":
            errors.append(f"{fact.get('id')}: source_url must be a GitHub HTTPS URL")
        if commit and commit not in fact.get("source_url", ""):
            errors.append(f"{fact.get('id')}: source URL must pin the reviewed commit")
        if fact.get("runtime_use_allowed") is not False:
            errors.append(f"{fact.get('id')}: Linux source evidence cannot directly enable runtime code")
        if fact.get("confidence") != "verified_in_pinned_source":
            errors.append(f"{fact.get('id')}: confidence must describe source verification, not target validation")

    runtime = data.get("runtime_contract", {})
    if runtime.get("status") != "not_yet_derived_from_a_verified_loader_handoff":
        errors.append("runtime contract must remain unverified")
    fields = runtime.get("fields", {})
    if set(fields) != REQUIRED_RUNTIME_FIELDS:
        errors.append("runtime field set differs from the reviewed required set")
    for name, value in fields.items():
        if value is not None:
            errors.append(f"runtime field {name} must remain null until target-specific evidence exists")

    constraints = data.get("implementation_constraints", [])
    if len(constraints) < 5:
        errors.append("implementation constraints are incomplete")
    return errors


def main() -> int:
    try:
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"platform contract: cannot read valid JSON: {exc}", file=sys.stderr)
        return 1
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"platform contract: ERROR: {error}", file=sys.stderr)
        return 1
    print("platform contract: valid (evidence-only; runtime fields remain unresolved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
