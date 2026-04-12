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
merge_status_data = MODULE.merge_status_data
parse_control_xml = MODULE.parse_control_xml
parse_status_xml = MODULE.parse_status_xml


def test_parse_status_xml() -> None:
    fixture = Path("tests/fixtures/status.xml").read_text(encoding="utf-8")
    status = parse_status_xml(fixture)

    assert status.values["device_time"] == "Pi  20:15:23  10.04.2026"
    assert status.values["tep2"] == 20.4
    assert status.values["tep3"] == 39.2
    assert status.values["tep4"] == 0.0
    assert status.values["tep8"] == 3.2
    assert status.values["power_level"] == 73
    assert status.values["operation_state"] == "normal_operation"
    assert status.values["status_3"] is False


def test_parse_control_xml() -> None:
    fixture = Path("tests/fixtures/control.xml").read_text(encoding="utf-8")
    status = parse_control_xml(fixture)

    assert status.values["heat_pump_enabled"] is True
    assert status.values["operation_mode"] == "heating"
    assert status.values["season_mode"] == "winter"


def test_merge_status_data() -> None:
    status_xml = Path("tests/fixtures/status.xml").read_text(encoding="utf-8")
    control_xml = Path("tests/fixtures/control.xml").read_text(encoding="utf-8")
    merged = merge_status_data(parse_status_xml(status_xml), parse_control_xml(control_xml))

    assert merged.values["operation_state"] == "normal_operation"
    assert merged.values["heat_pump_enabled"] is True
    assert merged.values["operation_mode"] == "heating"
    assert merged.values["season_mode"] == "winter"
