"""Pure XML parsing helpers for ATW MINI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re
import xml.etree.ElementTree as ET


class AtwMiniParseError(Exception):
    """Raised when the XML payload cannot be parsed."""


ST1_STATE_MAP: dict[str, str] = {
    "1": "normal_operation",
    "4": "defrost",
}

CONTROL_POWER_MAP: dict[str, bool] = {
    "0": False,
    "1": True,
}

CONTROL_OPERATION_MODE_MAP: dict[str, str] = {
    "1": "heating",
    "2": "cooling",
}

CONTROL_SEASON_MODE_MAP: dict[str, str] = {
    "1": "summer",
    "2": "winter",
}


@dataclass(slots=True)
class AtwMiniStatus:
    """Normalized status payload returned by the heat pump."""

    raw: dict[str, str]
    values: dict[str, Any]


def parse_status_xml(xml_text: str) -> AtwMiniStatus:
    """Parse the raw XML returned by the device."""
    return _parse_xml(xml_text, source="status")


def parse_control_xml(xml_text: str) -> AtwMiniStatus:
    """Parse the raw XML returned by the control endpoint."""
    return _parse_xml(xml_text, source="control")


def merge_status_data(*payloads: AtwMiniStatus) -> AtwMiniStatus:
    """Merge multiple parsed payloads into one structure."""
    raw: dict[str, str] = {}
    values: dict[str, Any] = {}
    for payload in payloads:
        raw.update(payload.raw)
        values.update(payload.values)
    return AtwMiniStatus(raw=raw, values=values)


def _parse_xml(xml_text: str, source: str) -> AtwMiniStatus:
    """Parse device XML returned by one endpoint."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as err:
        raise AtwMiniParseError("Invalid XML received from device") from err

    raw: dict[str, str] = {}
    values: dict[str, Any] = {}

    for child in root:
        if child.text is None:
            continue

        raw_value = child.text.strip()
        raw_key = f"{source}_{child.tag}"
        raw[raw_key] = raw_value

        if source == "status":
            _parse_status_value(child.tag, raw_value, values)
        elif source == "control":
            _parse_control_value(child.tag, raw_value, values)
        else:
            values[raw_key] = raw_value

    return AtwMiniStatus(raw=raw, values=values)


def _parse_status_value(tag: str, raw_value: str, values: dict[str, Any]) -> None:
    """Parse values returned by status.xml."""
    if tag == "rtcc":
        values["device_time"] = raw_value
    elif tag == "st1":
        values["operation_state"] = _parse_st1_state(raw_value)
    elif tag.startswith("tep"):
        values[tag] = _parse_temperature(raw_value)
    elif tag == "pwr":
        values["power_level"] = _parse_percentage(raw_value)
    elif tag.startswith("st"):
        values[f"status_{tag[2:]}"] = raw_value == "1"
    else:
        values[f"status_{tag}"] = raw_value


def _parse_control_value(tag: str, raw_value: str, values: dict[str, Any]) -> None:
    """Parse values returned by control.xml."""
    if tag == "st1":
        values["heat_pump_enabled"] = CONTROL_POWER_MAP.get(raw_value)
    elif tag == "st2":
        values["operation_mode"] = CONTROL_OPERATION_MODE_MAP.get(
            raw_value, f"unknown_{raw_value}"
        )
    elif tag == "st3":
        values["season_mode"] = CONTROL_SEASON_MODE_MAP.get(
            raw_value, f"unknown_{raw_value}"
        )
    else:
        values[f"control_{tag}"] = raw_value


def _parse_temperature(value: str) -> float | None:
    """Extract a temperature from strings such as `20.4?C`."""
    match = re.search(r"-?\d+(?:[.,]\d+)?", value)
    if not match:
        return None
    return float(match.group(0).replace(",", "."))


def _parse_percentage(value: str) -> int | None:
    """Extract an integer percentage from strings such as `73 %`."""
    match = re.search(r"\d+", value)
    if not match:
        return None
    return int(match.group(0))


def _parse_st1_state(value: str) -> str:
    """Map st1 raw values to a stable operation state."""
    return ST1_STATE_MAP.get(value, f"unknown_{value}")
