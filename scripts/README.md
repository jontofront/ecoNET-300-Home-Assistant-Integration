# Essential Scripts

This directory contains essential scripts for the ecoNET-300 Home Assistant integration.

## 🔧 Available Scripts

### API Testing
- **test_api_endpoints.py** - Test all API endpoints and document responses

### Translation Management
- **check_translations.py** - Validate translation files
- **download_cloud_translations.py** - Download cloud translation data
- **extract_cloud_translations.py** - Extract translation data from cloud files

## 🚀 Usage

Most scripts can be run directly with Python:

```bash
# Test API endpoints
python scripts/test_api_endpoints.py --host YOUR_DEVICE_IP --username admin --password YOUR_PASSWORD

# Check translations
python scripts/check_translations.py

# Download cloud translations
python scripts/download_cloud_translations.py

# Extract cloud translations
python scripts/extract_cloud_translations.py
```

## 📋 Script Details

### test_api_endpoints.py
- **Purpose**: Test all discovered API endpoints and document their responses
- **Use case**: Verify API functionality, debug connection issues
- **Output**: Detailed endpoint documentation and test results

### check_translations.py
- **Purpose**: Validate translation files for consistency
- **Use case**: Ensure all translation keys are present and properly formatted
- **Output**: Translation validation report

### download_cloud_translations.py
- **Purpose**: Download translation data from ecoNET cloud services
- **Use case**: Get latest translation updates from official sources
- **Output**: Raw translation data files

### extract_cloud_translations.py
- **Purpose**: Extract and process translation data from cloud files
- **Use case**: Convert cloud translations to Home Assistant format
- **Output**: Processed translation files ready for integration

## 🎯 Integration Development

These scripts support the ongoing development of the Home Assistant integration:

1. **API Testing** - Verify endpoint functionality and response structures
2. **Translation Management** - Ensure proper localization support
3. **Cloud Integration** - Access official translation data

All discovery and analysis tools have been moved to the development archive after completing the initial API discovery phase.
