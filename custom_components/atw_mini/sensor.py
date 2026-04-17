"""Sensor platform for ATW MINI."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import AtwMiniDataUpdateCoordinator
from .entity import AtwMiniCoordinatorEntity
from .parser import PARAMETER_DEFINITIONS, AtwMiniParameterDefinition


@dataclass(frozen=True, kw_only=True)
class AtwMiniSensorDescription(SensorEntityDescription):
    """Describes an ATW MINI sensor."""

    value_key: str
    raw_tag: str
    group: str


def _parameter_to_sensor_description(
    definition: AtwMiniParameterDefinition,
) -> AtwMiniSensorDescription:
    """Convert one parameter definition to a sensor description."""
    native_unit: str | None = None
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None

    if definition.control_type == "temperature":
        native_unit = UnitOfTemperature.CELSIUS
        device_class = SensorDeviceClass.TEMPERATURE
        state_class = SensorStateClass.MEASUREMENT
    elif definition.control_type == "percent":
        native_unit = PERCENTAGE
        state_class = SensorStateClass.MEASUREMENT
    elif definition.control_type == "duration":
        native_unit = "min"

    return AtwMiniSensorDescription(
        key=definition.key,
        name=definition.label,
        value_key=definition.key,
        raw_tag=f"parameters_t{definition.index}",
        group=definition.category,
        native_unit_of_measurement=native_unit,
        device_class=device_class,
        state_class=state_class,
        suggested_display_precision=1 if definition.control_type == "temperature" else None,
        entity_category=EntityCategory.DIAGNOSTIC if definition.diagnostic else None,
        entity_registry_enabled_default=definition.enabled_default,
        icon="mdi:tune-variant" if definition.diagnostic else None,
    )


CORE_SENSOR_DESCRIPTIONS: tuple[AtwMiniSensorDescription, ...] = (
    AtwMiniSensorDescription(
        key="indoor_temperature",
        translation_key="indoor_temperature",
        name="Indoor temperature",
        value_key="tep2",
        raw_tag="status_tep2",
        group="device_state",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="water_target_temperature",
        translation_key="water_target_temperature",
        name="Water target temperature",
        value_key="tep3",
        raw_tag="status_tep3",
        group="device_state",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="dhw_temperature",
        translation_key="dhw_temperature",
        name="DHW temperature",
        value_key="dhw_temperature",
        raw_tag="status_tep4",
        group="device_state",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="sensor_e_temperature",
        translation_key="sensor_e_temperature",
        name="Sensor E temperature",
        value_key="sensor_e_temperature",
        raw_tag="status_tep5",
        group="extra_sensors",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    AtwMiniSensorDescription(
        key="sensor_f_temperature",
        translation_key="sensor_f_temperature",
        name="Sensor F temperature",
        value_key="sensor_f_temperature",
        raw_tag="status_tep6",
        group="extra_sensors",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    AtwMiniSensorDescription(
        key="sensor_g_temperature",
        translation_key="sensor_g_temperature",
        name="Sensor G temperature",
        value_key="sensor_g_temperature",
        raw_tag="status_tep7",
        group="extra_sensors",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    AtwMiniSensorDescription(
        key="outdoor_temperature",
        translation_key="outdoor_temperature",
        name="Outdoor temperature",
        value_key="tep8",
        raw_tag="status_tep8",
        group="device_state",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="power_level",
        translation_key="power_level",
        name="Power level",
        value_key="power_level",
        raw_tag="status_pwr",
        group="device_state",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="operation_state",
        translation_key="operation_state",
        name="Operation state",
        value_key="operation_state",
        raw_tag="status_st1",
        group="device_state",
        icon="mdi:heat-pump",
        device_class=SensorDeviceClass.ENUM,
        options=["hidden_off", "heating_mode", "cooling_mode", "off", "defrost", "fault"],
    ),
    AtwMiniSensorDescription(
        key="heating_delivery_state",
        translation_key="heating_delivery_state",
        name="Heating delivery state",
        value_key="heating_delivery_state",
        raw_tag="status_st2",
        group="status_detail",
        icon="mdi:radiator",
        device_class=SensorDeviceClass.ENUM,
        options=[
            "hidden_off",
            "heating_via_hp",
            "heating_via_hp_plus_bivalent_stage_1",
            "heating_via_hp_plus_bivalent_stage_1_2",
            "summer_mode_dhw_only",
        ],
    ),
    AtwMiniSensorDescription(
        key="dhw_heating_state",
        translation_key="dhw_heating_state",
        name="DHW heating state",
        value_key="dhw_heating_state",
        raw_tag="status_st3",
        group="status_detail",
        icon="mdi:water-boiler",
        device_class=SensorDeviceClass.ENUM,
        options=["hidden_off", "dhw_heating_via_hp", "dhw_heating_via_electric_heater"],
    ),
    AtwMiniSensorDescription(
        key="operation_mode",
        translation_key="operation_mode",
        name="Operation mode",
        value_key="operation_mode",
        raw_tag="control_st2",
        group="device_state",
        icon="mdi:autorenew",
        device_class=SensorDeviceClass.ENUM,
        options=["heating", "cooling"],
    ),
    AtwMiniSensorDescription(
        key="season_mode",
        translation_key="season_mode",
        name="Season mode",
        value_key="season_mode",
        raw_tag="control_st3",
        group="device_state",
        icon="mdi:weather-partly-snowy-rainy",
        device_class=SensorDeviceClass.ENUM,
        options=["summer", "winter"],
    ),
    AtwMiniSensorDescription(
        key="firmware_version",
        name="Firmware version",
        value_key="firmware_version",
        raw_tag="about_firmware_version",
        group="device_info",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:chip",
    ),
    AtwMiniSensorDescription(
        key="unit_type",
        name="Unit type",
        value_key="unit_type",
        raw_tag="about_unittp",
        group="device_info",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:identifier",
    ),
    AtwMiniSensorDescription(
        key="build_time",
        name="Build time",
        value_key="build_time",
        raw_tag="about_build_time",
        group="device_info",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:clock-outline",
        entity_registry_enabled_default=False,
    ),
    AtwMiniSensorDescription(
        key="sd_card_state",
        name="SD card state",
        value_key="sd_card_state",
        raw_tag="about_sd_card_state",
        group="device_info",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:sd",
    ),
    AtwMiniSensorDescription(
        key="device_time",
        translation_key="device_time",
        name="Device time",
        value_key="device_time",
        raw_tag="status_rtcc",
        group="device_info",
        icon="mdi:clock-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)

PARAMETER_SENSOR_DESCRIPTIONS: tuple[AtwMiniSensorDescription, ...] = tuple(
    _parameter_to_sensor_description(definition) for definition in PARAMETER_DEFINITIONS
)

SENSOR_DESCRIPTIONS: tuple[AtwMiniSensorDescription, ...] = (
    *CORE_SENSOR_DESCRIPTIONS,
    *PARAMETER_SENSOR_DESCRIPTIONS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ATW MINI sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AtwMiniSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS
    )


class AtwMiniSensor(AtwMiniCoordinatorEntity, SensorEntity):
    """Representation of an ATW MINI sensor."""

    entity_description: AtwMiniSensorDescription

    def __init__(
        self,
        coordinator: AtwMiniDataUpdateCoordinator,
        description: AtwMiniSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{self.entity_description.key}"
        )

    @property
    def native_value(self):
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.values.get(self.entity_description.value_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        attributes: dict[str, Any] = {
            "group": self.entity_description.group,
            "raw_tag": self.entity_description.raw_tag,
            "last_update_success": self.coordinator.last_update_success,
            "raw_value": self.coordinator.data.raw.get(self.entity_description.raw_tag)
            if self.coordinator.data
            else None,
        }

        parameter = self.coordinator.data.parameters.get(self.entity_description.key)
        if parameter is not None:
            attributes.update(
                {
                    "label": parameter.label,
                    "value_display": parameter.value_display,
                    "value_raw": parameter.value_raw,
                    "editable": parameter.editable,
                    "min_raw": parameter.min_raw,
                    "max_raw": parameter.max_raw,
                    "control_type": parameter.control_type,
                    "category": parameter.category,
                }
            )

        return attributes
