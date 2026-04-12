# Changelog

All notable changes to this project will be documented in this file.

The project follows Semantic Versioning.

## [0.3.0] - 2026-04-12

### Added

- Read-only parsing for `parameters.htm`
- Read-only parsing for `about.htm`
- Read-only parsing for `about.xml`
- New grouped parameter and device-info sensors based on those sources

### Changed

- Internal data model now stores structured parameter records and device metadata
- The integration now reads five sources: `status.xml`, `control.xml`, `parameters.htm`, `about.htm`, and `about.xml`

## [0.2.0] - 2026-04-12

### Added

- Support for reading `control.xml` alongside `status.xml`
- Binary sensor for heat pump enabled state from `control.xml`
- Enum sensor for heating versus cooling operation mode
- Enum sensor for summer versus winter season mode

### Changed

- `st1` from `status.xml` remains modeled as operation state
- Internal parsing now distinguishes `status.xml` and `control.xml` values to avoid key collisions

## [0.1.0] - 2026-04-12

### Added

- Initial HACS-compatible Home Assistant integration scaffold
- Config flow for host, username, password, and scan interval
- Read-only XML polling from `status.xml`
- Sensors for indoor temperature, water target temperature, unknown `tep4`, outdoor temperature, power level, and device time
- Binary sensors for `st1` through `st5`
- Diagnostics support with redacted sensitive fields
- GitHub workflow, issue templates, documentation, and project icon
