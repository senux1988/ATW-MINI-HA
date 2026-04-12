# Changelog

All notable changes to this project will be documented in this file.

The project follows Semantic Versioning.

## [0.1.0] - 2026-04-12

### Added

- Initial HACS-compatible Home Assistant integration scaffold
- Config flow for host, username, password, and scan interval
- Read-only XML polling from `status.xml`
- Sensors for indoor temperature, water target temperature, unknown `tep4`, outdoor temperature, power level, and device time
- Binary sensors for `st1` through `st5`
- Diagnostics support with redacted sensitive fields
- GitHub workflow, issue templates, documentation, and project icon

### Changed

- `st1` is now modeled as an operation state sensor instead of a binary sensor
- Added derived `defrost` binary sensor based on `st1 == 4`
