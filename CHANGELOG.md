# Changelog

## [v1.2.7a2] - 2026-05-03

### Fixed

- **`rmData` `NoneType` crash in `_lookup_cdp_value`**: Sensor entities no longer raise `AttributeError: 'NoneType' object has no attribute 'get'` when the `rmCurrentDataParams` endpoint returns `None` for a single coordinator update (transient device hiccup, malformed response, etc.). Root cause was fixed in `common.py` — the RM result loops now normalize both exceptions and `None` results to `{}`, so every key in `rm_data` is guaranteed to be a dict for downstream consumers. Sensor `_lookup_cdp_value` was also updated to use the defense-in-depth `or {}` pattern already used elsewhere in the file.

### Added

- **Diagnostics: raw probes** for endpoints the integration does not consume but whose response shape (or device-side error string) helps identify protocol/controller variants — `rmDeviceList`, `rmCurrentDataObject`, legacy `/sys`, `rmParamsData` without `uid`. Captured under `extended_endpoints.raw_probes` in every standard "Download diagnostics" file with HTTP status, body, and error preserved.
- **Diagnostics: "Generate diagnostics report" options-flow action** ([#231](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/231)): a new menu entry under Settings → Devices & Services → ecoNET300 → Configure that runs the full collection, writes a redacted JSON report to `homeassistant.log` with a unique marker (`ECONET300_DIAGNOSTICS_REPORT`), and raises a persistent notification with a triage-friendly summary (controllerID, protocolType, uid presence, regParams count, per-probe status). Lets users attach a complete report to a GitHub issue without searching for log files.
- **`Econet300Api.fetch_raw_endpoint()`** + **`EconetClient.probe_raw()`**: low-level diagnostic helpers that capture HTTP status + body for any `/econet/<endpoint>`, never collapsing a non-200 response or parse error to `None`. This is what surfaces the device-side error strings (e.g. `'Controller' object has no attribute 'onrmDeviceList'`) used by the new raw probes.

### Tests

- **+14 tests** in `tests/test_diagnostics.py` across three new classes:
  - `TestRawEndpointProbes` — verifies probe list covers issue #231 endpoints, uses correct paths, captures status + body, preserves device error payloads, isolates per-probe failures.
  - `TestApiRawEndpointHelper` — verifies URL construction with/without `uid`.
  - `TestDiagnosticsReportSummary` — verifies the persistent-notification summary surfaces controllerID/protocolType, reports `uid` presence, includes regParams count, reflects raw-probe statuses including errors, handles `None` sysParams defensively, includes the log marker.
- All 463 tests pass (was 449); 4 pre-existing skips unchanged.

### Translations

- **EN + PL** translations added for the new `diagnostics` options-flow step and menu label (`strings.json`, `translations/en.json`, `translations/pl.json`).

### Documentation

- **README**: extended `## 🔧 Diagnostics` with a "Generating a triage report" subsection covering the new action and the `raw_probes` block.

### Notes

- This is a **pre-release** (PEP 440 `a2`). HACS will not auto-prompt users on the stable channel. Install manually to test.

---

## [v1.2.7a1] - 2026-04-29

### Fixed

- **ecoMAX360i temperature sensors crash on `"off"` ([#227](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/227))**: `ActualFlowTemp`, `ActualReturnTemp`, `Circuit1DesiredLWT`, and other ecoMAX360i numeric sensors no longer raise `ValueError` when the heat-pump controller reports the literal string `"off"` from `informationParams` / `editParams`. A scoped `_numeric_or_none` value processor now coerces non-numeric API responses to `None`, so HA renders the entity as `unavailable` until a real numeric value arrives, instead of failing entity setup.

### Added

- **Regression test**: `TestEconetSensorBasic.test_ecomax360i_temperature_sensors_ignore_off_state` parametrized across `ActualFlowTemp`, `ActualReturnTemp`, and `Circuit1DesiredLWT` — verifies `process_val("off") is None` and numeric strings still convert to floats.

### Notes

- This is a **pre-release** (PEP 440 `a1`). HACS will not auto-prompt users on the stable channel. Install manually to test.

---

## [v1.2.6] - 2026-04-21

### Fixed

- **Dynamic select entities not saving changes** ([#225](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/225), [#224](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/224)): `EconetDynamicSelect.async_select_option` now calls `api.set_param_by_index` (the `rmNewParamIndex` endpoint) instead of `api.set_param`. Previously, dynamic select parameters that were not explicitly mapped in `RMNEWPARAM_PARAMS` / `NUMBER_MAP` / `CONTROL_PARAMS` (e.g. `Output H1` = 159, `Output H2 and H3` = 160, `Feeding time` = 28 on ecoMAX810P-L and equivalents on ecoMAX860P3-O / ecoMAX920P1-O) fell through to the default `newParamName=<numeric_id>` route, which the controller silently ignored — so UI changes never persisted. Static `heaterMode` (param `55`) was unaffected because it is explicitly listed in `RMNEWPARAM_PARAMS`.

### Added

- **Test fixture for `ecoMAX920P1-O`** under `tests/fixtures/ecoMAX920P1-O/` (18 JSON files + README) generated from real diagnostics via `scripts/create_fixture_from_diagnostics.py`; includes 20 dynamic-select candidates used to pin the fix above
- **Regression tests** (`TestDynamicSelectEntities` in `tests/test_dynamic_number_entities.py`): parametrized across `ecoMAX810P-L`, `ecoMAX860P3-O`, and `ecoMAX920P1-O` — asserts `set_param_by_index` is called (and `set_param` is not), verifies error handling for failed writes and invalid options

---

## [v1.2.5] - 2026-04-09

### Fixed

- **ecoSOL 301 / ecoSOL 500 sensors** ([#219](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/219)): Sensor platform now uses `ECOSOL_SENSORS` (`T1`, `P1`, `TzCWU`, etc.) when `controllerID` is an ecoSOL model, instead of boiler-only `DEFAULT_SENSORS` (which left critical sensors unavailable after v1.1.16)

### Added

- **Diagnostics**: `api_endpoint_data.extended_endpoints` — per-endpoint snapshots for RM API data (`rmParamsNames`, `rmParamsData`, `rmStructure`, `rmCurrentDataParams`, languages, locks, alarms, etc.) and optional **`editParams`**; failures are isolated so one timeout does not empty the rest
- **`fetch_edit_params`** / `API_EDIT_PARAMS_URI` for `GET /econet/editParams` (module-dependent; missing endpoints appear as `_ha_diagnostics_unavailable` in diagnostics)
- **`scripts/create_fixture_from_diagnostics.py`**: can emit `editParams.json`, `rmParamsNames.json`, and other RM fixture files from `extended_endpoints` when present
- **Tests**: `ecoSOL301` fixture folder and sensor mapping regression tests ([#219](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/219))

### Documentation

- **[MIGRATION.md](docs/MIGRATION.md)**: Troubleshooting for ecoSOL 301/500 sensors after upgrading from v1.1.16

---

## [v1.2.4] - 2026-03-24

### 🔧 Improvements

- **Alarm Event Translations**: Unified alarm event entity name to "Alarm" across all languages and added translated `state_attributes` for `alarm_triggered` / `alarm_cleared` event types (EN, PL, CZ, FR, UK)
- **Missing Alarm Translations**: Added `last_alarm`, `alarm_count`, `alarm_active`, and `boiler_alarm` translations for Czech, French, and Ukrainian — previously only English and Polish were covered

---

## [v1.2.3] - 2026-03-26

### ✨ New Features

- **Alarm Sensors** ([#71](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/71)): Real-time alarm monitoring from `sysParams.alarms` + `rmAlarmsNames`
  - **Last Alarm** sensor: shows the most recent alarm description with full details in attributes
  - **Alarm Count** sensor: total number of alarms with the 5 most recent in attributes
  - **Alarm Active** binary sensor: ON when any alarm is currently active (device class: `problem`)
  - **Boiler Alarm** event entity: fires `alarm_triggered` / `alarm_cleared` events for instant notification automations
- **Schedule Sensors** — **[Schedules Guide](docs/SCHEDULES.md)**: Auto-created sensor entities for every schedule configured on the device (boiler, water heater, mixers, thermostats, circulation pump, etc.)
  - **Native value**: Today's active-hours summary (e.g. `06:00-12:00, 20:00-00:00`)
  - **Attributes**: Per-day summaries (sunday–saturday) + schedule metadata — perfect for Markdown cards
  - **Dynamic**: Only schedules present on your device are created (no extra clutter)
  - **Translated**: EN, PL, FR, UK, CZ — 20 schedule types covered
  - **Icon**: `mdi:calendar-clock` for all schedule sensors
- **ecoMAX360i Sensors**: Added flap valve states, heat demanded, water pump running, Axen heat pump temperatures, circuit comfort/eco setpoints
- **Schedule Service**: New `econet300.get_schedule` service to read ecoMAX heating schedules (boiler, mixers, thermostats, water heater)

### 🔧 Improvements

- **API Throttling**: Added semaphore-based concurrency limit (max 3 parallel requests) to prevent overwhelming the ecoNET module ([#210](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/210))
- **Update Timeouts**: First update gets 120s timeout (cold cache), subsequent updates 30s
- **Legacy Number Entities**: Simplified fallback — mixer entities only (basic entities already created by `_create_basic_entities`)
- **PLATFORMS list**: Sorted alphabetically, added `Platform.EVENT`

### 📖 Documentation

- **[Alarms & Events Guide](docs/ALARMS_AND_EVENTS.md)** — entity details, automation examples (push notifications, persistent alerts, logbook logging)
- **[Schedules Guide](docs/SCHEDULES.md)** — how to display heating schedules on your dashboard

---

## [v1.2.2] - 2026-02-15

### ✨ New Features

- **Custom Entity Selector**: Create your own sensors and binary sensors from any parameter available on your ecoNET device — directly from the Home Assistant UI, no code changes needed
  - Choose from **regParams** (named parameters) or **regParamsData** (numeric IDs with names)
  - Configure each entity: friendly name, device group, entity type, category
  - For sensors: set unit, device class, and display precision
  - All custom entities appear immediately after saving

### 🐛 Bug Fixes

- **Fuel consumption sensor not working**: Fixed a race condition and unique ID mismatch that prevented `FuelConsumptionTotalSensor` from being created
- **Duplicate number entity IDs**: Dynamic entities from `mergedData` no longer collide with static number entities
- **"Unknown" state for custom entities**: Entities configured from `regParamsData` now correctly resolve their values
- **NoneType crash on startup**: Safely handle missing `regParams` data during initialization

### 🔧 Improvements

- Merged `regParamsData` and `rmCurrentDataParams` into a single endpoint for easier entity selection
- Enriched parameter labels showing names, units, and current values
- Static sensors and binary sensors automatically filtered from selection list to prevent duplicates
- Replaced all hardcoded `fuelStream` strings with `SENSOR_FUEL_STREAM` constant
- Updated README with new Custom Entity Selector screenshots

---

## [v1.2.1] - 2026-02-24

### 🚀 New Features

- **Fuel Consumption Tracking**: New `fuel_consumption_total` sensor that tracks total fuel usage in kg
  - Integrates the `fuelStream` rate sensor (kg/h) over time using trapezoidal method
  - Persists across Home Assistant restarts
  - New services: **Reset meter** and **Calibrate meter** to manage the counter
- **Legacy Device Support**: Automatic detection of devices that don't support RM endpoints
  - Devices without RM API support (older firmware) are now handled gracefully
  - No more errors or timeouts for legacy modules

### 🐛 Bug Fixes

- **Boiler ON/OFF Switch Not Updating**: Fixed bug where the switch stopped updating after initial load
  - Switch now correctly reflects boiler state on every poll cycle
  - Manually turning off the boiler is now properly detected
- **Boiler Switch State Logic**: Improved ON/OFF detection using operation mode mapping
  - Unknown or unexpected mode values now safely default to OFF

### 📦 New Device Support

- Added test fixtures for **ecoMAX860D3-HB**
- Added test fixtures for **ecoMAX860P3-O**
- Added test fixtures for **ecoMAX360-cf8**
- Added test fixtures for **SControl EM892**

---

## [v1.2.0] - 2025-01-28

### 🚀 New Features

- **Dynamic Entity System**: Complete rewrite of entity creation from `mergedData` API
  - 165+ dynamic parameters from boiler's remote menu
  - Automatic entity type detection (Number, Switch, Select, Sensor)
  - Category-based entity grouping with smart defaults (CONFIG entities disabled by default)

- **Mixer Device Support**: Entities correctly assigned to mixer devices (Mixer 1-4)
  - Keyword-based detection for mixer-related entities (`MIXER_RELATED_KEYWORDS`)
  - Hardware validation to prevent phantom mixer devices

- **ecoSTER Panel Detection**: Smart filtering for ecoSTER-related entities
  - Entities only created when ecoSTER panel is connected (`ecoster_exists()`)

- **Parameter Locking**: Device-side parameter locks reflected in Home Assistant
  - Lock icon (`mdi:lock`) displayed for locked parameters
  - Lock reason shown in entity attributes

- **Transmission State Mappings**: Added complete transmission state support
  - 14 boiler operation modes with proper state mappings
  - Multi-language translations (EN, PL, FR) for all modes
  - Icons and state translations in `icons.json`

- **Expanded Boiler Status Codes**: Complete support for all 27 known boiler operation status codes
  - Added all status codes from ecoNET cloud JavaScript to `SENSOR_STATUS_CO_MAPPING`
  - New status codes: `prevention` (16), `work_grate` (17), `supervision_grate` (18), `calibration` (19), `maintain` (20), `afterburning` (21), `chimney_sweep` (22), `heating` (23), `open_door` (24), `cooling` (25), `safe` (26)

- **Repair Issues System** (Gold tier `repair-issues` rule)
  - Connection Failure Detection: Automatically detects persistent connection failures (after 5 consecutive failures)
  - User-Friendly Repairs: Repair issues appear in **Settings → System → Repairs** with clear descriptions
  - One-Click Fix: Users can update connection settings directly from the Repairs UI
  - Auto-Resolution: Repair issues automatically removed when connection is restored

- **Reconfiguration Flow** (Gold tier `reconfiguration-flow` rule)
  - Options Flow: Added ability to reconfigure host, username, and password after initial setup
  - Easy Access: Available via integration options (gear icon) in Settings → Devices & Services
  - Validation: Connection is validated before applying changes

### 🐛 Bug Fixes

- **Number Entity Min/Max**: Fixed initialization to properly handle `0.0` as valid minimum value
- **Heating Curve Values**: Fixed value setting - now correctly sends float values to API via `set_param_by_index()`
- **Boiler On/Off Switch**: Fixed state reading from `regParams.mode` instead of incorrect path
- **Entity Icons**: Fixed `icons.json` translations using `_attr_has_entity_name` attribute
- **Switch Entity Init**: Fixed `async_write_ha_state()` called before entity added to Home Assistant
- **Entity Registry Default**: Reverted property-based `entity_registry_enabled_default` to maintain compatibility
- **moduleEcoSTERSoftVer**: Fixed incorrect treatment as numeric sensor (#189)
- **Dynamic Entity Limits**: Skip API limits lookup for entities with pre-set limits from mergedData (reduces log spam)

### 🔧 Improvements

- **Number Entity Input Mode**: Changed basic NUMBER_MAP entities from slider to input box for easier value entry

### ⚙️ Technical Improvements

- **API Enhancement**: New `set_param_by_index()` method for dynamic parameter editing
- **Entity Registry**: CONFIG category entities disabled by default, DIAGNOSTIC/uncategorized enabled
- **Code Quality**: Refactored mixer keywords to `MIXER_RELATED_KEYWORDS` constant in `const.py`
- **Validation Layer**: Centralized parameter validation in `common_functions.py`
  - `validate_parameter_data()`, `is_parameter_locked()`, `get_lock_reason()`
  - `should_be_number_entity()`, `should_be_switch_entity()`, `should_be_select_entity()`
- **Component Detection**: `get_validated_entity_component()` with hardware validation
- **Entity Setup**: Enhanced setup process to ensure registration for updates even when coordinator data unavailable
- **Failure Tracking**: Coordinator now tracks consecutive connection failures
- **Issue Registry Integration**: Uses Home Assistant's native issue registry for repairs
- **Entry Cleanup**: Repair issues automatically cleaned up when integration is removed
- **PARALLEL_UPDATES**: Added constant for polling integration compliance
- **CI Updates**: Updated `actions/checkout` from v4 to v6 in GitHub workflows

### 🌐 Translation Updates

- **Status Code Translations**: Added translations for all 27 status codes in 5 languages (English, Polish, French, Ukrainian, Czech)
- **Repair Issue Translations**: Added translations for repair issues in all 5 languages

### 🧪 Testing

- New tests for `async_remove_entry` and repair issue cleanup
- Updated tests for switch exception handling and dynamic number entity key generation

### 📚 Documentation

- Added `docs/DYNAMIC_ENTITY_VALIDATION.md` for dynamic entity system
- **Boiler Operation Mode Reference**: Complete mapping table with 14 operation modes
- Updated API documentation with 80+ discovered endpoints
- Enhanced cursor rules for dynamic entity changes
- Improved bug report template with dropdown device selection

---

## [v1.1.16] - 2025-12-29

### 🚀 New Features

- **Reconfigure Flow**: You can now update your ecoNET300 connection settings (IP address, username, password) without removing the integration!
  - **How to use**: Settings → Devices & Services → ecoNET300 → ⋮ → Reconfigure
  - **Use case**: After power outages, if your device gets a new IP address, just reconfigure — no data loss!
  - **Translations**: Available in English, Polish, Czech, French, and Ukrainian
  - **Files Modified**: `config_flow.py`, `strings.json`, all translation files

### 🐛 Bug Fixes

- **#187 - Sensors Not Refreshing**: Fixed critical bug where mixer and other sensors stopped updating automatically
  - **Problem**: If initial data was missing, entities never registered with the coordinator for updates
  - **Solution**: Moved `super().async_added_to_hass()` to run first, ensuring entities always register for updates
  - **Impact**: All sensors (especially mixers) now refresh automatically every 30 seconds
  - **Files Modified**: `entity.py`

- **#189 - Firmware Version ValueError**: Fixed error when ecoSTER/ecoSRV firmware versions caused crashes
  - **Problem**: `moduleEcoSTERSoftVer` and `ecosrvSoftVer` values like `'1.25.90'` were incorrectly treated as numeric
  - **Solution**: Added these keys to `ENTITY_PRECISION` with `None` value to mark them as non-numeric
  - **Impact**: No more `ValueError: could not convert string to float` errors in logs
  - **Files Modified**: `const.py`

### 📋 Issue Form Improvements

- **Bug Report Form**: Simplified device selection (dropdown instead of checkboxes), removed "How to reproduce?", added diagnostics upload instructions with [HA docs link](https://www.home-assistant.io/integrations/diagnostics/)
- **Feature Request Form**: Replaced long "New Sensor" form with a generic, simplified "Feature Request" form that works for any feature type

### 🔧 Technical Changes

- **Home Assistant Version**: Updated minimum requirement to `>=2025.2.2`
- **Config Flow**: Updated docstrings from "Example Integration" to "ecoNET300 Integration"

---

## [v1.1.15] - 2025-01-13

### New Features

- **Universal Select Entity System**: Implemented dynamic select entity creation with camel_to_snake conversion
  - **Dynamic Configuration**: Select entities now created from `const.py` mappings instead of hardcoded definitions
  - **Camel Case Support**: API parameters use camelCase format (`heaterMode`) with automatic snake_case conversion for entity IDs
  - **Scalable Architecture**: Easy to add new select entities by updating `SELECT_KEY_SET`, `SELECT_KEY_STATE`, and `SELECT_KEY_VALUES`
  - **Files Modified**: `custom_components/econet300/select.py`, `custom_components/econet300/const.py`

### Bug Fixes

- **Select Entity Translation Display**: Fixed issue where raw values were shown instead of translated text
  - **Problem**: Option values in dictionary were lowercase (`"summer"`) but translations expected Title Case (`"Summer"`)
  - **Solution**: Updated all option values to use Title Case consistently across all files
  - **Impact**: UI now displays proper translations (e.g., "Summer" instead of "summer")
  - **Files Modified**: `const.py`, `icons.json`, `strings.json`, all translation files

- **Select Entity Option Conversion**: Fixed dictionary lookup errors in option value conversion
  - **Problem**: Legacy functions used wrong dictionary keys (`"heater_mode"` vs `"heaterMode"`)
  - **Solution**: Updated `get_heater_mode_value()` and `get_heater_mode_name()` to use correct camelCase keys
  - **Impact**: Select entity option changes now work correctly (e.g., changing to "Summer" mode)
  - **Files Modified**: `custom_components/econet300/select.py`

- **Translation Case Consistency**: Fixed case mismatch between option values and translation keys
  - **Problem**: Dictionary values and translation keys had different case formats
  - **Solution**: Standardized all option values to Title Case format
  - **Impact**: Proper translation display in all supported languages
  - **Files Modified**: All translation files (`en.json`, `pl.json`, `fr.json`, `uk.json`)

### Technical Improvements

- **Code Cleanup**: Reduced verbose debug logging while preserving essential troubleshooting information
  - **Removed**: 9 verbose debug logs that cluttered output
  - **Kept**: 25 essential debug logs for troubleshooting
  - **Benefits**: Cleaner logs, better performance, easier debugging
  - **Files Modified**: `custom_components/econet300/select.py`

- **Icon System Optimization**: Centralized icon management in `icons.json` file
  - **Removed**: Duplicate icon mappings from `const.py`
  - **Centralized**: All icon definitions now in `icons.json` following Home Assistant best practices
  - **State-Specific Icons**: Select options now have proper state-specific icons
  - **Files Modified**: `custom_components/econet300/const.py`, `custom_components/econet300/icons.json`

- **Translation Structure**: Updated translation format to use proper Home Assistant `options` structure
  - **Before**: Separate translation keys for each option (`heater_mode_winter`, `heater_mode_summer`)
  - **After**: Proper `options` structure with option keys (`Winter`, `Summer`, `Auto`)
  - **Benefits**: Better Home Assistant integration, cleaner translation files
  - **Files Modified**: All translation files

### Multi-language Support

- **Enhanced Select Entity Translations**: Added comprehensive translations for select entity options
  - **English**: Winter, Summer, Auto
  - **Polish**: Zima, Lato, Auto
  - **French**: Hiver, Été, Auto
  - **Ukrainian**: Зима, Літо, Авто
  - **Files Modified**: All translation files (`en.json`, `pl.json`, `fr.json`, `uk.json`)

## [v1.1.14] - 2025-01-10

### New Features

- **Multi-language Support**: Added comprehensive translation support for 6 languages
  - **Czech (cs)**: Complete translation coverage with 348 parameters
  - **French (fr)**: Complete translation coverage with 876 parameters
  - **Ukrainian (uk)**: Complete translation coverage with 855 parameters
  - **Enhanced Testing**: Updated all translation test scripts to validate all 6 languages
  - **Cloud Integration**: Translations sourced from official ecoNET cloud reference
  - **Files Added**: `custom_components/econet300/translations/cz.json`, `fr.json`, `uk.json`
  - **Files Updated**: `scripts/check_translations.py`, `tests/test_translations_comprehensive.py`

### Bug Fixes

- **Type Compatibility Error**: Fixed MyPy type checking error in sensor platform
  - **Problem**: `gather_entities` function had incompatible type annotations causing MyPy errors
  - **Solution**: Updated return type from `list[EconetSensor]` to `list[SensorEntity]` to accommodate all sensor types
  - **Impact**: Resolves type compatibility issues with MixerSensor, LambdaSensors, and EcoSterSensor entities
  - **Files Modified**: `custom_components/econet300/sensor.py`
  - **Technical Details**: Changed function signature to use base `SensorEntity` type instead of specific `EconetSensor` type

### Technical Improvements

- **Type Safety**: Improved type annotations for better code maintainability
  - **Before**: Function expected only `EconetSensor` entities but was receiving mixed sensor types
  - **After**: Function properly handles all sensor entity types through base class inheritance
  - **Benefits**: Better type safety, cleaner code, and proper MyPy compliance

## [v1.1.13] - 2025-09-03

### Added

- **Integration Diagnostics Support**: Added comprehensive diagnostics functionality for troubleshooting
  - **Config Entry Diagnostics**: Download detailed configuration and system information
  - **Device Diagnostics**: Download device-specific information including entity states and API data
  - **Sensitive Data Protection**: Automatic redaction of sensitive information (passwords, UIDs, network details)
  - **API Endpoint Data**: Raw data from all API endpoints (sysParams, regParams, regParamsData, paramEditData)
  - **Entity Information**: Current values, units, and attributes for all entities
  - **Integration Version**: Version information included in diagnostics output
  - **Error Handling**: Robust error handling with graceful degradation
  - **File Structure**: Diagnostics functionality properly separated into dedicated `diagnostics.py` file
  - **Comprehensive Documentation**: Complete diagnostics guide with troubleshooting instructions and usage examples

### Implementation Details

- **New File**: `custom_components/econet300/diagnostics.py` - Dedicated diagnostics module
- **New Documentation**: `docs/DIAGNOSTICS.md` - Comprehensive diagnostics documentation and troubleshooting guide
- **Diagnostics Implementation**: Implemented `async_get_config_entry_diagnostics` and `async_get_device_diagnostics` functions
- **Comprehensive Testing**: Added test coverage for diagnostics functionality
- **Code Quality**: Fixed linting issues and improved error handling
- **Security**: Implemented sensitive data redaction for device UIDs, passwords, API keys, and network information
- **Documentation**: Updated README.md with diagnostics section and link to detailed documentation

## [v1.1.12] - 2025-09-03

### v1.1.12 New Features

- **Summer/Winter/Auto Mode Control**: Added comprehensive heater mode selection functionality
  - **New Select Entity**: `select.heater_mode` for controlling boiler operation modes
  - **Three Operation Modes**:
    - **Winter Mode** (0): Full heating operation for cold weather
    - **Summer Mode** (1): Hot water only operation for warm weather
    - **Auto Mode** (2): Automatic mode selection based on conditions
  - **API Integration**: Direct control via ecoNET API parameter 55
  - **State Management**: Real-time mode synchronization with boiler controller
  - **Logging**: Comprehensive logging for mode changes with context for Home Assistant logbook

### v1.1.12 Improvements

- **API Parameter Handling**: Enhanced API parameter handling for better reliability
  - **Endpoint Mapping**: Improved parameter endpoint mapping for different parameter types
  - **Error Handling**: Better error handling and validation for parameter changes
  - **State Synchronization**: Improved state synchronization between Home Assistant and boiler controller

### v1.1.12 Implementation Details

- **Select Platform**: Added new `select.py` platform for mode selection entities
- **Constants**: Added `HEATER_MODE_VALUES` and `HEATER_MODE_PARAM_INDEX` constants
- **Translation System**: Integrated heater mode options with Home Assistant translation system
- **API Methods**: Enhanced `set_param()` method to handle different parameter types
- **Entity Management**: Added proper entity lifecycle management for select entities

## [v1.1.10] - 2025-08-30

### v1.1.10 New Features

- **Modern Icon Translation System**: Implemented comprehensive icon management using Home Assistant's recommended approach
  - **New Icon Management**: All icons now managed through `icons.json` with proper translation keys
  - **State-Based Icons**: Added dynamic icons that change based on entity state (status_co, status_cwu, mode, lambda_status)
  - **Multi-Language Support**: Icons properly integrated with translation system for internationalization
  - **Icon Validation**: All Material Design Icons validated and replaced invalid ones with proper alternatives

### v1.1.10 Architecture Changes

- **Icon System Architecture**: Replaced old icon constants with modern translation-based approach
  - **Before**: Icons defined in `const.py` as hardcoded constants
  - **After**: Icons managed in `icons.json` with translation key mapping
  - **Benefits**: Better maintainability, easier customization, Home Assistant best practices compliance

- **Pre-commit Configuration**: Streamlined development workflow
  - **Removed**: codespell hook that was causing false positives
  - **Kept**: ruff (linting), ruff-format (formatting), mypy (type checking)
  - **Impact**: Cleaner, faster pre-commit checks with focus on essential quality metrics

### v1.1.10 Bug Fixes

- **Invalid Material Design Icons**: Resolved 20+ non-existent icon references
  - **Problem**: Many icons like `mdi:screw-lag`, `mdi:fire-off`, `mdi:gauge-off` didn't exist in MDI database
  - **Solution**: Replaced with valid alternatives like `mdi:gauge`, `mdi:fire`, `mdi:conveyor-belt`
  - **Impact**: All entities now display proper icons in Home Assistant UI

- **Icon Display Issues**: Fixed entities not showing icons in UI
  - **Problem**: Some entities like `feeder_works` and `contact_gzc` had missing or broken icons
  - **Solution**: Implemented proper translation key mapping and icon validation
  - **Impact**: Consistent icon display across all entity types

## [v1.1.9] - 2025-08-27

### v1.1.9 Improvements

- **Logging Level Refactoring**: Major refactoring of logging levels throughout the integration
- **VS Code Settings Optimization**: Streamlined development environment configuration

### v1.1.9 Bug Fixes

- **Git Pre-commit Hook Issues**: Fixed file formatting issues that caused pre-commit hook failures
  - **Problem**: Pre-commit hooks were failing due to trailing whitespace and end-of-file formatting
  - **Solution**: Cleaned up file formatting to meet git hook requirements
  - **Impact**: All pre-commit hooks now pass successfully, ensuring code quality
  - **Files Modified**: `.vscode/settings.json`

### v1.1.9 Technical Changes

- **Logging Refactoring**: Systematic review and adjustment of log levels across the codebase
- **VS Code Configuration**: Streamlined Ruff settings to use native VS Code support
- **Git Hooks**: Ensured all pre-commit hooks pass for consistent code quality
- **Development Environment**: Cleaner, more maintainable VS Code configuration
- **Code Quality**: Improved logging practices for better debugging and monitoring

## [v1.1.8] - 2025-08-11

### Critical Fixes

- **Critical Error Resolution**: Fixed `TypeError: argument of type 'NoneType' is not iterable` error
  - **Problem**: System crashed when controllers didn't support `rmCurrentDataParamsEdits` endpoint
  - **Solution**: Added controller-specific endpoint support detection and comprehensive safety checks
  - **Impact**: No more crashes for ecoSOL500, ecoSOL, SControl MK1, and ecoMAX360i controllers
  - **Files Modified**: `custom_components/econet300/api.py`, `common.py`, `entity.py`

- **API Endpoint Error**: Fixed `Data for key: data does not exist in endpoint: rmCurrentDataParamsEdits` error
  - **Problem**: API calls to unsupported endpoints caused system failures
  - **Solution**: Implemented proactive controller detection to skip unsupported endpoints
  - **Impact**: Better performance and stability for all controller types
  - **Files Modified**: `custom_components/econet300/common.py`

### v1.1.8 New Features

- **Controller-Specific Endpoint Support**: Added intelligent detection of endpoint compatibility
  - **Supported Controllers**: ecoMAX series (810P-L, 850R2-X, 860P2-N, 860P3-V)
  - **Unsupported Controllers**: ecoSOL500, ecoSOL, SControl MK1, ecoMAX360i
  - **Smart Detection**: System automatically detects controller type and skips incompatible endpoints
  - **Performance Improvement**: No unnecessary API calls to unsupported endpoints

- **Comprehensive Safety Checks**: Added multiple layers of protection against None values
  - **API Level**: Ensures `fetch_param_edit_data()` always returns dict, never None
  - **Entity Level**: Double-checks params_edits is always a dict before processing
  - **Logging**: Clear warnings when unexpected None values are encountered
  - **Graceful Degradation**: System continues working even when endpoints are unavailable

### v1.1.8 Improvements

- **Error Handling Strategy**: Changed from reactive error handling to proactive endpoint detection
  - **Before**: Made API calls first, then handled errors when they occurred
  - **After**: Check controller compatibility first, then make only supported API calls
  - **Benefits**: Faster startup, better performance, no crashes, cleaner logs

### v1.1.8 Implementation Details

- **skip_params_edits Function**: Enhanced to detect all unsupported controller types
- **Safety Checks**: Added multiple validation layers in entity update methods
- **Documentation**: Updated API documentation with controller-specific endpoint information
- **Code Quality**: Improved error handling and logging throughout the system

## [v1.1.7] - 2025-08-08

### v1.1.7 Bug Fixes

- **Entity Category Mapping**: Fixed binary sensor entity categories for better UI organization
  - **Problem**: Diagnostic entities like 'lan', 'wifi', 'mainSrv' were showing in Sensors section instead of Diagnostics
  - **Solution**: Added explicit entity_category property to EconetBinarySensor class and proper type annotations
  - **Impact**: Diagnostic entities now appear in the correct Diagnostics section in Home Assistant UI
  - **Files Modified**: `custom_components/econet300/binary_sensor.py`
  - **Technical Details**: Added EntityCategory import and explicit entity_category property with proper type annotations

### v1.1.7 Implementation Details

- **Type Annotations**: Fixed mypy type checking errors for \_attr_is_on property
- **Entity Category Property**: Added explicit entity_category property to ensure proper category inheritance
- **Code Quality**: All pre-commit checks pass including mypy static type checking

## [v1.1.6] - 2025-08-08

### v1.1.6 New Features

- **ecoSOL500 Solar Collector Support**: Added comprehensive support for ecoSOL500 solar collector controller
  - **New Device Type**: Full integration with ecoSOL500 solar collector capabilities
  - **Temperature Sensors**: Added support for T1-T6 temperature sensors (collector, tank, return temperatures)
  - **Hot Water Temperature**: Added TzCWU sensor for hot water temperature monitoring
  - **Pump Status Sensors**: Added P1 and P2 pump status sensors
  - **Output Status**: Added H output status sensor
  - **Heat Output**: Added Uzysk_ca_kowity (total heat output) sensor with percentage unit
  - **Test Fixtures**: Added complete test fixtures for ecoSOL500 validation
  - **Translation Support**: Added proper translations for all ecoSOL500 sensors

### v1.1.6 Bug Fixes

- **Entity Category Mapping**: Fixed binary sensor entity categories for better UI organization
  - **Problem**: Diagnostic entities like 'lan', 'wifi', 'mainSrv' were showing in Sensors section instead of Diagnostics
  - **Solution**: Added proper entity_category mapping in binary sensor creation
  - **Impact**: Diagnostic entities now appear in the correct Diagnostics section in Home Assistant UI
  - **Files Modified**: `custom_components/econet300/binary_sensor.py`

### v1.1.6 Development Tools

- **Code Quality Tools**: Enhanced development workflow with professional code quality tools
  - **Pre-commit Hooks**: Added comprehensive pre-commit configuration with debug statement prevention and docstring checks
  - **Type Checking**: Added mypy static type checking with proper dependencies
  - **Security Analysis**: Added CodeQL security analysis workflow for automated vulnerability detection
  - **Files Modified**: `.pre-commit-config.yaml`, `.github/workflows/codeql.yml`

### v1.1.6 Implementation Details

- **Constants Organization**: Added ecoSOL500-specific sensor mappings, device classes, units, and icons
- **Entity Creation Logic**: Improved entity category handling for better UI organization
- **Development Standards**: Enhanced code quality with automated linting, formatting, and security checks
- **Documentation**: Updated development workflow with professional standards

## [v1.1.5] - 2025-08-06

### v1.1.5 New Features

- **ecoMAX850R2-X Support**: Added comprehensive support for the new ecoMAX850R2-X boiler controller
  - **New Device Type**: Full integration with ecoMAX850R2-X controller capabilities
  - **ecoSTER Thermostat Support**: Added support for up to 8 ecoSTER room thermostats
  - **Enhanced Sensor Support**: Added new sensors specific to ecoMAX850R2-X (fuelConsum, fuelStream, tempBack, transmission)
  - **Documentation**: Created comprehensive documentation for ecoMAX850R2-X features and capabilities
  - **Test Fixtures**: Added complete test fixtures for ecoMAX850R2-X validation

### v1.1.5 Bug Fixes

- **statusCO Sensor Translation**: Fixed missing translation for statusCO sensor causing "PLUM ecoNET300" display issue
  - **Problem**: statusCO sensor was missing translation key in sensor section
  - **Solution**: Added status_co translation to all translation files (strings.json, en.json, pl.json)
  - **Impact**: statusCO sensor now displays as "Central heating status" instead of raw translation key
  - **Files Modified**: Translation files in sensor section

### v1.1.5 Architecture Changes

- **ecoSTER as Separate Devices**: Refactored ecoSTER thermostats to be separate Home Assistant devices
  - **Device Structure**: Each ecoSTER thermostat (1-8) now appears as a separate device under the main controller
  - **Entity Organization**: ecoSTER sensors and binary sensors are properly grouped by thermostat
  - **Module Detection**: ecoSTER entities only created when moduleEcoSTERSoftVer is present in sysParams
  - **Files Modified**: `custom_components/econet300/entity.py`, `sensor.py`, `binary_sensor.py`

### v1.1.5 Implementation Details

- **Constants Organization**: Reorganized sensor and binary sensor mappings for better device-specific support
- **Translation Validation**: Added comprehensive validation logic and commit workflow documentation
- **Entity Creation Logic**: Improved module detection and entity filtering for ecoSTER devices
- **Documentation**: Updated cursor rules with validation guidelines and commit workflow

## [v1.1.4] - 2025-01-XX

### Version Update

- **Version Update**: Updated version to 1.1.4

## [v1.1.3] - 2025-07-15

### v1.1.3 New Features

- **Mixer Temperature Setpoints**: Added support for mixer temperature setpoints 1-6
  - **New Number Entities**: mixerSetTemp1 through mixerSetTemp6 (parameters 1287-1292)
  - **Translation Support**: Added proper translations for all mixer setpoints in English and Polish
  - **Smart Entity Creation**: Only creates entities for mixers that exist on your specific boiler model
  - **Files Modified**: `custom_components/econet300/const.py`, translation files

### v1.1.3 Improvements

- **Exception Handling**: Improved debugging by using general exception handling during development
  - **Better Error Visibility**: Catches all possible errors to help identify issues during testing
  - **Development Friendly**: Easier to debug unexpected API responses or network issues
  - **Files Modified**: `custom_components/econet300/api.py`

### v1.1.3 Implementation Details

- **NUMBER_MAP**: Added mixer temperature setpoints 1287-1292
- **Translation Files**: Updated strings.json, en.json, and pl.json with mixer setpoint translations
- **Entity Creation Logic**: Existing logic automatically handles null values (mixers that don't exist)
- **GitHub Actions**: Added CI workflow with translation checks, tests, and linting

## [v1.1.2] - 2025-01-XX

### v1.1.2 Critical Fixes

- **Temperature Control API Endpoint**: Fixed incorrect API endpoint for temperature setpoints
  - **Problem**: Integration was using `/econet/rmNewParam?newParamIndex={param}` which doesn't work
  - **Solution**: Changed to `/econet/rmCurrNewParam?newParamKey={param}` which is the correct endpoint
  - **Impact**: Boiler temperature setpoints, hot water setpoints, and mixer temperature controls now work correctly
  - **Files Modified**: `custom_components/econet300/api.py`
  - **Technical Details**: Updated `set_param()` method to use correct endpoint format for NUMBER_MAP parameters

### v1.1.2 Implementation Details

- **API Endpoint**: Changed from `rmNewParam` to `rmCurrNewParam` for temperature setpoints
- **Parameter Format**: Changed from `newParamIndex` to `newParamKey` for temperature parameters
- **Affected Parameters**: All temperature setpoints (1280=tempCOSet, 1281=tempCWUSet, 1287-1292=mixerSetTemp1-6)
- **Backward Compatibility**: No breaking changes, only fixes non-working functionality

## Version History Summary

### Key Versions

- **v0.3.3** - Stable version by @pblxpt (original developer)
- **v1.0.0** - Development version with enhanced API data retrieval
- **v1.1.1** - Added boiler ON/OFF control switch functionality
- **v1.1.3** - Critical fixes for temperature control and mixer setpoints
- **v1.1.13** - Added comprehensive diagnostics support for troubleshooting
- **v1.2.0** - Dynamic entity system, mixer support, parameter locking
- **v1.2.1** - Fuel consumption tracking, legacy device support
- **v1.2.2** - Custom Entity Selector, fuel sensor fixes
- **v1.2.3** - Alarm monitoring, schedule sensors, ecoMAX360i sensors, API throttling
