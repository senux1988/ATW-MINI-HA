"""Pure parsing helpers for ATW MINI XML and HTML sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import unescape
from typing import Any
import re
import xml.etree.ElementTree as ET


class AtwMiniParseError(Exception):
    """Raised when a payload cannot be parsed."""


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


@dataclass(frozen=True, slots=True)
class AtwMiniParameterDefinition:
    """Definition of one parameter entry from parameters.htm."""

    index: int
    key: str
    label: str
    category: str
    control_type: str
    unit: str | None = None
    diagnostic: bool = False
    enabled_default: bool = True


PARAMETER_DEFINITIONS: tuple[AtwMiniParameterDefinition, ...] = (
    AtwMiniParameterDefinition(0, "mode_v1", "Mode V1", "advanced", "opaque", diagnostic=True, enabled_default=False),
    AtwMiniParameterDefinition(1, "min_exchanger_temp_cooling", "Cooling min exchanger temperature", "cooling_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(2, "max_exchanger_temp_heating", "Heating max exchanger temperature", "heating_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(3, "min_indoor_temp_cooling", "Cooling min indoor temperature", "cooling_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(4, "max_indoor_temp_heating", "Heating max indoor temperature", "heating_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(5, "regulation_constant", "Regulation constant", "advanced", "integer", diagnostic=True, enabled_default=False),
    AtwMiniParameterDefinition(6, "mode_v2", "Mode V2", "advanced", "opaque", diagnostic=True, enabled_default=False),
    AtwMiniParameterDefinition(7, "heating_curve_minus_20", "Heating curve -20 C", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(8, "heating_curve_minus_12", "Heating curve -12 C", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(9, "heating_curve_minus_4", "Heating curve -4 C", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(10, "heating_curve_plus_4", "Heating curve +4 C", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(11, "heating_curve_plus_12", "Heating curve +12 C", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(12, "heating_curve_plus_20", "Heating curve +20 C", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(13, "dhw_power_limit", "DHW power limit", "dhw", "percent", "%"),
    AtwMiniParameterDefinition(14, "dhw_min_temperature", "DHW min temperature", "dhw", "temperature", "°C"),
    AtwMiniParameterDefinition(15, "dhw_max_temperature", "DHW max temperature", "dhw", "temperature", "°C"),
    AtwMiniParameterDefinition(16, "heating_power_limit", "Heating power limit", "heating_limits", "percent", "%"),
    AtwMiniParameterDefinition(17, "cooling_power_limit", "Cooling power limit", "cooling_limits", "percent", "%"),
    AtwMiniParameterDefinition(18, "cooling_water_temperature", "Cooling water temperature", "cooling_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(19, "bivalent_temperature", "Bivalent temperature", "heating_curve", "temperature", "°C"),
    AtwMiniParameterDefinition(20, "heating_temperature_setback", "Heating temperature setback", "heating_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(21, "cooling_temperature_setback", "Cooling temperature setback", "cooling_limits", "temperature", "°C"),
    AtwMiniParameterDefinition(22, "dhw_time_limit", "DHW time limit", "dhw", "duration", "min"),
)

PARAMETER_DEFINITIONS_BY_INDEX = {item.index: item for item in PARAMETER_DEFINITIONS}


@dataclass(slots=True)
class AtwMiniParameterRecord:
    """Parsed parameter row from parameters.htm."""

    key: str
    display_id: str
    label: str
    value_display: str
    value_raw: str | None
    parsed_value: Any
    unit: str | None
    category: str
    editable: bool
    min_raw: int | None
    max_raw: int | None
    control_type: str


@dataclass(slots=True)
class AtwMiniStatus:
    """Normalized payload returned by the device."""

    raw: dict[str, str]
    values: dict[str, Any]
    parameters: dict[str, AtwMiniParameterRecord] = field(default_factory=dict)
    device_info: dict[str, Any] = field(default_factory=dict)


def parse_status_xml(xml_text: str) -> AtwMiniStatus:
    """Parse the raw XML returned by status.xml."""
    return _parse_xml(xml_text, source="status")


def parse_control_xml(xml_text: str) -> AtwMiniStatus:
    """Parse the raw XML returned by control.xml."""
    return _parse_xml(xml_text, source="control")


def parse_about_xml(xml_text: str) -> AtwMiniStatus:
    """Parse the raw XML returned by about.xml."""
    return _parse_xml(xml_text, source="about")


def parse_about_html(html_text: str) -> AtwMiniStatus:
    """Parse the static metadata from about.htm."""
    raw: dict[str, str] = {}
    values: dict[str, Any] = {}
    device_info: dict[str, Any] = {}

    field_map = {
        "Verzia": "firmware_version",
        "Typ jedn.": "unit_type_label",
        "Vytvorené": "build_time",
        "SD Karta": "sd_card_state",
    }

    for label, value in re.findall(
        r"<div><label><B>([^<:]+):\s*</B></label><td>(.*?)</div>",
        html_text,
        re.S,
    ):
        clean_label = _strip_html(_normalize_space(label))
        clean_value = _strip_html(_normalize_space(value))
        key = field_map.get(clean_label)
        if key is None:
            continue
        raw[f"about_{key}"] = clean_value
        values[key] = clean_value
        device_info[key] = clean_value

    return AtwMiniStatus(raw=raw, values=values, device_info=device_info)


def parse_parameters_html(html_text: str) -> AtwMiniStatus:
    """Parse editable parameters from parameters.htm."""
    hidden_values = {
        int(index): value
        for index, value in re.findall(
            r'<input type="hidden" name="p(\d+)" id="p\d+" value="([^"]*)"\s*/?>',
            html_text,
        )
    }

    row_pattern = re.compile(
        r'<div class="w36 fl teppop">(.*?)</div>\s*'
        r'<div class="w34 fr tepost" id="(t\d+)">(.*?)</div>\s*'
        r"</div>\s*<div class=\"w28 fr\">(.*?)</div>",
        re.S,
    )

    raw: dict[str, str] = {}
    values: dict[str, Any] = {}
    parameters: dict[str, AtwMiniParameterRecord] = {}

    for label_html, display_id, value_html, controls_html in row_pattern.findall(html_text):
        index = int(display_id[1:])
        definition = PARAMETER_DEFINITIONS_BY_INDEX.get(index)
        if definition is None:
            continue

        label = _strip_html(_normalize_space(label_html))
        value_display = _strip_html(_normalize_space(value_html))
        value_raw = hidden_values.get(index)
        editable, min_raw, max_raw = _parse_button_metadata(controls_html)
        parsed_value = _parse_parameter_value(value_display, definition.control_type)

        record = AtwMiniParameterRecord(
            key=definition.key,
            display_id=display_id,
            label=label,
            value_display=value_display,
            value_raw=str(value_raw) if value_raw is not None else None,
            parsed_value=parsed_value,
            unit=definition.unit,
            category=definition.category,
            editable=editable,
            min_raw=min_raw,
            max_raw=max_raw,
            control_type=definition.control_type,
        )

        parameters[definition.key] = record
        values[definition.key] = parsed_value
        raw[f"parameters_{display_id}"] = value_display
        if value_raw is not None:
            raw[f"parameters_p{index}"] = str(value_raw)

    return AtwMiniStatus(raw=raw, values=values, parameters=parameters)


def merge_status_data(*payloads: AtwMiniStatus) -> AtwMiniStatus:
    """Merge multiple parsed payloads into one structure."""
    raw: dict[str, str] = {}
    values: dict[str, Any] = {}
    parameters: dict[str, AtwMiniParameterRecord] = {}
    device_info: dict[str, Any] = {}

    for payload in payloads:
        raw.update(payload.raw)
        values.update(payload.values)
        parameters.update(payload.parameters)
        device_info.update(payload.device_info)

    return AtwMiniStatus(
        raw=raw,
        values=values,
        parameters=parameters,
        device_info=device_info,
    )


def _parse_xml(xml_text: str, source: str) -> AtwMiniStatus:
    """Parse one XML endpoint."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as err:
        raise AtwMiniParseError("Invalid XML received from device") from err

    raw: dict[str, str] = {}
    values: dict[str, Any] = {}
    device_info: dict[str, Any] = {}

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
        elif source == "about":
            _parse_about_value(child.tag, raw_value, values, device_info)
        else:
            values[raw_key] = raw_value

    return AtwMiniStatus(raw=raw, values=values, device_info=device_info)


def _parse_status_value(tag: str, raw_value: str, values: dict[str, Any]) -> None:
    """Parse values returned by status.xml."""
    if tag == "rtcc":
        values["device_time"] = raw_value
    elif tag == "st1":
        values["operation_state"] = _parse_st1_state(raw_value)
    elif tag == "st2":
        values["heat_pump_running"] = raw_value == "1"
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
        values["operation_mode"] = CONTROL_OPERATION_MODE_MAP.get(raw_value, f"unknown_{raw_value}")
    elif tag == "st3":
        values["season_mode"] = CONTROL_SEASON_MODE_MAP.get(raw_value, f"unknown_{raw_value}")
    else:
        values[f"control_{tag}"] = raw_value


def _parse_about_value(
    tag: str,
    raw_value: str,
    values: dict[str, Any],
    device_info: dict[str, Any],
) -> None:
    """Parse values returned by about.xml."""
    if tag == "unittp":
        values["unit_type"] = raw_value
        device_info["unit_type"] = raw_value
    else:
        values[f"about_{tag}"] = raw_value
        device_info[tag] = raw_value


def _parse_parameter_value(value: str, control_type: str) -> Any:
    """Parse one parameter display value."""
    if control_type in {"temperature", "percent"}:
        return _parse_float(value)
    if control_type in {"integer", "duration"}:
        return _parse_int(value)
    return value


def _parse_button_metadata(controls_html: str) -> tuple[bool, int | None, int | None]:
    """Extract button metadata from the control column."""
    minus = re.search(r"mbt\(\d+,(-?\d+),\d+\)", controls_html)
    plus = re.search(r"pbt\(\d+,(-?\d+),\d+\)", controls_html)
    editable = bool(minus or plus)
    min_raw = int(minus.group(1)) if minus else None
    max_raw = int(plus.group(1)) if plus else None
    return editable, min_raw, max_raw


def _parse_temperature(value: str) -> float | None:
    """Extract a temperature from strings such as `20.4 °C`."""
    return _parse_float(value)


def _parse_percentage(value: str) -> int | None:
    """Extract an integer percentage from strings such as `73 %`."""
    parsed = _parse_int(value)
    return parsed


def _parse_st1_state(value: str) -> str:
    """Map st1 raw values to a stable operation state."""
    return ST1_STATE_MAP.get(value, f"unknown_{value}")


def _parse_float(value: str) -> float | None:
    """Extract a float from a localized string."""
    match = re.search(r"-?\d+(?:[.,]\d+)?", value)
    if not match:
        return None
    return float(match.group(0).replace(",", "."))


def _parse_int(value: str) -> int | None:
    """Extract an integer from a localized string."""
    match = re.search(r"-?\d+", value)
    if not match:
        return None
    return int(match.group(0))


def _normalize_space(value: str) -> str:
    """Collapse whitespace."""
    return re.sub(r"\s+", " ", value).strip()


def _strip_html(value: str) -> str:
    """Strip HTML tags and unescape entities."""
    without_tags = re.sub(r"<[^>]+>", "", value)
    return unescape(without_tags).strip()
