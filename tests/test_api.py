"""Tests for the ATW MINI XML parser."""

from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path("custom_components/atw_mini/parser.py")
SPEC = importlib.util.spec_from_file_location("atw_mini_parser", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
parse_status_xml = MODULE.parse_status_xml


def test_parse_status_xml() -> None:
    fixture = Path("tests/fixtures/status.xml").read_text(encoding="utf-8")
    status = parse_status_xml(fixture)

    assert status.values["rtcc"] == "Pi  20:15:23  10.04.2026"
    assert status.values["tep2"] == 20.4
    assert status.values["tep3"] == 39.2
    assert status.values["tep4"] == 0.0
    assert status.values["tep8"] == 3.2
    assert status.values["pwr"] == 73
    assert status.values["st1"] is True
    assert status.values["st3"] is False
