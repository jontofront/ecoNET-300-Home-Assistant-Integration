# ecoNET300 Home Assistant integration

[![Code_formatter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![HACS Action](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hacs.yml/badge.svg)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hacs.yml)
[![stability-alpha](https://img.shields.io/badge/stability-alpha-f4d03f.svg)](https://guidelines.denpa.pro/stability#alpha)
[![Validate with hassfest](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hassfest.yaml)

**Note:** This repository is a fork of the original [pblxptr/ecoNET-300-Home-Assistant-Integration](https://github.com/pblxptr/ecoNET-300-Home-Assistant-Integration). Most of the work was done by [@pblxpt](https://github.com/pblxpt), and we are very grateful for their efforts.
**Additionally, I maintained and supported this code up to version v0.3.3.**

<div align="center">

| Home Assistant  | ecoNET300     | device        |
| --------------- | ------------- | ------------- |
| <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/ha.png" width="100" height="100" />                |   <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/econet.webp" width="95" height="95" />            | <img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/econet300_device.jpg" width="100" height="100" /> |

</div>

## Overview
he **ecoNET300 Home Assistant Integration** allows local control and monitoring of ecoNET300 devices directly from Home Assistant. It communicates over your local network via the ecoNET300’s native REST API, avoiding any external cloud services.

- **Local Operation**: No dependency on econet24.com cloud services.
- **Easy Configuration**: Integrate directly via Home Assistant UI.
- **Tested With**: ecoMAX810P-L TOUCH controller from [Plum Sp. z o.o.](https://www.plum.pl/)

## Table of Contents
1. [ecoNET300 Home Assistant Integration](#econet300-home-assistant-integration)
2. [Overview](#overview)
3. [Versions](#versions)
   - [Migrating to v1.0.0_beta](#migrating-to-v100_beta)
4. [Example](#example)
5. [Installation](#installation)
   - [HACS (Recommended)](#hacs-recommended)
   - [Manual Installation](#manual-installation)
6. [Configuration](#configuration)
7. [Entities](#entities)
   - [Sensors](#sensors)
   - [Binary Sensors](#binary-sensors)
8. [Contributing](#contributing)
9. [Acknowledgments](#acknowledgments)
10. [Disclaimer](#disclaimer)

## versions
* v0.3.3 - version is stable. Most of the work was done by @pblxpt, for which we're very thankful as the community.
* v1.0.0 - A development version that retrieves more data from the API. It may be unstable, and upgrades from previous versions are not supported.

### Migrating to v1.0.0_beta

> **Important**: This release resets versioning. To upgrade:
> 1. Remove the existing integration.
> 2. Install v1.0.0_beta fresh.
> 3. Reconfigure as instructed below.


## Example
<div align="center">


<img src="https://raw.githubusercontent.com/jontofront/ecoNET-300-Home-Assistant-Integration/master/images/sensors.png" />             

</div>

## Installation
### HACS (Recommended)
1. Install and configure [HACS](https://hacs.xyz/).
2. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) using:
```
https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration
```
3. In HACS, search for **"ecoNET300"**, install the integration.
4. Restart Home Assistant.

## Manual Installation
1. Download or clone this repository.
2. Copy `custom_components/econet300` into your `<config_directory>/custom_components/`.

```
<config directory>/
|-- custom_components/
|   |-- econet300/
|       |-- [...]
```
3. Restart Home Assistant.

## Configuration

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
<br>

## Entities

### Sensors

These sensors are retrieved from the `../econet/regParams` and `../econet/sysParams` endpoints. Below is the list of available entity keys, their descriptions, and the corresponding API endpoint keys:
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
| `moduleASoftVer`     | Software version of Module A                             | `../econet/sysParams` |
| `moduleBSoftVer`     | Software version of Module B                             | `../econet/sysParams` |
| `moduleCSoftVer`     | Software version of Module C                             | `../econet/sysParams` |
| `moduleLambdaSoftVer`| Software version of the lambda module                    | `../econet/sysParams` |
| `modulePanelSoftVer` | Software version of the control panel                    | `../econet/sysParams` |
</details>

### Binary Sensors

These binary sensors are retrieved from the `../econet/regParams` and `../econet/sysParams` endpoints. Below is the list of available entity keys, their descriptions, and the corresponding API endpoint keys:
<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key           | Description                                      | Endpoint              |
|----------------------|--------------------------------------------------|-----------------------|
| `lighter`            | Indicates if the lighter is active               | `../econet/regParams` |
| `pumpCOWorks`        | Indicates if the fireplace pump is working       | `../econet/regParams` |
| `fanWorks`           | Indicates if the fan is currently active         | `../econet/regParams` |
| `pumpFireplaceWorks` | Indicates if the fireplace pump is working       | `../econet/regParams` |
| `pumpCWUWorks`       | Indicates if the hot water (CWU) pump is active  | `../econet/regParams` |
| `mainSrv`            | Indicates if the main server is operational      | `../econet/sysParams` |
| `wifi`               | Indicates if the Wi-Fi connection is active      | `../econet/sysParams` |
| `lan`                | Indicates if the LAN connection is active        | `../econet/sysParams` |
</details>

### Number Entities

These number entities are retrieved from the `../econet/rmCurrentDataParamsEdits` endpoint. Below is the list of available entity keys, their descriptions, and the corresponding API endpoint keys:

<details>
  <summary>**👉 Click here to expand the table**</summary>

| Entity Key           | Description                                  | Endpoint                             |
|----------------------|----------------------------------------------|--------------------------------------|
| `tempCOSet`          | Desired fireplace set temperature            | `../econet/rmCurrentDataParamsEdits` |
| `tempCWUSet`         | Desired hot water (CWU) set temperature      | `../econet/rmCurrentDataParamsEdits` |
</details>

## Contributing

We welcome contributions to improve the ecoNET300 integration! Please follow these steps to ensure your contributions align with Home Assistant's development guidelines:

1. Familiarize yourself with the [Home Assistant Contribution Guidelines](https://developers.home-assistant.io/docs/development_submitting/).
2. Fork this repository and create a new branch for your changes.
3. Write code that follows Home Assistant's [Coding Standards](https://developers.home-assistant.io/docs/development_guidelines/).
4. Update documentation to reflect any changes or new functionality.
5. Open a pull request with a clear description of your changes and reference any related issues.

Thank you for contributing to the Home Assistant community!

**Acknowledgments:**  
- [@pblxpt](https://github.com/pblxpt) for the original integration code.  
- [@denpamusic](https://github.com/denpamusic) for guidance.
<a href="https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=jontofront/ecoNET-300-Home-Assistant-Integration" />
</a>


## Disclaimer

**Use at your own risk.**  
This software is provided as-is, for educational purposes. The authors and contributors hold no responsibility for any harm, data loss, or damage caused by using this integration.
