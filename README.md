# ATW MINI Home Assistant Integration

![ATW MINI icon](assets/atw-mini-icon.svg)

Custom Home Assistant integration for the ATW MINI / NeoRe Mini heat pump using local HTTP/XML/HTML communication.

For the Slovak version, see [README.sk.md](README.sk.md).

## Current Status

This integration is already able to connect to the device over the local network and read multiple endpoints.

Current plugin version:
- `0.4.0`

Current integration scope:
- read-only
- local polling
- UI setup through `config_flow`
- compatible with HACS as a custom repository

## What The Plugin Currently Reads

The plugin currently reads these sources:
- `status.xml`
- `control.xml`
- `parameters.htm`
- `about.htm`
- `about.xml`

Authentication and transport:
- HTTP Basic Auth
- local device IP / hostname
- response encoding `windows-1250`

## What The Plugin Currently Exposes

### Device State

- indoor temperature
- water target temperature
- DHW temperature
- sensor E temperature
- sensor F temperature
- sensor G temperature
- outdoor temperature
- current power level in percent
- operation state from `status.xml`
  - `hidden_off`
  - `heating_mode`
  - `cooling_mode`
  - `off`
  - `defrost`
  - `fault`
- heating delivery state from `status.xml`
  - `hidden_off`
  - `heating_via_hp`
  - `heating_via_hp_plus_bivalent_stage_1`
  - `heating_via_hp_plus_bivalent_stage_1_2`
  - `summer_mode_dhw_only`
- DHW heating state from `status.xml`
  - `hidden_off`
  - `dhw_heating_via_hp`
  - `dhw_heating_via_electric_heater`
- operation mode from `control.xml`
  - `heating`
  - `cooling`
- season mode from `control.xml`
  - `summer`
  - `winter`
- heat pump enabled / disabled
- heat pump running / not running
- defrost binary state
- time setback active
- HDO blocking active

### Device Info

- firmware version
- unit type
- build time
- SD card state
- device time

### Parameter Groups

The integration also reads and exposes grouped parameter sensors from `parameters.htm`:

- Heating Curve
- Heating Limits
- Cooling Limits
- DHW
- Advanced / Unknown

For parameter-backed sensors, the integration stores and exposes:
- parsed value
- visible display value
- raw parameter value (`pN`)
- editability
- raw min / max limits when present
- grouping metadata

## What The Plugin Does Not Do Yet

The integration is still read-only.

It does not currently:
- write values back to the heat pump
- change operating mode
- change season mode
- change target temperatures
- submit form values from `parameters.htm`
- expose writable `number`, `select`, `switch`, or `climate` entities

## Installation Direction

Recommended installation path:
- add this repository to HACS as a custom repository
- install the integration
- restart Home Assistant
- add the integration from the UI
- enter host/IP, username, password, and scan interval

## Repository Contents

- [README.sk.md](README.sk.md) - Slovak overview
- [CHANGELOG.md](CHANGELOG.md) - release history
- [docs/hacs-navrh.md](docs/hacs-navrh.md) - architecture notes
- [docs/github-project-plan.md](docs/github-project-plan.md) - GitHub project structure
- [tests/fixtures](tests/fixtures) - sanitized parser fixtures

## Versioning

The integration version shown in Home Assistant comes from [manifest.json](custom_components/atw_mini/manifest.json).

Versioning rules:
- patch: fixes and small compatibility updates
- minor: new read-only entities, new sources, backward-compatible improvements
- major: breaking changes to entity names, config, or behavior

For every public release:
- update `custom_components/atw_mini/manifest.json`
- update [CHANGELOG.md](CHANGELOG.md)
- create a Git tag
- publish a GitHub release

## Notes

- real device IP addresses and credentials must never be committed
- raw local captures can stay local and out of Git
- `tep4` is now mapped as DHW temperature
- `tep5`, `tep6`, and `tep7` are currently exposed as Sensor E/F/G until their exact names are clarified further
- `status.xml st1` through `st5` are now mapped according to manufacturer documentation
- `heat_pump_running` is exposed as a simple derived binary state where `status.xml st2 != 0`
- the repository icon asset is stored in `assets/atw-mini-icon.svg`
- the Home Assistant UI tile icon is separate from the README image and usually requires Home Assistant branding assets to replace the default placeholder
