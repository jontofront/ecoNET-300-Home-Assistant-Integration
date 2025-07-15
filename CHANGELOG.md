# Changelog

## [v1.1.3] - 2025-07-15
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