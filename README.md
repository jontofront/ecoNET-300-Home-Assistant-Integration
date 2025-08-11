# ecoNET-300 Home Assistant Integration

[![Code Formatter](https://img.shields.io/badge/Code%20Formatter-Ruff-000000?style=for-the-badge&logo=python)](https://github.com/astral-sh/ruff)
[![Latest Release](https://img.shields.io/github/v/release/jontofront/ecoNET-300-Home-Assistant-Integration?style=for-the-badge)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/releases)
[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5?style=for-the-badge&logo=homeassistant)](https://github.com/hacs/integration)
[![HACS Action](https://img.shields.io/badge/HACS%20Action-passing-brightgreen?style=for-the-badge&logo=github)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hacs.yml)
[![Stability](https://img.shields.io/badge/Stability-Stable-2ecc71?style=for-the-badge)](https://guidelines.denpa.pro/stability#stable)
[![Hassfest](https://img.shields.io/badge/Hassfest-Validated-brightgreen?style=for-the-badge&logo=homeassistant)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hassfest.yaml)

**Note:** This repository is a fork of the original [pblxptr/ecoNET-300-Home-Assistant-Integration](https://github.com/pblxptr/ecoNET-300-Home-Assistant-Integration). Most of the work was done by [@pblxpt](https://github.com/pblxpt), and we are very grateful for their efforts.
**Additionally, I maintained and supported this code up to version v0.3.3.**

<div align="center">

| Home Assistant  | ecoNET300     | device        |
| --------------- | ------------- | ------------- |
| <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/ha.png" width="100" height="100" />                |   <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/econet.webp" width="95" height="95" />            | <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/econet300_device.jpg" width="100" height="100" /> |

</div>

## 🎉 Major Achievement: Complete API Discovery

We have successfully discovered and documented **48 API endpoints** on the ecoNET-300 device, achieving a **100% success rate**! This represents a **12x increase** from the original 4 known endpoints.

### 📊 Discovery Statistics
- **Total Endpoints:** 48 (all successful)
- **Total Data Retrieved:** 89.5 KB
- **Average Response Time:** 0.130s
- **Device Tested:** ecoMAX810P-L TOUCH
- **Key Discovery:** Real-time sensor data access via `rmCurrentDataParams`

---

## Overview

The **ecoNET300 Home Assistant Integration** allows local control and monitoring of ecoNET300 devices directly from Home Assistant. It communicates over your local network via the ecoNET-300's native REST API, avoiding any external cloud services.

### ✨ Features
- **Local Operation**: No dependency on econet24.com cloud services
- **Easy Configuration**: Integrate directly via Home Assistant UI
- **Boiler Control**: Turn your boiler ON/OFF directly from Home Assistant
- **Real-time Monitoring**: Monitor temperatures, fuel levels, and system status
- **Comprehensive API Access**: Access to 48 different API endpoints
- **Multiple Entity Types**: Sensors, Binary Sensors, Switches, and Number entities

### 🏠 Supported Devices
- **ecoMAX810P-L TOUCH** controller from [Plum Sp. z o.o.](https://www.plum.pl/)
- **ecoMAX850R2-X** pellet boiler controller
- **ecoMAX360** boiler controller
- **ecoMAX860P2-N** boiler controller
- **ecoMAX860P3-V** boiler controller
- **ecoSOL** solar thermal controller
- **SControl MK1** control module
- Other ecoNET300 compatible devices

---

## 📋 Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Entities](#entities)
4. [API Discovery](#api-discovery)
5. [Development Roadmap](#development-roadmap)
6. [Contributing](#contributing)
7. [Acknowledgments](#acknowledgments)

---

## 🚀 Installation

### HACS (Recommended)
1. Install and configure [HACS](https://hacs.xyz/).
2. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) using:
```
https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration
```
3. In HACS, search for **"ecoNET300"**, install the integration.
4. Restart Home Assistant.

### Manual Installation
1. Download or clone this repository.
2. Copy `custom_components/econet300` into your `<config_directory>/custom_components/`.

```
<config directory>/
|-- custom_components/
|   |-- econet300/
|       |-- [...]
```
3. Restart Home Assistant.

---

## ⚙️ Configuration

Integrate ecoNET300 via the user interface:

[![Add integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=econet300)

<details>
  <summary><b>Manual Configuration Steps</b></summary>

Apart from using 'My button' (in case it doesn't work) you can also perform the following steps manually:

1. Go to **Settings > Devices & Services** in Home Assistant.
2. Click **Add Integration**.
3. Search and select **"ecoNET300"**.
4. In the bottom right, click on the Add Integration button.
5. From the list, search and select **"ecoNET300"**.

![Search dialog](https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/search.png)

6. Enter your local device IP/domain and local credentials (not econet24.com credentials). **"Submit"**.

__Host__: Local IP/domain of your device.

__Username__: Local username (NOT the username that you use to login to econet24.com!).

__Password__: Local password (NOT the password that you use to login to econet24.com!).

![Configuration dialog](https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/configure.png)

7. Your device should now be available in your Home Assistant installation.

![Success](https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/success.png)

</details>

---

## 🏠 Entities

### Switches

The integration provides a boiler control switch that allows you to turn the boiler ON and OFF directly from Home Assistant.

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key           | Description                                  | Control | State Detection |
|----------------------|----------------------------------------------|---------|-----------------|
| `boiler_control`     | Boiler ON/OFF control switch                 | `BOILER_CONTROL` parameter | `mode` parameter |
</details>

**Features:**
- **Direct Control**: Turn boiler ON/OFF with a simple switch
- **State Synchronization**: Switch state reflects actual boiler operation mode
- **API Integration**: Uses the ecoNET-300's native `BOILER_CONTROL` parameter
- **Real-time Updates**: Switch state updates based on current boiler mode

### Sensors

These sensors are retrieved from the `../econet/regParams` and `../econet/sysParams` endpoints.

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key           | Description                                               | Endpoint              |
|----------------------|-----------------------------------------------------------|-----------------------|
| `tempFeeder`         | Temperature of the feeder mechanism                       | `../econet/regParams` |
| `fuelLevel`          | Current fuel level in the system                          | `../econet/regParams` |
| `tempCO`             | Current fireplace temperature                             | `../econet/regParams` |
| `tempCOSet`          | Desired fireplace set temperature                         | `../econet/regParams` |
| `statusCWU`          | Status of the hot water (CWU) system                      | `../econet/regParams` |
| `tempCWU`            | Current hot water (CWU) temperature                       | `../econet/regParams` |
| `tempCWUSet`         | Desired hot water (CWU) temperature                       | `../econet/regParams` |
| `tempFlueGas`        | Exhaust temperature reading                               | `../econet/regParams` |
| `mode`               | Current operational mode of the device                    | `../econet/regParams` |
| `fanPower`           | Current fan power usage                                   | `../econet/regParams` |
| `thermostat`         | Thermostat status or set temperature                      | `../econet/regParams` |
| `tempExternalSensor` | Outside (external) temperature                            | `../econet/regParams` |
| `tempLowerBuffer`    | Temperature of the lower thermal buffer                   | `../econet/regParams` |
| `tempUpperBuffer`    | Temperature of the upper thermal buffer                   | `../econet/regParams` |
| `boilerPower`        | Current power output of the boiler                        | `../econet/regParams` |
| `quality`            | Fuel quality or system quality indicator (if applicable) | `../econet/sysParams` |
| `signal`             | Signal strength or communication status                  | `../econet/sysParams` |
| `softVer`            | Software version of the controller                       | `../econet/sysParams` |
| `controllerID`       | Unique identifier for the controller                     | `../econet/sysParams` |
</details>

### Binary Sensors

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key           | Description                                               | Endpoint              |
|----------------------|-----------------------------------------------------------|-----------------------|
| `pumpCO`             | Central heating pump status                               | `../econet/regParams` |
| `pumpCWU`            | Hot water pump status                                     | `../econet/regParams` |
| `pumpSolar`          | Solar pump status                                         | `../econet/regParams` |
| `pumpCirculation`    | Circulation pump status                                   | `../econet/regParams` |
| `pumpFireplace`      | Fireplace pump status                                     | `../econet/regParams` |
| `fan`                | Fan status                                                | `../econet/regParams` |
| `blowFan1`           | Blow fan 1 status                                         | `../econet/regParams` |
| `blowFan2`           | Blow fan 2 status                                         | `../econet/regParams` |
| `feeder`             | Feeder mechanism status                                   | `../econet/regParams` |
| `lighter`            | Lighter status                                            | `../econet/regParams` |
| `outerBoiler`        | Outer boiler status                                       | `../econet/regParams` |
| `contactGZC`         | GZC contact status                                        | `../econet/regParams` |
| `alarmOutput`        | Alarm output status                                       | `../econet/regParams` |
</details>

### Number Entities

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key           | Description                                               | Endpoint              |
|----------------------|-----------------------------------------------------------|-----------------------|
| `tempCOSet`          | Central heating temperature setpoint                      | `../econet/regParams` |
| `tempCWUSet`         | Hot water temperature setpoint                            | `../econet/regParams` |
| `mixerSetTemp1`      | Mixer 1 temperature setpoint                              | `../econet/regParams` |
| `mixerSetTemp2`      | Mixer 2 temperature setpoint                              | `../econet/regParams` |
| `mixerSetTemp3`      | Mixer 3 temperature setpoint                              | `../econet/regParams` |
| `mixerSetTemp4`      | Mixer 4 temperature setpoint                              | `../econet/regParams` |
| `mixerSetTemp5`      | Mixer 5 temperature setpoint                              | `../econet/regParams` |
| `mixerSetTemp6`      | Mixer 6 temperature setpoint                              | `../econet/regParams` |
</details>

---

## 🔍 API Discovery

### 🎯 Key API Endpoints Discovered

#### ⭐ **HIGH PRIORITY** (Implement First)
1. **rmCurrentDataParams** - Real-time sensor data (4.8 KB)
2. **rmParamsData** - Parameter values (12.7 KB)
3. **rmParamsNames** - Parameter names (5.4 KB)
4. **rmParamsDescs** - Parameter descriptions (29.1 KB)
5. **rmAlarms** - System alarms
6. **rmStatus** - System status

#### 🔧 **MEDIUM PRIORITY** (Implement Second)
1. **rmStructure** - System structure (13.1 KB)
2. **rmParamsEnums** - Parameter enumerations (2.5 KB)
3. **rmCatsNames** - Category names (1.1 KB)
4. **rmDiagnostics** - Diagnostic information
5. **rmSchedule** - Automation capabilities
6. **rmStatistics** - Performance monitoring

#### ⚙️ **LOW PRIORITY** (Advanced Features)
- 16 parameter management endpoints
- System administration endpoints
- Testing and calibration endpoints
- Factory and backup endpoints

### 📊 Integration Potential
- **11 potential sensors** identified
- **45 potential controls** identified
- **Real-time monitoring** capabilities
- **Complete parameter ecosystem** access
- **Comprehensive alarm system** integration

---

## 🚀 Development Roadmap

### ✅ **Completed**
- [x] API endpoint discovery (48 endpoints)
- [x] Response structure documentation
- [x] Performance analysis
- [x] Data sanitization
- [x] Project organization
- [x] Complete documentation

### 🚧 **In Progress**
- [ ] Home Assistant sensor implementation
- [ ] Parameter monitoring integration
- [ ] Alarm system integration
- [ ] Status monitoring implementation

### 📅 **Planned**
- [ ] Parameter control implementation
- [ ] Advanced automation features
- [ ] User interface improvements
- [ ] Performance optimization
- [ ] Comprehensive testing

### 🎯 **Next Steps for Integration**

#### 1. **Implement Core Sensors** (Week 1)
- Use `rmCurrentDataParams` for real-time temperature, status, and power data
- Create sensors for boiler temperature, pump status, fan status, fuel level
- Implement alarm sensors using `rmAlarms`

#### 2. **Add Parameter Monitoring** (Week 2)
- Use `rmParamsData` + `rmParamsNames` for parameter monitoring
- Create user-friendly parameter names using the name mappings
- Add parameter descriptions using `rmParamsDescs`

#### 3. **Implement Status Monitoring** (Week 3)
- Use `rmStatus` for system health monitoring
- Add diagnostic information using `rmDiagnostics`
- Implement performance monitoring using `rmStatistics`

#### 4. **Add Parameter Controls** (Week 4)
- Use `rmCurrentDataParamsEdits` for editable parameters
- Implement parameter validation using `rmParamsEnums`
- Add parameter limits using the parameter metadata endpoints

#### 5. **Create Advanced Features** (Week 5+)
- Implement scheduling using `rmSchedule`
- Add system administration features
- Create comprehensive automation capabilities

---

## 📁 Project Structure

```
ecoNET-300-Home-Assistant-Integration/
├── custom_components/econet300/     # Home Assistant integration
├── docs/                            # Complete API documentation
├── scripts/                         # Essential development scripts
├── tests/                           # Integration tests
└── [standard project files]
```

### 🔧 **Essential Scripts** (in `scripts/`)
- **test_api_endpoints.py** - Test all API endpoints
- **check_translations.py** - Validate translation files
- **download_cloud_translations.py** - Download cloud translations
- **extract_cloud_translations.py** - Extract translation data

### 📚 **Essential Documentation** (in `docs/`)
- **API_V1_DOCUMENTATION.md** - Complete API documentation (consolidated)
- **BOILER_CONTROL_README.md** - Boiler control documentation
- **CLOUD_TRANSLATIONS.md** - Cloud translations documentation

---

## 📋 Versions

* v0.3.3 - version is stable. Most of the work was done by @pblxpt, for which we're very thankful as the community.
* v1.0.0 - A development version that retrieves more data from the API. It may be unstable, and upgrades from previous versions are not supported.
* v1.1.1 - Added boiler ON/OFF control switch functionality. New features include direct boiler control via Home Assistant switches.
* v1.1.3 - **Critical Fix**: Fixed temperature control API endpoint. Temperature setpoints now work correctly.
* v1.1.3 - **Mixer Temperature Setpoints**: Added support for mixer temperature setpoints 1-6 with smart entity creation.

### New Features in v1.1.1
- **Boiler Control Switch**: Turn your boiler ON/OFF directly from Home Assistant
- **API Integration**: Uses the ecoNET-300's native `BOILER_CONTROL` parameter
- **State Synchronization**: Switch state reflects actual boiler operation mode
- **Real-time Updates**: Automatic state updates based on boiler mode changes

### Critical Fix in v1.1.3
- **Temperature Control**: Fixed API endpoint for temperature setpoints
- **Boiler Temperature**: Users can now set boiler temperature setpoints
- **Hot Water Temperature**: Hot water temperature can be adjusted
- **Mixer Temperature**: All mixer temperature setpoints work correctly
- **Number Entities**: Home Assistant number entities function properly
- **Mixer Temperature Setpoints**: Added support for mixer temperature setpoints 1-6
- **Smart Entity Creation**: Only creates entities for mixers that exist on your boiler
- **Translation Support**: Proper English and Polish translations for all mixer setpoints
- **Improved Debugging**: Better error handling for development and troubleshooting

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Testing
Use the provided scripts in the `scripts/` directory to test API endpoints and validate translations.

---

## 🙏 Acknowledgments

- **[@pblxpt](https://github.com/pblxpt)** - Original developer and maintainer up to v0.3.3
- **[@jontofront](https://github.com/jontofront)** - Current maintainer and developer
- **ecoNET300 Community** - For testing, feedback, and support
- **Plum Sp. z o.o.** - For creating the ecoNET300 system

---

## ⚠️ Disclaimer

This integration is not officially affiliated with or endorsed by Plum Sp. z o.o. Use at your own risk. The developers are not responsible for any damage to your equipment or system.

---

## 📞 Support

If you encounter any issues or have questions:
1. Check the [API Documentation](docs/API_V1_DOCUMENTATION.md)
2. Search existing [Issues](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues)
3. Create a new issue with detailed information about your problem

---

*This README was last updated on 2025-07-18 after completing the comprehensive API discovery process.*
