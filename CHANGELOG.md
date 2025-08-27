# Changelog

## [v1.1.9] - 2025-01-27

### Changed

- **Logging Level Refactoring**: Major refactoring of logging levels throughout the integration
- **VS Code Settings Optimization**: Streamlined development environment configuration

### Fixed

- **Git Pre-commit Hook Issues**: Fixed file formatting issues that caused pre-commit hook failures
  - **Problem**: Pre-commit hooks were failing due to trailing whitespace and end-of-file formatting
  - **Solution**: Cleaned up file formatting to meet git hook requirements
  - **Impact**: All pre-commit hooks now pass successfully, ensuring code quality
  - **Files Modified**: `.vscode/settings.json`

### Technical Changes

- **Logging Refactoring**: Systematic review and adjustment of log levels across the codebase
- **VS Code Configuration**: Streamlined Ruff settings to use native VS Code support
- **Git Hooks**: Ensured all pre-commit hooks pass for consistent code quality
- **Development Environment**: Cleaner, more maintainable VS Code configuration
- **Code Quality**: Improved logging practices for better debugging and monitoring

## [v1.1.8] - 2025-08-11

### Fixed

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

### Added

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

### Changed

- **Error Handling Strategy**: Changed from reactive error handling to proactive endpoint detection
  - **Before**: Made API calls first, then handled errors when they occurred
  - **After**: Check controller compatibility first, then make only supported API calls
  - **Benefits**: Faster startup, better performance, no crashes, cleaner logs

### Technical Changes

- **skip_params_edits Function**: Enhanced to detect all unsupported controller types
- **Safety Checks**: Added multiple validation layers in entity update methods
- **Documentation**: Updated API documentation with controller-specific endpoint information
- **Code Quality**: Improved error handling and logging throughout the system

## [v1.1.7] - 2025-08-08

### Fixed

- **Entity Category Mapping**: Fixed binary sensor entity categories for better UI organization
  - **Problem**: Diagnostic entities like 'lan', 'wifi', 'mainSrv' were showing in Sensors section instead of Diagnostics
  - **Solution**: Added explicit entity_category property to EconetBinarySensor class and proper type annotations
  - **Impact**: Diagnostic entities now appear in the correct Diagnostics section in Home Assistant UI
  - **Files Modified**: `custom_components/econet300/binary_sensor.py`
  - **Technical Details**: Added EntityCategory import and explicit entity_category property with proper type annotations

### Technical Changes

- **Type Annotations**: Fixed mypy type checking errors for \_attr_is_on property
- **Entity Category Property**: Added explicit entity_category property to ensure proper category inheritance
- **Code Quality**: All pre-commit checks pass including mypy static type checking

## [v1.1.6] - 2025-08-08

### Added

- **ecoSOL500 Solar Collector Support**: Added comprehensive support for ecoSOL500 solar collector controller
  - **New Device Type**: Full integration with ecoSOL500 solar collector capabilities
  - **Temperature Sensors**: Added support for T1-T6 temperature sensors (collector, tank, return temperatures)
  - **Hot Water Temperature**: Added TzCWU sensor for hot water temperature monitoring
  - **Pump Status Sensors**: Added P1 and P2 pump status sensors
  - **Output Status**: Added H output status sensor
  - **Heat Output**: Added Uzysk_ca_kowity (total heat output) sensor with percentage unit
  - **Test Fixtures**: Added complete test fixtures for ecoSOL500 validation
  - **Translation Support**: Added proper translations for all ecoSOL500 sensors

### Fixed

- **Entity Category Mapping**: Fixed binary sensor entity categories for better UI organization
  - **Problem**: Diagnostic entities like 'lan', 'wifi', 'mainSrv' were showing in Sensors section instead of Diagnostics
  - **Solution**: Added proper entity_category mapping in binary sensor creation
  - **Impact**: Diagnostic entities now appear in the correct Diagnostics section in Home Assistant UI
  - **Files Modified**: `custom_components/econet300/binary_sensor.py`

### Changed

- **Code Quality Tools**: Enhanced development workflow with professional code quality tools
  - **Pre-commit Hooks**: Added comprehensive pre-commit configuration with debug statement prevention and docstring checks
  - **Type Checking**: Added mypy static type checking with proper dependencies
  - **Security Analysis**: Added CodeQL security analysis workflow for automated vulnerability detection
  - **Files Modified**: `.pre-commit-config.yaml`, `.github/workflows/codeql.yml`

### Technical Changes

- **Constants Organization**: Added ecoSOL500-specific sensor mappings, device classes, units, and icons
- **Entity Creation Logic**: Improved entity category handling for better UI organization
- **Development Standards**: Enhanced code quality with automated linting, formatting, and security checks
- **Documentation**: Updated development workflow with professional standards

## [v1.1.5] - 2025-08-06

### Added

- **ecoMAX850R2-X Support**: Added comprehensive support for the new ecoMAX850R2-X boiler controller
  - **New Device Type**: Full integration with ecoMAX850R2-X controller capabilities
  - **ecoSTER Thermostat Support**: Added support for up to 8 ecoSTER room thermostats
  - **Enhanced Sensor Support**: Added new sensors specific to ecoMAX850R2-X (fuelConsum, fuelStream, tempBack, transmission)
  - **Documentation**: Created comprehensive documentation for ecoMAX850R2-X features and capabilities
  - **Test Fixtures**: Added complete test fixtures for ecoMAX850R2-X validation

### Fixed

- **statusCO Sensor Translation**: Fixed missing translation for statusCO sensor causing "PLUM ecoNET300" display issue
  - **Problem**: statusCO sensor was missing translation key in sensor section
  - **Solution**: Added status_co translation to all translation files (strings.json, en.json, pl.json)
  - **Impact**: statusCO sensor now displays as "Central heating status" instead of raw translation key
  - **Files Modified**: Translation files in sensor section

### Changed

- **ecoSTER as Separate Devices**: Refactored ecoSTER thermostats to be separate Home Assistant devices
  - **Device Structure**: Each ecoSTER thermostat (1-8) now appears as a separate device under the main controller
  - **Entity Organization**: ecoSTER sensors and binary sensors are properly grouped by thermostat
  - **Module Detection**: ecoSTER entities only created when moduleEcoSTERSoftVer is present in sysParams
  - **Files Modified**: `custom_components/econet300/entity.py`, `sensor.py`, `binary_sensor.py`

### Technical Changes

- **Constants Organization**: Reorganized sensor and binary sensor mappings for better device-specific support
- **Translation Validation**: Added comprehensive validation logic and commit workflow documentation
- **Entity Creation Logic**: Improved module detection and entity filtering for ecoSTER devices
- **Documentation**: Updated cursor rules with validation guidelines and commit workflow

## [v1.1.4] - 2025-01-XX

### Changed

- **Version Update**: Updated version to 1.1.4

## [v1.1.3] - 2025-07-15

### Added

- **Mixer Temperature Setpoints**: Added support for mixer temperature setpoints 1-6
  - **New Number Entities**: mixerSetTemp1 through mixerSetTemp6 (parameters 1287-1292)
  - **Translation Support**: Added proper translations for all mixer setpoints in English and Polish
  - **Smart Entity Creation**: Only creates entities for mixers that exist on your specific boiler model
  - **Files Modified**: `custom_components/econet300/const.py`, translation files

### Changed

- **Exception Handling**: Improved debugging by using general exception handling during development
  - **Better Error Visibility**: Catches all possible errors to help identify issues during testing
  - **Development Friendly**: Easier to debug unexpected API responses or network issues
  - **Files Modified**: `custom_components/econet300/api.py`

### Technical Changes

- **NUMBER_MAP**: Added mixer temperature setpoints 1287-1292
- **Translation Files**: Updated strings.json, en.json, and pl.json with mixer setpoint translations
- **Entity Creation Logic**: Existing logic automatically handles null values (mixers that don't exist)
- **GitHub Actions**: Added CI workflow with translation checks, tests, and linting

## [v1.1.2] - 2025-01-XX

### Fixed

- **Temperature Control API Endpoint**: Fixed incorrect API endpoint for temperature setpoints
  - **Problem**: Integration was using `/econet/rmNewParam?newParamIndex={param}` which doesn't work
  - **Solution**: Changed to `/econet/rmCurrNewParam?newParamKey={param}` which is the correct endpoint
  - **Impact**: Boiler temperature setpoints, hot water setpoints, and mixer temperature controls now work correctly
  - **Files Modified**: `custom_components/econet300/api.py`
  - **Technical Details**: Updated `set_param()` method to use correct endpoint format for NUMBER_MAP parameters

### Technical Changes

- **API Endpoint**: Changed from `rmNewParam` to `rmCurrNewParam` for temperature setpoints
- **Parameter Format**: Changed from `newParamIndex` to `newParamKey` for temperature parameters
- **Affected Parameters**: All temperature setpoints (1280=tempCOSet, 1281=tempCWUSet, 1287-1292=mixerSetTemp1-6)
- **Backward Compatibility**: No breaking changes, only fixes non-working functionality

## [v1.1.2] - 2025-01-XX
