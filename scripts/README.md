# ecoNET-300 Scripts

This directory contains essential utility scripts for working with the ecoNET-300 integration.

## 🧪 API Endpoint Testing Script

### `test_api_endpoints.py`

A comprehensive API endpoint testing script that tests all safe endpoints.

#### Usage

```bash
python test_api_endpoints.py --host 192.168.1.100 --username admin --password your_password
```

#### Command Line Options

- `--host`: Device IP address or hostname (required)
- `--username`: Username for authentication (required)
- `--password`: Password for authentication (required)
- `--output-dir`: Output directory for results (default: `api_test_results`)
- `--verbose, -v`: Enable verbose logging

#### Output

The script generates:
- **JSON Results**: Complete test results in JSON format
- **Summary Report**: Markdown summary of test results
- **Endpoint Documentation**: Detailed documentation of each endpoint

## 🔍 Translation Management Scripts

### `check_translations.py`
Validates translation files for consistency and completeness.
- Checks for missing translations
- Validates translation key formats
- Ensures consistency across language files

### `language_finder.py`
**NEW: Optimized language discovery tool** that combines fast and comprehensive discovery.
- Fast language detection (reads file beginnings)
- Comprehensive analysis (full file processing)
- Coverage analysis and reporting
- Generates detailed language reports

#### Usage
```bash
python language_finder.py
```

#### Output
- `available_languages.txt` - Simple language list
- `language_coverage_report.json` - Detailed coverage data
- `language_coverage_report.md` - Markdown report with samples

## 📥 Diagnostics → test fixtures

1. Save a Home Assistant **Download diagnostics** JSON under `scripts/ad_diagnostic_file/` (see `ad_diagnostic_file/README.md`).
2. Run `python scripts/create_fixture_from_diagnostics.py` (use `--dry-run` or `--keep-file` as needed).

That produces `tests/fixtures/<device>/` files for regression tests.

## 📁 Scripts Organization

### **Current Scripts (Essential):**
- `test_api_endpoints.py` - API testing and documentation
- `check_translations.py` - Translation validation
- `language_finder.py` - Language discovery and analysis
- `create_fixture_from_diagnostics.py` - Build fixtures from HA diagnostics
- `ad_diagnostic_file/README.md` - Where to drop `config_entry-econet300-*.json`
- `README.md` - This documentation

### **Backup (Obsolete):**
- `obsolete_backup/` - Contains scripts that have accomplished their goals
- These scripts are kept for reference but are no longer needed

## 🚀 Quick Start

1. **API Testing**: Use `test_api_endpoints.py` for device testing
2. **Translation Validation**: Use `check_translations.py` for quality checks
3. **Language Discovery**: Use `language_finder.py` to find new languages

## 📊 Script Statistics

| Script | Purpose | Status | Size |
|--------|---------|--------|------|
| `test_api_endpoints.py` | API testing | ✅ Active | 15KB |
| `check_translations.py` | Translation validation | ✅ Active | 3KB |
| `language_finder.py` | Language discovery | ✅ Active | 8KB |
| **Total Active** | | | **26KB** |

**Previous total**: 12 scripts, ~80KB
**Current total**: 3 scripts, 26KB
**Improvement**: 67% reduction in size, 75% reduction in scripts
