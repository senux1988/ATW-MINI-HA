# GitHub Project Plan

## 1. Goal

Prepare the repository so it is easy to publish, maintain, and extend as a public HACS-compatible Home Assistant integration.

This plan covers:

- repository structure
- issue categories
- milestones
- labels
- project board workflow
- release expectations

## 2. Repository Layout

Recommended repository layout:

```text
.
+-- README.md
+-- LICENSE
+-- .gitignore
+-- hacs.json
+-- custom_components/
|   +-- atw_mini/
|       +-- __init__.py
|       +-- manifest.json
|       +-- const.py
|       +-- config_flow.py
|       +-- coordinator.py
|       +-- entity.py
|       +-- sensor.py
|       +-- binary_sensor.py
|       +-- api.py
|       +-- diagnostics.py
|       +-- translations/
|           +-- en.json
+-- tests/
|   +-- fixtures/
|   |   +-- status.xml
|   +-- test_api.py
|   +-- test_sensor.py
+-- docs/
|   +-- hacs-navrh.md
|   +-- github-project-plan.md
+-- .github/
    +-- ISSUE_TEMPLATE/
    |   +-- bug_report.yml
    |   +-- feature_request.yml
    +-- workflows/
        +-- validate.yml
```

## 3. Recommended GitHub Labels

Core labels:

- `bug`
- `enhancement`
- `documentation`
- `question`
- `good first issue`
- `help wanted`
- `needs investigation`
- `blocked`

Technical area labels:

- `area:api`
- `area:parser`
- `area:sensor`
- `area:binary-sensor`
- `area:config-flow`
- `area:tests`
- `area:docs`
- `area:hacs`

Priority labels:

- `priority:high`
- `priority:medium`
- `priority:low`

## 4. Recommended Milestones

Suggested milestone structure:

### `v0.1.0 - Read-only MVP`

- repository scaffold
- HACS metadata
- config flow
- XML fetcher
- XML parser
- sensors and binary sensors
- basic tests

### `v0.2.0 - Better Mapping`

- semantic naming cleanup
- `tep4` mapping
- `st1..st5` mapping
- better diagnostics
- improved docs

### `v0.3.0 - Control Support`

- investigate write endpoints
- add safe writable entities if supported
- add service calls if needed

## 5. Recommended Initial Issues

Suggested starter issues:

1. Create repository scaffold for HACS custom integration
2. Implement async API client for `status.xml`
3. Parse XML response and normalize values
4. Add Home Assistant `DataUpdateCoordinator`
5. Expose temperature and power sensors
6. Expose `st1..st5` as binary sensors
7. Implement config flow with connection test
8. Add fixture-based parser tests
9. Add diagnostics support
10. Prepare HACS metadata and public README

## 6. Project Board Mapping

Recommended GitHub Project columns:

- `Backlog`
- `Ready`
- `In Progress`
- `Review`
- `Done`

Recommended use:

- `Backlog`: captured work not yet prioritized
- `Ready`: well-defined tasks that can be started immediately
- `In Progress`: active implementation
- `Review`: code ready for validation or manual device testing
- `Done`: merged and documented

## 7. Definition Of Done

For implementation tasks, consider an issue done when:

- code is implemented
- XML edge cases are handled
- no real credentials are present
- tests or fixtures are updated when relevant
- README or docs are updated when behavior changes

## 8. Release Readiness Checklist

Before the first public release:

- `README.md` is in English
- repository contains `LICENSE`
- repository contains `hacs.json`
- integration has `manifest.json`
- setup works through Home Assistant UI
- device communication is fully local
- sample fixture data is anonymized
- installation instructions are documented

## 9. Suggested GitHub Roadmap Summary

The repository should start as a clean, read-only HACS integration with a narrow scope and strong naming discipline. The first public milestone should focus on reliable local polling, correct parsing, and solid documentation. Control features should be deferred until the write API is confirmed and validated on the real device.
