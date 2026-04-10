"""Pure XML parsing helpers for ATW MINI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import re
import xml.etree.ElementTree as ET


class AtwMiniParseError(Exception):
    """Raised when the XML payload cannot be parsed."""


@dataclass(slots=True)
class AtwMiniStatus:
    """Normalized status payload returned by the heat pump."""

    raw: dict[str, str]
    values: dict[str, Any]


def parse_status_xml(xml_text: str) -> AtwMiniStatus:
    """Parse the raw XML returned by the device."""
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
        raw[child.tag] = raw_value

        if child.tag == "rtcc":
            values[child.tag] = raw_value
        elif child.tag.startswith("tep"):
            values[child.tag] = _parse_temperature(raw_value)
        elif child.tag == "pwr":
            values[child.tag] = _parse_percentage(raw_value)
        elif child.tag.startswith("st"):
            values[child.tag] = raw_value == "1"
        else:
            values[child.tag] = raw_value

    return AtwMiniStatus(raw=raw, values=values)


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

