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

| Home Assistant                                                                                                                                 | ecoNET300                                                                                                                                         | device                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/ha.png" width="100" height="100" /> | <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/econet.webp" width="95" height="95" /> | <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/econet300_device.jpg" width="100" height="100" /> |

</div>

## Overview

The **ecoNET300 Home Assistant Integration** allows local control and monitoring of ecoNET300 devices directly from Home Assistant. It communicates over your local network via the ecoNET-300's native REST API, avoiding any external cloud services.

### ✨ Features

- **Local Operation**: No dependency on econet24.com cloud services
- **Easy Configuration**: Integrate directly via Home Assistant UI
- **Boiler Control**: Turn your boiler ON/OFF directly from Home Assistant
- **Real-time Monitoring**: Monitor temperatures, fuel levels, and system status
- **Comprehensive API Access**: Access to 48 different API endpoints
- **Multiple Entity Types**: Sensors, Binary Sensors, Switches, and Number entities
- **Diagnostics Support**: Download comprehensive diagnostics for troubleshooting

### 🌐 Language Support

The integration supports **6 languages** with comprehensive translations:

| Language | Code | Status | Coverage |
|----------|------|--------|----------|
| 🇬🇧 English | `en` | ✅ Complete | Base language |
| 🇵🇱 Polish | `pl` | ✅ Complete | Full translation |
| 🇨🇿 Czech | `cs` | ✅ Complete | 348 parameters |
| 🇫🇷 French | `fr` | ✅ Complete | 876 parameters |
| 🇺🇦 Ukrainian | `uk` | ✅ Complete | 855 parameters |

### 🏠 Supported Devices

- **ecoMAX810P-L TOUCH** controller from [Plum Sp. z o.o.](https://www.plum.pl/)
- **ecoMAX850R2-X** pellet boiler controller
- **ecoMAX360** boiler controller
- **ecoMAX860P2-N** boiler controller
- **ecoMAX860P3-V** boiler controller
- **ecoSOL500** solar collector system controller
- **ecosol301**
- **ecoSOL** solar thermal controller
- **SControl MK1** control module
- Other ecoNET300 compatible devices

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Entities](#entities)
4. [Contributing](#contributing)
5. [Acknowledgments](#acknowledgments)

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

**Host**: Local IP/domain of your device.

**Username**: Local username (NOT the username that you use to login to econet24.com!).

**Password**: Local password (NOT the password that you use to login to econet24.com!).

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

| Entity Key       | Description                  | Control                    | State Detection  |
| ---------------- | ---------------------------- | -------------------------- | ---------------- |
| `boiler_control` | Boiler ON/OFF control switch | `BOILER_CONTROL` parameter | `mode` parameter |

</details>

**Features:**

- **Direct Control**: Turn boiler ON/OFF with a simple switch
- **State Synchronization**: Switch state reflects actual boiler operation mode
- **API Integration**: Uses the ecoNET-300's native `BOILER_CONTROL` parameter
- **Real-time Updates**: Switch state updates based on current boiler mode

### Select Entities

The integration provides a heater mode selector that allows you to control the boiler operation mode directly from Home Assistant.

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key    | Description                    | Options              | API Parameter |
| ------------- | ------------------------------ | -------------------- | ------------- |
| `heater_mode` | Heater operation mode selector | Winter, Summer, Auto | Parameter 55  |

</details>

**Features:**

- **Winter Mode**: Full heating operation for cold weather
- **Summer Mode**: Hot water only operation for warm weather
- **Auto Mode**: Automatic mode selection based on conditions
- **Real-time Sync**: Mode selection reflects actual boiler operation
- **API Integration**: Uses ecoNET-300's native parameter 55

### Sensors

These sensors are retrieved from the `../econet/regParams` and `../econet/sysParams` endpoints.

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key                   | Description                               | Endpoint              |
| ---------------------------- | ----------------------------------------- | --------------------- |
| **Boiler & Heating**         |
| `boilerPower`                | Boiler output                             | `../econet/regParams` |
| `boilerPowerKW`              | Boiler power                              | `../econet/regParams` |
| `tempCO`                     | Heating temperature                       | `../econet/regParams` |
| `tempCOSet`                  | Heating target temperature                | `../econet/regParams` |
| `tempBack`                   | Return temperature                        | `../econet/regParams` |
| `statusCO`                   | Central heating status                    | `../econet/regParams` |
| **Hot Water (CWU)**          |
| `tempCWU`                    | Water heater temperature                  | `../econet/regParams` |
| `tempCWUSet`                 | Water heater set temperature              | `../econet/regParams` |
| `statusCWU`                  | Water heater status                       | `../econet/regParams` |
| **Temperature Sensors**      |
| `tempFeeder`                 | Feeder temperature                        | `../econet/regParams` |
| `tempFlueGas`                | Flue gas temperature                      | `../econet/regParams` |
| `tempExternalSensor`         | Outside temperature                       | `../econet/regParams` |
| `tempLowerBuffer`            | Lower buffer temperature                  | `../econet/regParams` |
| `tempUpperBuffer`            | Upper buffer temperature                  | `../econet/regParams` |
| **Mixer Temperatures**       |
| `mixerTemp1`                 | Mixer 1 temperature                       | `../econet/regParams` |
| `mixerTemp2`                 | Mixer 2 temperature                       | `../econet/regParams` |
| `mixerTemp3`                 | Mixer 3 temperature                       | `../econet/regParams` |
| `mixerTemp4`                 | Mixer 4 temperature                       | `../econet/regParams` |
| `mixerTemp5`                 | Mixer 5 temperature                       | `../econet/regParams` |
| `mixerTemp6`                 | Mixer 6 temperature                       | `../econet/regParams` |
| **System Status**            |
| `mode`                       | Boiler mode                               | `../econet/regParams` |
| `fanPower`                   | Fan power                                 | `../econet/regParams` |
| `thermostat`                 | Thermostat                                | `../econet/regParams` |
| **Fuel & Consumption**       |
| `fuelLevel`                  | Fuel level                                | `../econet/regParams` |
| `fuelConsum`                 | Fuel consumption                          | `../econet/regParams` |
| `fuelStream`                 | Fuel stream                               | `../econet/regParams` |
| **ecoSTER Room Thermostats** |
| `ecosterTemp1`               | Room temperature 1                        | `../econet/regParams` |
| `ecosterTemp2`               | Room temperature 2                        | `../econet/regParams` |
| `ecosterTemp3`               | Room temperature 3                        | `../econet/regParams` |
| `ecosterTemp4`               | Room temperature 4                        | `../econet/regParams` |
| `ecosterTemp5`               | Room temperature 5                        | `../econet/regParams` |
| `ecosterTemp6`               | Room temperature 6                        | `../econet/regParams` |
| `ecosterTemp7`               | Room temperature 7                        | `../econet/regParams` |
| `ecosterTemp8`               | Room temperature 8                        | `../econet/regParams` |
| `ecosterMode1`               | Room thermostat 1 mode                    | `../econet/regParams` |
| `ecosterMode2`               | Room thermostat 2 mode                    | `../econet/regParams` |
| `ecosterMode3`               | Room thermostat 3 mode                    | `../econet/regParams` |
| `ecosterMode4`               | Room thermostat 4 mode                    | `../econet/regParams` |
| `ecosterMode5`               | Room thermostat 5 mode                    | `../econet/regParams` |
| `ecosterMode6`               | Room thermostat 6 mode                    | `../econet/regParams` |
| `ecosterMode7`               | Room thermostat 7 mode                    | `../econet/regParams` |
| `ecosterMode8`               | Room thermostat 8 mode                    | `../econet/regParams` |
| **Lambda Sensor Module**     |
| `lambdaStatus`               | Lambda status                             | `../econet/regParams` |
| `lambdaSet`                  | Lambda set                                | `../econet/regParams` |
| `lambdaLevel`                | Lambda level                              | `../econet/regParams` |
| **ecoSOL 500 Solar System**  |
| `T1`                         | Collector Temperature                     | `../econet/regParams` |
| `T2`                         | Tank Temperature                          | `../econet/regParams` |
| `T3`                         | Tank Temperature                          | `../econet/regParams` |
| `T4`                         | Return Temperature                        | `../econet/regParams` |
| `T5`                         | Collector Temperature - Power Measurement | `../econet/regParams` |
| `T6`                         | Temperature Sensor                        | `../econet/regParams` |
| `TzCWU`                      | Hot Water Temperature                     | `../econet/regParams` |
| `P1`                         | Pump 1 Status                             | `../econet/regParams` |
| `P2`                         | Pump 2 Status                             | `../econet/regParams` |
| `H`                          | Output Status                             | `../econet/regParams` |
| `Uzysk_ca_kowity`            | Total Heat Output                         | `../econet/regParams` |
| **System Information**       |
| `quality`                    | Signal quality                            | `../econet/sysParams` |
| `signal`                     | Signal strength                           | `../econet/sysParams` |
| `softVer`                    | Module ecoNET version                     | `../econet/sysParams` |
| `controllerID`               | Controller name                           | `../econet/sysParams` |
| `moduleASoftVer`             | Module A version                          | `../econet/sysParams` |
| `moduleBSoftVer`             | Module B version                          | `../econet/sysParams` |
| `moduleCSoftVer`             | Module C version                          | `../econet/sysParams` |
| `moduleLambdaSoftVer`        | Module Lambda version                     | `../econet/sysParams` |
| `modulePanelSoftVer`         | Module Panel version                      | `../econet/sysParams` |
| `moduleEcoSTERSoftVer`       | Module ecoSTER version                    | `../econet/sysParams` |
| `transmission`               | Transmission                              | `../econet/regParams` |

</details>

### Binary Sensors

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key                   | Description                    | Endpoint              |
| ---------------------------- | ------------------------------ | --------------------- |
| **Pump Status**              |
| `pumpCOWorks`                | Central heating pump working   | `../econet/regParams` |
| `pumpCWUWorks`               | Hot water pump working         | `../econet/regParams` |
| `pumpSolarWorks`             | Solar pump working             | `../econet/regParams` |
| `pumpCirculationWorks`       | Circulation pump working       | `../econet/regParams` |
| `pumpFireplaceWorks`         | Fireplace pump working         | `../econet/regParams` |
| **Fan Status**               |
| `fanWorks`                   | Fan working                    | `../econet/regParams` |
| **System Components**        |
| `lighterWorks`               | Lighter working                | `../econet/regParams` |
| `feederWorks`                | Feeder working                 | `../econet/regParams` |
| `thermostat`                 | Thermostat                     | `../econet/regParams` |
| `statusCWU`                  | Hot water status               | `../econet/regParams` |
| **Network & Communication**  |
| `mainSrv`                    | Econet24.com server            | `../econet/regParams` |
| `wifi`                       | Wi-Fi connection               | `../econet/regParams` |
| `lan`                        | LAN connection                 | `../econet/regParams` |
| **ecoMAX850R2-X Specific**   |
| `contactGZC`                 | GZC contact                    | `../econet/regParams` |
| `contactGZCActive`           | GZC contact active             | `../econet/regParams` |
| **ecoSTER Room Thermostats** |
| `ecosterContacts1`           | Room thermostat 1 contacts     | `../econet/regParams` |
| `ecosterContacts2`           | Room thermostat 2 contacts     | `../econet/regParams` |
| `ecosterContacts3`           | Room thermostat 3 contacts     | `../econet/regParams` |
| `ecosterContacts4`           | Room thermostat 4 contacts     | `../econet/regParams` |
| `ecosterContacts5`           | Room thermostat 5 contacts     | `../econet/regParams` |
| `ecosterContacts6`           | Room thermostat 6 contacts     | `../econet/regParams` |
| `ecosterContacts7`           | Room thermostat 7 contacts     | `../econet/regParams` |
| `ecosterContacts8`           | Room thermostat 8 contacts     | `../econet/regParams` |
| `ecosterDaySched1`           | Room thermostat 1 day schedule | `../econet/regParams` |
| `ecosterDaySched2`           | Room thermostat 2 day schedule | `../econet/regParams` |
| `ecosterDaySched3`           | Room thermostat 3 day schedule | `../econet/regParams` |
| `ecosterDaySched4`           | Room thermostat 4 day schedule | `../econet/regParams` |
| `ecosterDaySched5`           | Room thermostat 5 day schedule | `../econet/regParams` |
| `ecosterDaySched6`           | Room thermostat 6 day schedule | `../econet/regParams` |
| `ecosterDaySched7`           | Room thermostat 7 day schedule | `../econet/regParams` |
| `ecosterDaySched8`           | Room thermostat 8 day schedule | `../econet/regParams` |
| **ecoSOL 500 Solar System**  |
| `fuelConsumptionCalc`        | Fuel consumption calculator    | `../econet/regParams` |
| `ecosrvHttps`                | ecoNET server HTTPS            | `../econet/regParams` |

</details>

### Number Entities

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key                            | Description                          | Endpoint              |
| ------------------------------------- | ------------------------------------ | --------------------- |
| **Temperature Setpoints**             |
| `tempCOSet`                           | Central heating temperature setpoint | `../econet/regParams` |
| `tempCWUSet`                          | Hot water temperature setpoint       | `../econet/regParams` |
| **Mixer Temperature Setpoints**       |
| `mixerSetTemp1`                       | Mixer 1 target temperature           | `../econet/regParams` |
| `mixerSetTemp2`                       | Mixer 2 target temperature           | `../econet/regParams` |
| `mixerSetTemp3`                       | Mixer 3 target temperature           | `../econet/regParams` |
| `mixerSetTemp4`                       | Mixer 4 target temperature           | `../econet/regParams` |
| `mixerSetTemp5`                       | Mixer 5 target temperature           | `../econet/regParams` |
| `mixerSetTemp6`                       | Mixer 6 target temperature           | `../econet/regParams` |
| **ecoSTER Room Thermostat Setpoints** |
| `ecosterSetTemp1`                     | Room thermostat 1 setpoint           | `../econet/regParams` |
| `ecosterSetTemp2`                     | Room thermostat 2 setpoint           | `../econet/regParams` |
| `ecosterSetTemp3`                     | Room thermostat 3 setpoint           | `../econet/regParams` |
| `ecosterSetTemp4`                     | Room thermostat 4 setpoint           | `../econet/regParams` |
| `ecosterSetTemp5`                     | Room thermostat 5 setpoint           | `../econet/regParams` |
| `ecosterSetTemp6`                     | Room thermostat 6 setpoint           | `../econet/regParams` |
| `ecosterSetTemp7`                     | Room thermostat 7 setpoint           | `../econet/regParams` |
| `ecosterSetTemp8`                     | Room thermostat 8 setpoint           | `../econet/regParams` |

</details>

---

## 🔧 Diagnostics

The integration includes comprehensive diagnostics support to help troubleshoot issues. Download detailed system information including entity states, API data, and configuration details.

**📖 [Complete Diagnostics Documentation](docs/DIAGNOSTICS.md)**

### Quick Start

1. Go to **Settings > Devices & Services** in Home Assistant
2. Find your **ecoNET300** integration
3. Click the **Download diagnostics** button
4. Share the redacted diagnostics file for support

**Features:**

- ✅ Automatic sensitive data redaction
- ✅ Complete API endpoint data
- ✅ Entity states and attributes
- ✅ System configuration details

---

## 📁 Project Structure

```
ecoNET-300-Home-Assistant-Integration/
├── custom_components/econet300/     # Home Assistant integration
├── docs/                            # Complete documentation
├── scripts/                         # Development and utility scripts
├── tests/                           # Integration tests
└── [standard project files]
```

### 🔧 **Essential Scripts** (in `scripts/`)

- **test_api_endpoints.py** - Test all API endpoints and validate responses
- **check_translations.py** - Validate translation files for consistency
- **language_finder.py** - Find and analyze language-specific content
- **README.md** - Scripts documentation and usage instructions

### 📚 **Essential Documentation** (in `docs/`)

- **DIAGNOSTICS.md** - Complete diagnostics documentation and troubleshooting guide
- **API_V1_DOCUMENTATION.md** - Complete API documentation (consolidated)
- **BOILER_CONTROL_README.md** - Boiler control documentation and setup
- **CLOUD_TRANSLATIONS.md** - Cloud translations documentation and usage
- **ecoSOL_DISCOVERY_SUMMARY.md** - ecoSOL device discovery and analysis
- **ecoMAX810P-L_PARAMETER_NAMES_ANALYSIS.md** - Parameter analysis for ecoMAX810P-L
- **ecoMAX850R2-X_DOCUMENTATION.md** - Complete ecoMAX850R2-X documentation
- **NEW_API_ENDPOINTS_DISCOVERED.md** - Newly discovered API endpoints
- **devices/** - Device-specific documentation and parameters
- **cloud_translations/** - Cloud translation data and references

---

## 📋 Versions

For detailed version information and changelog, see [CHANGELOG.md](CHANGELOG.md).

### Latest Features

- **Diagnostics Support**: Comprehensive diagnostics for troubleshooting issues
- **Boiler Control**: Turn boiler ON/OFF directly from Home Assistant
- **Temperature Setpoints**: Full control over heating and hot water temperatures
- **Mixer Support**: Smart entity creation for up to 6 mixer temperature setpoints
- **ecoSTER Integration**: Support for 8 room thermostats
- **ecoSOL 500 Support**: Solar collector system integration
- **Multi-language**: 6 language support (English, Polish, Czech, French, Ukrainian)

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

- **[@jontofront](https://github.com/jontofront)** - Current maintainer and developer
- **[@pblxpt](https://github.com/pblxpt)** - Original developer and maintainer up to v0.3.3
- **[@KirilKurkianec](https://github.com/KirilKurkianec)** - Contributor and supporter
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

_This README was last updated on 2025-07-18 after completing the comprehensive API discovery process._
