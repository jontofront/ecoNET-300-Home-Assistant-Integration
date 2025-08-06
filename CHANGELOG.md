# Changelog

## [v1.1.5] - 2025-01-XX
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
