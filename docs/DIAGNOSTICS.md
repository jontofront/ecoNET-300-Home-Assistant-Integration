# Diagnostics

The ecoNET300 Home Assistant Integration includes comprehensive diagnostics support to help troubleshoot issues and provide detailed system information.

## Overview

Diagnostics functionality allows you to download detailed information about your integration configuration, device status, entity states, and API data. This information is essential for troubleshooting issues and providing support.

## How to Download Diagnostics

### Method 1: Integration Diagnostics (Recommended)

1. Go to **Settings > Devices & Services** in Home Assistant
2. Find your **ecoNET300** integration
3. Click on the integration name
4. Click the **Download diagnostics** button
5. A JSON file will be downloaded with comprehensive system information

### Method 2: Device Diagnostics

1. Go to **Settings > Devices & Services** in Home Assistant
2. Find your **ecoNET300** device
3. Click on the device name
4. Click the **Download diagnostics** button
5. A JSON file will be downloaded with device-specific information

## What's Included in Diagnostics

### Integration Diagnostics

- **Integration Information**

  - Integration version
  - Configuration details
  - Setup times and performance metrics

- **Device Information**

  - Device ID and name
  - Manufacturer and model
  - Hardware and software versions
  - Device identifiers (redacted for security)

- **Entity Information**

  - Complete list of all entities
  - Current values and states
  - Units of measurement
  - Entity attributes and metadata
  - Entity count and platform information

- **API Endpoint Data**

  - Raw data from `sysParams` endpoint
  - Raw data from `regParams` endpoint
  - Raw data from `regParamsData` endpoint
  - Raw data from `paramEditData` endpoint

- **System Status**
  - Connection status
  - Coordinator data
  - Last update information
  - Data availability status

### Device Diagnostics

Device diagnostics include all the information from integration diagnostics, plus:

- **Device-Specific Information**

  - Device registry details
  - Device connections and identifiers
  - Device area and disabled status

- **Entity Registry Information**
  - Entity registry entries
  - Entity platform and disabled status
  - Entity unique IDs

## Sensitive Data Protection

The diagnostics system automatically redacts sensitive information to protect your privacy and security:

### Automatically Redacted Information

- **Device Identifiers**

  - Device UIDs (e.g., `7VCPMB4ZJ8DHH208002Z0`)
  - Device identifiers in registry
  - Unique device identifiers

- **Authentication Information**

  - Passwords and API keys
  - Service passwords
  - Authentication tokens

- **Network Information**

  - WiFi SSIDs
  - Network interface IP addresses (`wlan0`, `eth0`)
  - Internal network details

- **Other Sensitive Data**
  - Any other configuration data that could compromise security

### Example of Redacted Data

```json
{
  "device_info": {
    "identifiers": "**REDACTED**",
    "device_uid": "**REDACTED**"
  },
  "api_endpoint_data": {
    "sys_params": {
      "uid": "**REDACTED**",
      "key": "**REDACTED**",
      "password": "**REDACTED**",
      "ssid": "**REDACTED**",
      "wlan0": "**REDACTED**",
      "eth0": "**REDACTED**"
    }
  }
}
```

## Using Diagnostics for Troubleshooting

### Common Use Cases

1. **Integration Issues**

   - Check integration version and configuration
   - Verify device connection status
   - Review entity creation and status

2. **Entity Problems**

   - Verify entity states and values
   - Check entity attributes and metadata
   - Identify missing or incorrect entities

3. **API Communication Issues**

   - Review raw API endpoint data
   - Check for API response errors
   - Verify data availability and freshness

4. **Device-Specific Issues**
   - Check device information and versions
   - Verify hardware compatibility
   - Review device registry status

### Sharing Diagnostics

When sharing diagnostics for support:

1. **Always use redacted diagnostics** - Never share raw API data
2. **Include relevant context** - Describe the issue you're experiencing
3. **Check file size** - Large diagnostics files may need to be shared via file hosting services
4. **Remove personal information** - Double-check that no personal data is included

## File Structure

The diagnostics file is a JSON document with the following structure:

```json
{
  "home_assistant": {
    "version": "2025.8.3",
    "installation_type": "Home Assistant OS"
  },
  "custom_components": {
    "econet300": {
      "version": "1.1.13"
    }
  },
  "integration_manifest": {
    "domain": "econet300",
    "version": "1.1.13",
    "diagnostics": true
  },
  "data": {
    "integration_version": "1.1.13",
    "device_info": { ... },
    "entity_info": { ... },
    "coordinator_data": { ... },
    "api_endpoint_data": { ... }
  },
  "issues": []
}
```

## Troubleshooting Diagnostics

### Common Issues

1. **"Site wasn't available" Error**

   - This usually indicates a temporary network or API issue
   - Try downloading diagnostics again after a few minutes
   - Check your device's network connection

2. **Empty or Incomplete Diagnostics**

   - Ensure the integration is properly configured
   - Check that the device is online and accessible
   - Verify API credentials are correct

3. **Large File Size**
   - Diagnostics files can be large due to extensive API data
   - This is normal and indicates comprehensive data collection
   - Consider using file compression when sharing

### Getting Help

If you encounter issues with diagnostics:

1. **Check the logs** - Look for error messages in Home Assistant logs
2. **Verify configuration** - Ensure your integration is properly set up
3. **Test connectivity** - Verify your device is accessible on the network
4. **Contact support** - Share diagnostics (redacted) with the development team

## Technical Details

### Implementation

- **File**: `custom_components/econet300/diagnostics.py`
- **Functions**: `async_get_config_entry_diagnostics()`, `async_get_device_diagnostics()`
- **Redaction**: Custom `_redact_data()` function with comprehensive sensitive data detection
- **Error Handling**: Robust error handling with graceful degradation

### Performance

- **Download Time**: Typically 1-5 seconds depending on API response times
- **File Size**: Usually 50-500KB depending on device complexity
- **Memory Usage**: Minimal impact on Home Assistant performance
- **Network**: Uses existing API connections, no additional network overhead

### Security

- **Automatic Redaction**: All sensitive data is automatically identified and redacted
- **No Storage**: Diagnostics are generated on-demand and not stored
- **Local Processing**: All redaction happens locally in Home Assistant
- **Privacy First**: Designed to protect user privacy while providing useful debugging information

---

For more information about the ecoNET300 integration, see the [main README](../README.md).
