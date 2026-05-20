# ecoMAX360i Test Fixtures

## Overview

This directory contains test fixtures for the **ecoMAX360i** ecoNET device.

## Files

### Data Files

- `editParams.json` - Extracted from diagnostic file
- `regParams.json` - Extracted from diagnostic file
- `rmAlarmsNames.json` - Extracted from diagnostic file
- `rmCurrentDataParams.json` - Extracted from diagnostic file
- `rmCurrentDataParamsEdits.json` - Extracted from diagnostic file
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

## Usage

These fixtures are used by the integration's test suite to verify correct behavior
without requiring a live ecoNET device connection.

```python
# Example: Load fixture data in tests
import json
from pathlib import Path

fixture_path = Path(__file__).parent / "fixtures" / "ecoMAX360i"
sys_params = json.loads((fixture_path / "sysParams.json").read_text())
```
