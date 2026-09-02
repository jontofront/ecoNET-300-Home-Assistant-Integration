# ecoMAX850P-R Test Fixtures

## Overview

This directory contains test fixtures for the **ecoMAX850P-R** ecoNET device.
This is a different controller from **ecoMAX850R2-X** (`tests/fixtures/ecoMAX850R2-X/`).

## Device snapshot (issue [#247](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/247))

| Field | Value |
| ----- | ----- |
| `controllerID` | `ecoMAX850P-R` |
| `protocolType` | `em` |
| Module A | `2.10.14.V1` |
| Module B | `1.31.14` |
| Panel | `2.30.11` |
| ecoNET `softVer` | `3.2.3886` |
| Integration | v1.3.2 |
| `remoteMenu` | `false` (rm\* endpoints empty / unavailable) |

### Boiler state in this dump

| Parameter | Raw value | Notes |
| --------- | --------- | ----- |
| `mode` | `1` | Panel: Pause / Stop. Mapped to `stop` via `SENSOR_STATUS_CO_MAPPING` |
| `statusCO` | `40` | Not in `SENSOR_STATUS_CO_MAPPING` (0–26) |
| `transmission` | `5` | Halt / paused in both current and official tables |
| `fan` / `fanWorks` / `fanPower` | off / `0` | |
| `feeder` / `lighter` | off | |
| `boilerPower` | `0` | |
| `tempCO` | ~22 °C | Cold |
| `tempFlueGas` | ~23 °C | Ambient |
| mode tile `extra_` | `CAN_TURN_OFF_BOILER` | Boiler control is enabled (not mode `0`) |

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

`mergedData.json` and `rmStructure.json` were not present in the diagnostic dump
(`remoteMenu` is disabled on this module).

## Source

These fixtures were generated from the Home Assistant diagnostic file attached to
issue [#247](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/247)
using `scripts/create_fixture_from_diagnostics.py`.

## Usage

```python
# Example: Load fixture data in tests
import json
from pathlib import Path

fixture_path = Path(__file__).parent / "fixtures" / "ecoMAX850P-R"
sys_params = json.loads((fixture_path / "sysParams.json").read_text())
```
