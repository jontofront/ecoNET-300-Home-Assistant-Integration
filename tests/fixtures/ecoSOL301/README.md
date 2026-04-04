# ecoSOL301 Test Fixtures

Sanitized snapshot for **ecoSOL 301** (GitHub issue #219).

## Source

- **`regParams.json`** — `data.coordinator_data.data.regParams` from `scripts/ad_diagnostic_file/config_entry-econet300-01KN4FMJHTT8ZEKG07VWWXM1K0.json`. The LAN API for this device exposes **only these 11 flat keys** (no `tempCO` / boiler-style registers).
- **`sysParams.json`** — same diagnostic, `coordinator_data.data.sysParams`; secrets and network fields replaced with placeholders (`uid` → `UID`, `etPasswords` → `{}`, etc.).

The diagnostic also includes **`api_endpoint_data.reg_params`**, which can differ slightly from coordinator `regParams` (e.g. temperatures) because the two snapshots are taken at different times.

## Other files

- `regParamsData.json`, `rmCurrentDataParams*.json` — error stubs (no RM API on device)
