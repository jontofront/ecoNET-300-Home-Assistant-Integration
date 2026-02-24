# SControl_EM892 Test Fixtures

## Overview

This directory contains test fixtures for the **SControl_EM892** ecoNET device.

## Files

### Data Files

- `regParams.json` - Extracted from diagnostic file
- `regParamsData.json` - Extracted from diagnostic file
- `rmCurrentDataParamsEdits.json` - Extracted from diagnostic file
- `rmData.json` - Extracted from diagnostic file
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

fixture_path = Path(__file__).parent / "fixtures" / "SControl_EM892"
sys_params = json.loads((fixture_path / "sysParams.json").read_text())
```
