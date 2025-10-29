# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant custom integration for ecoNET-300 devices (heating/boiler controllers and solar systems). It provides local control over ecoMAX, ecoSOL, and SControl devices through their native REST API, without requiring cloud services.

## Development Commands

### Code Quality & Formatting

```bash
# Format code (ALWAYS run before committing)
ruff format .

# Check code quality
ruff check .

# Auto-fix issues
ruff check --fix .

# Check spelling
codespell
```

**CRITICAL**: This project uses Ruff (version 0.12.2) exclusively for formatting and linting. Never use Black, isort, or flake8.

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sensor_basic.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_sensor_basic.py::test_sensor_creation
```

### API Testing

```bash
# Test API endpoints against a real device
python scripts/test_api_endpoints.py --host 192.168.1.100 --username admin --password your_password

# With verbose output
python scripts/test_api_endpoints.py --host 192.168.1.100 --username admin --password your_password --verbose
```

### Translation Validation

```bash
# Check translations for consistency
python scripts/check_translations.py

# Find available languages
python scripts/language_finder.py
```

## Architecture

### Core Components

1. **API Layer** (`api.py`):
   - Handles all HTTP communication with ecoNET-300 devices
   - Uses aiohttp for async requests with basic auth
   - Implements caching via `MemCache` class
   - Main endpoints: `/econet/regParams`, `/econet/sysParams`, `/econet/rmCurrentDataParams`, `/econet/editParams`

2. **Data Coordinator** (`common.py`):
   - `EconetDataCoordinator` extends Home Assistant's `DataUpdateCoordinator`
   - Polls device every 10 seconds for state updates
   - Manages entity refresh and error handling

3. **Entity Platforms**:
   - `sensor.py` - Read-only sensors (temperatures, power, status)
   - `binary_sensor.py` - On/off sensors (pumps, fans, connections)
   - `number.py` - Adjustable numeric values (temperature setpoints)
   - `switch.py` - Boiler on/off control
   - `select.py` - Mode selection (winter/summer/auto)

4. **Configuration** (`config_flow.py`):
   - UI-based configuration flow
   - Validates device connectivity during setup
   - Stores host, username, password

5. **Constants** (`const.py`):
   - All entity definitions in mapping dictionaries
   - Icons, units, device classes, precision settings
   - API endpoint constants

### Data Flow

```
Device API → Api.async_fetch_data() → EconetDataCoordinator → Entity.coordinator_update() → Home Assistant State
```

For control operations:
```
Home Assistant Service → Entity.async_set_* → Api.async_set_param() → Device API
```

### Device Type Support

The integration uses test fixtures in `tests/fixtures/` to validate against different device types:
- **ecoMAX810P-L** - Most feature-rich, all endpoints available
- **ecoMAX360** - Basic boiler controller
- **ecoMAX850R2-X** - Pellet boiler with extended features
- **ecoMAX860P2-N**, **ecoMAX860P3-V** - Alternative boiler models
- **ecoSOL**, **ecoSOL500** - Solar thermal controllers
- **SControl MK1** - Basic control module

Each device has different available parameters. The integration uses conditional entity creation based on what data is available.

## Critical Code Style Rules

**From `.cursor/rules/code-style-ruff.mdc`:**

1. **Import Order** (CRITICAL):
   ```python
   # Standard library (alphabetical)
   import asyncio
   import logging
   from typing import Any

   # Third-party (alphabetical)
   import aiohttp
   from homeassistant.core import HomeAssistant

   # Local (alphabetical)
   from .api import make_api
   from .const import DOMAIN
   ```

2. **No Whitespace in Blank Lines** - Blank lines must be completely empty (no spaces/tabs)

3. **Run Before Committing**:
   - `ruff format .` - Format code
   - `ruff check .` - Validate style
   - `ruff check --fix .` - Auto-fix issues

## Translation Requirements

**From `.cursor/rules/econet300-specific.mdc`:**

When adding new entities, ALWAYS update all three translation files:
1. `custom_components/econet300/strings.json` - Base English strings
2. `custom_components/econet300/translations/en.json` - English translations
3. `custom_components/econet300/translations/pl.json` - Polish translations

Translation key naming rules:
- Must match pattern: `[a-z0-9-_]+` (lowercase only, no uppercase)
- Use snake_case conversion of entity keys (e.g., `mixerTemp1` → `mixer_temp1`)
- Check cloud translations first: `docs/cloud_translations/MANUAL_TRANSLATION_REFERENCE.md`

## Entity Creation Pattern

All entities follow this pattern in `const.py`:

```python
# Define entity key mapping (what data to read from API)
SENSOR_MAP_KEY = {
    "tempCO": "tempCO",  # Entity key: API response key
}

# Define units
ENTITY_UNIT_MAP = {
    "tempCO": UnitOfTemperature.CELSIUS,
}

# Define device class
ENTITY_SENSOR_DEVICE_CLASS_MAP = {
    "tempCO": SensorDeviceClass.TEMPERATURE,
}

# Define icon
ENTITY_ICON = {
    "tempCO": "mdi:thermometer",
}

# Define state class
STATE_CLASS_MAP = {
    "tempCO": SensorStateClass.MEASUREMENT,
}

# Define precision (for numeric values)
ENTITY_PRECISION = {
    "tempCO": 1,  # 1 decimal place
}
```

Binary sensors default to `device_class=RUNNING`. Only add to `ENTITY_BINARY_DEVICE_CLASS_MAP` if using a different class (e.g., `CONNECTIVITY` for network sensors).

## API Response Validation

**From `.cursor/rules/api-endpoint-validation.mdc`:**

ALWAYS check test fixtures before documenting or implementing new features:
- Fixtures are in `tests/fixtures/<device_type>/`
- Use fixture data as source of truth for API structure
- Verify entity types match actual JSON responses
- Never document without checking actual response examples

## Common Development Tasks

### Adding a New Sensor

1. Check fixture data in `tests/fixtures/` for the parameter
2. Add to `SENSOR_MAP_KEY` in `const.py`
3. Add unit, device class, icon, state class, precision to respective maps
4. Add translations to all three translation files
5. Run `ruff format .` and `ruff check .`
6. Test with `pytest`

### Adding a New Binary Sensor

1. Check fixture data
2. Add to `BINARY_SENSOR_MAP_KEY` in `const.py`
3. Add device class (if not RUNNING), icon, icon_off to respective maps
4. Add translations
5. Format and test

### Adding a New Number Entity (Setpoint)

1. Check if parameter is editable in fixture data (look for editParams or rmCurrentDataParamsEdits)
2. Add to `NUMBER_MAP` in `const.py` with min/max/step values
3. Add to other mapping dictionaries (unit, icon, precision)
4. Add translations
5. Implement `async_set_native_value()` in `number.py` if needed
6. Format and test

## Testing Strategy

- **Unit Tests**: `tests/test_*.py` - Mock API responses using fixture data
- **Fixture-Based Testing**: All tests use real API responses from `tests/fixtures/`
- **Integration Tests**: `test_init.py`, `test_diagnostics.py` - Test full integration lifecycle
- **Translation Tests**: `test_translations_comprehensive.py`, `test_icon_translations.py` - Validate translation completeness

## Pre-Commit Checklist

Before committing ANY changes:

1. ✅ Run `ruff format .`
2. ✅ Run `ruff check .` (must show no errors)
3. ✅ Check translations are updated (all 3 files)
4. ✅ Run `pytest` (all tests pass)
5. ✅ Verify no duplicate keys in const.py mappings
6. ✅ Verify imports are sorted correctly
7. ✅ Verify no whitespace in blank lines

## Git Workflow

Main branch: `master`

Commit message format:
```
feat: Add support for ecoMAX360i editParams endpoint

- Add editParams API endpoint handler
- Update entity mappings for new parameters
- Add translations for new entities
- Update test fixtures
```

Categories: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`

## Key Files Reference

- `custom_components/econet300/__init__.py` - Integration entry point, platform setup
- `custom_components/econet300/api.py` - All API communication logic
- `custom_components/econet300/common.py` - DataUpdateCoordinator
- `custom_components/econet300/const.py` - ALL entity definitions and mappings
- `custom_components/econet300/entity.py` - Base entity classes
- `custom_components/econet300/manifest.json` - Integration metadata
- `.cursor/rules/MASTER_RULES.md` - Master development guidelines
- `tests/fixtures/` - Real API responses for all supported devices

## Home Assistant Integration Standards

Follow HA development guidelines: https://developers.home-assistant.io/docs/development_index

Key patterns:
- Use `async_setup_entry()` for platform setup
- Implement proper entity lifecycle (`__init__` → `async_added_to_hass` → `async_will_remove_from_hass`)
- Use `DataUpdateCoordinator` for polling
- Handle errors with `ConfigEntryAuthFailed` and `ConfigEntryNotReady`
- Use `async_get_clientsession()` for HTTP requests

## Documentation Structure

- `README.md` - User-facing documentation, installation, configuration
- `CHANGELOG.md` - Version history and changes
- `docs/API_V1_DOCUMENTATION.md` - Complete API reference
- `docs/DIAGNOSTICS.md` - Diagnostics feature documentation
- `docs/devices/` - Device-specific documentation
- `scripts/README.md` - Development scripts documentation
