# ecoNET-300 Scripts

This directory contains utility scripts for working with the ecoNET-300 integration.

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

## 🔧 Other Scripts

### `check_translations.py`
Validates translation files for consistency.

### `download_cloud_translations.py`
Downloads cloud translations from ecoNET servers.

### `extract_cloud_translations.py`
Extracts and processes cloud translation data.

### `test_api_endpoints.py`
Comprehensive API endpoint testing for safe endpoints only.
