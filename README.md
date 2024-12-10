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

These sensors are retrieved from the `../econet/regParams` endpoint. Below is the list of available entity keys and their descriptions:

| sensor Key           | Description                              |
|----------------------|------------------------------------------|
| `tempFeeder`         | Temperature of the feeder mechanism      |
| `fuelLevel`          | Current fuel level in the system         |
| `tempCO`             | Current fireplace temperature            |
| `tempCOSet`          | Desired fireplace set temperature        |
| `statusCWU`          | Status of the hot water (CWU) system     |
| `tempCWUSet`         | Desired hot water (CWU) temperature      |
| `tempFlueGas`        | Exhaust temperature reading              |
| `mode`               | Current operational mode of the device   |
| `fanPower`           | Current fan power usage                  |
| `thermostat`         | Thermostat status or set temperature     |
| `tempExternalSensor` | Outside (external) temperature           |


### Binary Sensors

These binary sensors are retrieved from the `../econet/regParams` endpoint. Below is the list of available entity keys and their descriptions:
| Entity Key           | Description                                 |
|----------------------|---------------------------------------------|
| `lighter`            | Indicates if the lighter is active          |
| `pumpCOWorks`        | Indicates if the fireplace pump is working  |
| `fanWorks`           | Indicates if the fan is currently active    |
| `pumpFireplaceWorks` | Indicates if the fireplace pump is working  |
| `pumpCWUWorks`       | Indicates if the hot water (CWU) pump is active |


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
