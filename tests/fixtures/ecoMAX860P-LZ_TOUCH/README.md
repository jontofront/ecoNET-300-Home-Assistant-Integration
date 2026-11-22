# ecoMAX860P-LZ_TOUCH Test Fixtures

## Overview

This directory contains test fixtures for the **ecoMAX860P-LZ_TOUCH** ecoNET device.

## Files

### Data Files

- `editParams.json` - Extracted from diagnostic file
- `regParams.json` - Extracted from diagnostic file
- `regParamsData.json` - Extracted from diagnostic file
- `rmAlarmsNames.json` - Extracted from diagnostic file
- `rmCurrentDataParams.json` - Extracted from diagnostic file
- `rmCurrentDataParamsEdits.json` - Extracted from diagnostic file
- `rmData.json` - Extracted from diagnostic file
- `rmExistingLangs.json` - Extracted from diagnostic file
- `rmLangs.json` - Extracted from diagnostic file
- `rmLocksNames.json` - Extracted from diagnostic file
- `rmParamsData.json` - Extracted from diagnostic file
- `rmParamsDescs.json` - Extracted from diagnostic file
- `rmParamsEnums.json` - Extracted from diagnostic file
- `rmParamsNames.json` - Extracted from diagnostic file
- `rmParamsUnitsNames.json` - Extracted from diagnostic file
- `sysParams.json` - Extracted from diagnostic file

## Source

These fixtures were automatically generated from a Home Assistant diagnostic file
using the `scripts/create_fixture_from_diagnostics.py` script.

The diagnostic file comes from
[#276](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/276)
(Lazar SmartFire 31, integration 1.3.6, Home Assistant 2026.11.1):

| Field              | Value                                   |
| ------------------ | --------------------------------------- |
| `controllerID`     | `ecoMAX860P-LZ TOUCH`                   |
| `protocolType`     | `em`                                    |
| ecoNET module      | 3.2.3886                                |
| Module A / panel   | 8.41.38.L0 / 8.30.28                    |
| `remoteMenu`       | `true`                                  |

At the time of capture the module answered every RM endpoint with empty data, so
there is no `mergedData.json` and the `rm*.json` files are empty. `editParams`
has no parameters (no ecoSTER). Only `rmCurrentDataParamsEdits.json` has
editable values: boiler and DHW setpoints, mixer 1 setpoint and heater mode.

## Usage

These fixtures are used by the integration's test suite to verify correct behavior
without requiring a live ecoNET device connection.

```python
# Example: Load fixture data in tests
import json
from pathlib import Path

fixture_path = Path(__file__).parent / "fixtures" / "ecoMAX860P-LZ_TOUCH"
sys_params = json.loads((fixture_path / "sysParams.json").read_text())
```
