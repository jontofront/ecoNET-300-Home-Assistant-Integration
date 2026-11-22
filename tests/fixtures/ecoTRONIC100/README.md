# ecoTRONIC100 Test Fixtures

## Overview

This directory contains test fixtures for the **ecoTRONIC100** ecoNET device.

## Files

### Data Files

- `editParams.json` - Extracted from diagnostic file
- `regParams.json` - Extracted from diagnostic file
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
- `rmStructure.json` - Extracted from diagnostic file
- `sysParams.json` - Extracted from diagnostic file

## Source

These fixtures were automatically generated from a Home Assistant diagnostic file
using the `scripts/create_fixture_from_diagnostics.py` script.

The diagnostic file comes from
[#271](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/271)
(Silesia Term heat pump with an ecoTRONIC 200 controller, integration 1.3.6,
Home Assistant 2026.6.4):

| Field              | Value                                   |
| ------------------ | --------------------------------------- |
| `controllerID`     | `ecoTRONIC100`                          |
| `protocolType`     | `gm3_pomp`                              |
| ecoNET module      | 3.2.3881                                |
| Module A / panel   | S006.88 / S003.66_2.66                  |
| `remoteMenu`       | `false`                                 |

The module has no remote menu, so the `rm*.json` files are empty and there is no
`mergedData.json`. `editParams` has the same structure as on ecoMAX360i, but other
parameter names and ids: 405 parameters, 370 of them editable. Only 33 are in the
user menu (`buttons`), 70 more only in the service menus (`serviceMenus`). The
module UID and the IP addresses in `informationParams` are redacted.

## Usage

These fixtures are used by the integration's test suite to verify correct behavior
without requiring a live ecoNET device connection.

```python
# Example: Load fixture data in tests
import json
from pathlib import Path

fixture_path = Path(__file__).parent / "fixtures" / "ecoTRONIC100"
sys_params = json.loads((fixture_path / "sysParams.json").read_text())
```
