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
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import AtwMiniCoordinatorEntity


@dataclass(frozen=True, kw_only=True)
class AtwMiniSensorDescription(SensorEntityDescription):
    """Describes an ATW MINI sensor."""

    value_key: str
    raw_tag: str


SENSOR_DESCRIPTIONS: tuple[AtwMiniSensorDescription, ...] = (
    AtwMiniSensorDescription(
        key="indoor_temperature",
        translation_key="indoor_temperature",
        name="Indoor temperature",
        value_key="tep2",
        raw_tag="tep2",
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
        raw_tag="tep3",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="temperature_4",
        translation_key="temperature_4",
        name="Temperature 4",
        value_key="tep4",
        raw_tag="tep4",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        suggested_display_precision=1,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    AtwMiniSensorDescription(
        key="outdoor_temperature",
        translation_key="outdoor_temperature",
        name="Outdoor temperature",
        value_key="tep8",
        raw_tag="tep8",
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
        icon="mdi:heat-pump",
        device_class=SensorDeviceClass.ENUM,
        options=["normal_operation", "defrost"],
    ),
    AtwMiniSensorDescription(
        key="operation_mode",
        translation_key="operation_mode",
        name="Operation mode",
        value_key="operation_mode",
        raw_tag="control_st2",
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
        icon="mdi:weather-partly-snowy-rainy",
        device_class=SensorDeviceClass.ENUM,
        options=["summer", "winter"],
    ),
    AtwMiniSensorDescription(
        key="device_time",
        translation_key="device_time",
        name="Device time",
        value_key="device_time",
        raw_tag="status_rtcc",
        icon="mdi:clock-outline",
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ATW MINI sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(AtwMiniSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS)


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
    def extra_state_attributes(self) -> dict[str, str | bool | None]:
        """Return extra state attributes."""
        return {
            "raw_tag": self.entity_description.raw_tag,
            "last_update_success": self.coordinator.last_update_success,
            "raw_value": self.coordinator.data.raw.get(self.entity_description.raw_tag)
            if self.coordinator.data
            else None,
        }
