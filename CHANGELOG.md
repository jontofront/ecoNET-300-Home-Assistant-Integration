# v0.1.0

## Added (6)

* [Entity/Sensor] Added `feeder temperature`
* [Entity/Sensor] Added `fan power`
* [Entity/Sensor] Added `exhaust emperature`
* [Entity/Sensor] Added `fireplace temperature`
* [Entity/Sensor] Added `water back temperature`
* [Entity/Sensor] Added `water temperature`
* [Entity/Sensor] Added `outside temperature`
* [Entity/Sensor] Added `boiler power output`
* [Entity/BinarySensor] Added `water pump works`
* [Entity/BinarySensor] Added `fireplace pump works`
* [Entity/BinarySensor] Added `solar pump works`
* [Entity/BinarySensor] Added `lighter works`
* [Config] Added config via GUI

## v0.1.1

Add new sensors and binary sensor
Add hardware version

## v0.1.5

* [Entity/Sensor] Added `lambdaLevel`
* [Entity/Sensor] Added `Wi-Fi signal strength`
* [Entity/Sensor] Added `Wi-Fi signal quality`
* [Entity/Sensor] Added `Module ecoNET software version`
* [Entity/Sensor] Added `Module A version`
* [Entity/Sensor] Added `Module B version`
* [Entity/Sensor] Added `Module Panel version`
* [Entity/Sensor] Added `Module Lambda version`

## v0.1.6

fix error in Entity sensor.wi_fi_signal_quality

## v0.1.7

Added `Thermostat sensor` ON or OFF
Added `lambdaStatus`
Added `mode` boiler operation names to status

## v0.1.7-3

Rename boiler mode names
Added `protocol_Type` to DIAGNOSTIC sensor
Added `controllerID` to DIAGNOSTIC sensor

## v0.1.8

Added REG_PARAM_PRECICION parameters from econet dev file
Added translations for the sensors
Added translations dictonary
By default sensors off: Fan2, Solar pump, Fireplace pump
Changed depricated unit TEMP_CELSIUS to UnitOfTemperature.CELSIUS

## [v0.3.0] 2023-11-30

Thank for @pblxptr add new code line from him

* Added: [New features boiler set temperature]
* Added: [Mixer sensor new device]
* Added: [Comments in code]
* Added: [Configuration in project code style by HA rules]

## [v0.3.1] 2023-12-04

* Rename: `tempCWU` sensor name from `water temperature` to `HUW temperature`
* Rename:  `pumpCO` binary_sensor name from `Pump` to `Boiler pump`
* Added: `HUW temperature` sensor key `tempCWUSet`
* Added: `Upper buffer temperature` sensor (by defoult off)

## [v0.3.3] 2023-12-14

* Change readme pictures links
* cleaned translation files and rename keys by requrements
* Added: alarm constants for future

## [v1.0.0-beta-11] 2024-10-03

* Added: `boiler_status` sensor
* Added: `boiler_status` binary_sensor
* Added: `boiler_status` sensor key `boiler_status`
* Added: `boiler_status` binary_sensor key `boiler_status`
* Added: `boiler_status` sensor key `boiler_status_text`
* Added: `boiler_status` binary_sensor key `boiler_status_text`

## [v1.0.1-beta] 2024-10-03

* Small code changes update repo

## [v1.0.2-beta] 2024-10-15

* Tests file structure according to documentation
* Code style chcnges by ruff recomendation
* Separated entity by types for better management
* Moved Mixer sensors to the Mixer sensor group and added icons

## [v1.0.3-beta] 2024-10-15

### Added

* Introduced new `ServoMixer1` state handling with predefined Home Assistant states (`STATE_OFF`, `STATE_CLOSING`, `STATE_OPENING`).
* Added logging for non-numeric values in sensor processing to improve debugging.

### Changed

* Updated `ENTITY_VALUE_PROCESSOR` to use predefined Home Assistant states for `ServoMixer1`.
* Improved error handling in `create_controller_sensors` to skip non-numeric values and log warnings.

### Fixed

* Fixed `ValueError` caused by non-numeric values in sensor state processing.
* Resolved Mypy type incompatibility issue in `STATE_CLASS_MAP` by removing the `servoMixer1` entry with `None` value.

## [v1.0.4-beta] 2024-11-04

### New Features

* **New Sensors Added**: Introduced new sensors for enhanced monitoring.
  * Added sensors: workAt100, workAt50, workAt30, FeederWork, FiringUpCount. (Commit: e41f882)

### Improvements

* **Valve State Constant**: Changed the valve STATE constant for better consistency. (Commit: 3835797)
* **Entity Value Processor**: Updated ENTITY_VALUE_PROCESSOR to use STATE_ON and STATE_OFF constants for improved state handling. (Commit: 17959c6)
* **Controller Name**: Added 'Controller name' to 'model_id' device info for better support and identification. (Commit: b5cf889)

### Bug Fixes

* **Boiler Status Keys**: Fixed the mapping of boiler status keys to include operation status. (Commit: a486402)

## [v1.0.4] 2024-12-09

### New Features

* **Endpoint Creation**: Testing out new way of creating entities from endpoint in [#22](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/22)
* **Endpoint Rewrite**: Feature rewrite endpoint and logic extended in [#40](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/40)
* **Endpoint Rewrite**: Feature rewrite endpoint and logic extended in [#43](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/43)
* **Translatable States**: Translatable boiler mode and lambda states by @denpamusic in [#47](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/47)
* **ServoMix1 HA States**: Add ServoMix1 HA states by @jontofront in [#76](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/76)

### Improvements

* **Entity Creation**: Testing out new way of creating entities from endpoint in [#22](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/22)
* **Code Alterations**: Made alterations to some code in [#42](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/42)
* **Inheritance Fix**: Fix inheritance in entity classes by @denpamusic in [#45](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/45)
* **Cleanup**: Moved camel case function to separate file and performed clean up in [#46](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/46)
* **Repository Update**: Updated repository by @jontofront in [#65](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/65)
* **Repository Update**: Updated repository by @jontofront in [#66](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/66)
* **Frozen Removal**: Remove frozen=True by @jontofront in [#67](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/67)
* **Code Changes**: Small code changes update repo by @jontofront in [#70](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/70)
* **Sensor Handling Refactor**: Refactor ecoNET sensor handling and mixer logic improvements by @jontofront in [#99](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/99)
* **Refactor**: Performed changes to refactor by @KirilKurkianec in [#100](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/100)
* **Refactor**: Refactor by @jontofront in [#102](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/102)
* **Refactor**: Refactor by @jontofront in [#104](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/104)
* **Refactor**: Refactor by @jontofront in [#107](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/107)

### Bug Fixes

* **Coordinator Keys Sync**: Fixing issue where coordinator keys not in sync with entity keys in [#41](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/41)
* **Translations Fix**: Fix translations by @denpamusic in [#44](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/44)
* **Binary Sensor Issue**: Fix binary sensor issue by @denpamusic in [#48](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/48)
* **Mixer Sensor Fix**: Fix adding mixer sensor by @m-przybylski in [#52](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/52)
* **Binary Sensor Constants**: Fix binary sensor change constants by @jontofront in [#74](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/74)
* **EconetClient Initialization**: Initialization of EconetClient Class with None Values by @jontofront in [#86](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/86)
* **Bug Data Fix**: 80 bug data for key data does not exist by @jontofront in [#96](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/96)
* **Class Function Hierarchy**: Fixing class function hierarchy by @KirilKurkianec in [#106](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/106)

### New Contributors

* @m-przybylski made their first contribution in [#52](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/52)
* @KirilKurkianec made their first contribution in [#100](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/pull/100)

**Full Changelog**: [https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/compare/v0.3.3...v1.0.5](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/compare/v0.3.3...v1.0.5)

## [v1.0.11]

Additions and Updates to Sensors:
Added boilerPowerKW as a new sensor type in custom_components/econet300/const.py and updated its unit, device class, and icon. [1] [2] [3] [4] [5]
Added feederWorks as a new binary sensor in custom_components/econet300/const.py and updated its icon. [1] [2] [3]
Updates to Existing Sensors:
Renamed the lighter sensor to lighterWorks in custom_components/econet300/const.py and updated its icon. [1] [2]
Updated the names of the lighter, boilerPower, and feeder sensors in custom_components/econet300/strings.json and custom_components/econet300/translations/en.json. [1] [2] [3] [4] [5] [6]

## # Changelog

## [1.1.0] - 2025-01-07
### Added
- Introduced `skip_params_edits` function in `custom_components/econet300/common.py` to determine if parameter edits should be skipped based on `controllerID` (controller_id == "ecoMAX360i").
- Added `async_gather_entities` function in `custom_components/econet300/sensor.py` to collect sensor entities.
- Added annotations and type hints across various functions.
- Support for ecoMAX360i controller.

### Changed
- Updated `EconetDataCoordinator` class in `custom_components/econet300/common.py` to use type hints and new `skip_params_edits` function.
- Modified entity setup in `custom_components/econet300/number.py` to skip for `controllerID: ecoMAX360i`.
- Refactored sensor entity gathering logic in `async_setup_entry`.
- Improved error handling in `Econet300Api` by adding specific exception logging.
- Changed `homeassistant` version to `2024.12.2` and `ruff` version to `0.8.4` in `requirements.txt`.
- Removed `colorlog` dependency from `requirements.txt`.

### Fixed
- Addressed type hinting issues in `custom_components/econet300/common.py` and `custom_components/econet300/number.py`.
- Improved data attribute checks in `EconetEntity` for better error handling.

For more details, you can view the commits.