# ecoNET300 Home Assistant Integration

[![Code_formatter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![HACS Action](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hacs.yml/badge.svg)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hacs.yml)
[![stability-alpha](https://img.shields.io/badge/stability-alpha-f4d03f.svg)](https://guidelines.denpa.pro/stability#alpha)
[![Validate with hassfest](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hassfest.yaml)

## Features

- **Local Operation**: No dependency on econet24.com cloud services
- **Easy Configuration**: Integrate directly via Home Assistant UI
- **Boiler Control**: Turn your boiler ON/OFF directly from Home Assistant
- **Real-time Monitoring**: Monitor temperatures, fuel levels, and system status
- **Multiple Entity Types**: Sensors, Binary Sensors, Switches, and Number entities

## Supported Devices

- ecoMAX810P-L TOUCH controller from [Plum Sp. z o.o.](https://www.plum.pl/)
- Other ecoNET300 compatible devices

## Quick Start

1. Install via HACS (recommended) or manual installation
2. Add integration via Home Assistant UI
3. Enter your device IP and local credentials
4. Enjoy full control and monitoring of your ecoNET300 device!

## Entity Types

- **Sensors**: Temperature, power, fuel level, and system status
- **Binary Sensors**: Pump status, fan status, and system indicators
- **Switches**: Boiler ON/OFF control
- **Number Entities**: Temperature setpoints and configuration

For detailed information, see the [full README](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration). 