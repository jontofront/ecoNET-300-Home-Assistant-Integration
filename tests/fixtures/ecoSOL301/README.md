# ecoSOL301 Test Fixtures

Sanitized snapshots for **ecoSOL 301** (GitHub issue #219).

## Source

Generated from Home Assistant diagnostics (`config_entry-econet300-*.json`, integration **v1.2.5-beta.1+**) via `scripts/create_fixture_from_diagnostics.py` and a small follow-up for `regParamsData` (see below).

## LAN API behaviour on this hardware

- **`reg_params`** — Flat live registers (`T1`, `P1`, `Uzysk_ca_kowity`, …); see `regParams.json`.
- **`reg_params_data`** — Often **`null`** from `GET …/regParamsData` on this module. Parameter metadata for many keys is exposed under **`extended_endpoints.edit_params.funcdata`** instead. `regParamsData.json` stores `{"curr": <funcdata>}` so tests and docs match that shape.
- **`extended_endpoints`** — Includes real **`edit_params`** (ecoSOL layout: `sections`, `data`, `funcdata`, …) and empty **`rm_*`** objects when the Remote Menu API is not used (`rmParamsNames.json`, … as `{}`).

## Files

| File | Role |
| --- | --- |
| `regParams.json` | Live `reg_params` snapshot; `Moc_chwilowa` added as `0` when missing from the snapshot. |
| `sysParams.json` | `sys_params` from diagnostics (redacted fields as in HA export). |
| `regParamsData.json` | Synthetic `curr` wrapper around `edit_params.funcdata` when `reg_params_data` is null. |
| `editParams.json` | Full `extended_endpoints.edit_params` payload. |
| `rm*.json` | RM endpoint snapshots (empty `{}` when unsupported). |
| `rmCurrentDataParamsEdits.json` | `param_edit_data` (`{}` when edits unsupported). |

Re-download diagnostics after firmware or integration changes, then re-run the fixture script (use `--keep-file` to retain the JSON in `scripts/ad_diagnostic_file/`).
