"""Tests for the ATW MINI XML parser."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

MODULE_PATH = Path("custom_components/atw_mini/parser.py")
SPEC = importlib.util.spec_from_file_location("atw_mini_parser", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
merge_status_data = MODULE.merge_status_data
parse_about_html = MODULE.parse_about_html
parse_about_xml = MODULE.parse_about_xml
parse_control_xml = MODULE.parse_control_xml
parse_parameters_html = MODULE.parse_parameters_html
parse_status_xml = MODULE.parse_status_xml


def test_parse_status_xml() -> None:
    fixture = Path("tests/fixtures/status.xml").read_text(encoding="utf-8")
    status = parse_status_xml(fixture)

    assert status.values["device_time"] == "Pi  20:15:23  10.04.2026"
    assert status.values["tep2"] == 20.4
    assert status.values["tep3"] == 39.2
    assert status.values["dhw_temperature"] == 0.0
    assert status.values["tep8"] == 3.2
    assert status.values["power_level"] == 73
    assert status.values["operation_state"] == "heating_mode"
    assert status.values["heating_delivery_state"] == "heating_via_hp"
    assert status.values["dhw_heating_state"] == "hidden_off"
    assert status.values["time_setback_active"] is False
    assert status.values["hdo_blocking_active"] is False


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

    assert merged.values["operation_state"] == "heating_mode"
    assert merged.values["heating_delivery_state"] == "heating_via_hp"
    assert merged.values["dhw_heating_state"] == "hidden_off"
    assert merged.values["heat_pump_enabled"] is True
    assert merged.values["operation_mode"] == "heating"
    assert merged.values["season_mode"] == "winter"


def test_parse_about_sources() -> None:
    about_html = Path("tests/fixtures/about.htm").read_text(encoding="utf-8")
    about_xml = Path("tests/fixtures/about.xml").read_text(encoding="utf-8")

    html_status = parse_about_html(about_html)
    xml_status = parse_about_xml(about_xml)
    merged = merge_status_data(html_status, xml_status)

    assert merged.values["firmware_version"] == "UTI-IQCP v2.1"
    assert merged.values["build_time"] == "May 13 2021 19:29:18"
    assert merged.values["sd_card_state"] == "nie je vložená"
    assert merged.values["unit_type"] == "W32"


def test_parse_parameters_html() -> None:
    parameters_html = Path("tests/fixtures/parameters.htm").read_text(encoding="utf-8")
    parsed = parse_parameters_html(parameters_html)

    assert parsed.values["mode_v1"] == "166"
    assert parsed.values["min_exchanger_temp_cooling"] == 7.0
    assert parsed.values["min_indoor_temp_cooling"] == 10.0
    assert parsed.values["max_indoor_temp_heating"] == 27.5
    assert parsed.values["regulation_constant"] == 12
    assert parsed.values["heating_curve_minus_20"] == 47.0
    assert parsed.values["heating_power_limit"] == 100.0
    assert parsed.values["dhw_time_limit"] == 20

    record = parsed.parameters["min_indoor_temp_cooling"]
    assert record.editable is True
    assert record.min_raw == 0
    assert record.max_raw == 127
    assert record.value_raw == "20"


def test_merge_all_sources() -> None:
    status_xml = Path("tests/fixtures/status.xml").read_text(encoding="utf-8")
    control_xml = Path("tests/fixtures/control.xml").read_text(encoding="utf-8")
    about_html = Path("tests/fixtures/about.htm").read_text(encoding="utf-8")
    about_xml = Path("tests/fixtures/about.xml").read_text(encoding="utf-8")
    parameters_html = Path("tests/fixtures/parameters.htm").read_text(encoding="utf-8")

    merged = merge_status_data(
        parse_status_xml(status_xml),
        parse_control_xml(control_xml),
        parse_about_html(about_html),
        parse_about_xml(about_xml),
        parse_parameters_html(parameters_html),
    )

    assert merged.values["operation_state"] == "heating_mode"
    assert merged.values["heating_delivery_state"] == "heating_via_hp"
    assert merged.values["dhw_heating_state"] == "hidden_off"
    assert merged.values["unit_type"] == "W32"
    assert merged.values["heating_curve_minus_20"] == 47.0
    assert merged.values["dhw_time_limit"] == 20
