# ecoNET-300 Home Assistant Integration

[![Code Formatter](https://img.shields.io/badge/Code%20Formatter-Ruff-000000?style=for-the-badge&logo=python)](https://github.com/astral-sh/ruff)
[![Latest Release](https://img.shields.io/github/v/release/jontofront/ecoNET-300-Home-Assistant-Integration?style=for-the-badge)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/releases)
[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5?style=for-the-badge&logo=homeassistant)](https://github.com/hacs/integration)
[![Active Installs](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.econet300.total&label=Active%20Installs&style=for-the-badge&logo=homeassistant&color=41BDF5)](https://analytics.home-assistant.io)
[![HACS Action](https://img.shields.io/badge/HACS%20Action-passing-brightgreen?style=for-the-badge&logo=github)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hacs.yml)
[![Stability](https://img.shields.io/badge/Stability-Stable-2ecc71?style=for-the-badge)](https://guidelines.denpa.pro/stability#stable)
[![Hassfest](https://img.shields.io/badge/Hassfest-Validated-brightgreen?style=for-the-badge&logo=homeassistant)](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/actions/workflows/hassfest.yaml)

**Note:** This repository is a fork of the original [pblxptr/ecoNET-300-Home-Assistant-Integration](https://github.com/pblxptr/ecoNET-300-Home-Assistant-Integration). Most of the work was done by [@pblxpt](https://github.com/pblxpt), and we are very grateful for their efforts. Additionally, I maintained and supported this code up to version v0.3.3.

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
- **Dynamic Entity Creation**: 165+ entities auto-discovered from your boiler's menu (v1.2.0+)
- **Boiler Control**: Turn your boiler ON/OFF directly from Home Assistant
- **Real-time Monitoring**: Monitor temperatures, fuel levels, and system status
- **Comprehensive API Access**: Access to 80+ API endpoints
- **Multiple Entity Types**: Sensors, Binary Sensors, Calendars, Events, Switches, Select, and Number entities
- **Parameter Locking**: Device-side locks reflected in Home Assistant UI
- **Repair Issues**: Automatic connection failure detection with one-click fix
- **Diagnostics Support**: Download diagnostics with core API data plus optional RM/`editParams` snapshots (v1.2.5+)

### 🌐 Language Support

The integration supports **6 languages** with comprehensive translations:

| Language     | Code | Status      | Coverage         |
| ------------ | ---- | ----------- | ---------------- |
| 🇬🇧 English   | `en` | ✅ Complete | Base language    |
| 🇵🇱 Polish    | `pl` | ✅ Complete | Full translation |
| 🇨🇿 Czech     | `cs` | ✅ Complete | 348 parameters   |
| 🇫🇷 French    | `fr` | ✅ Complete | 876 parameters   |
| 🇺🇦 Ukrainian | `uk` | ✅ Complete | 855 parameters   |

### 🏠 Supported Devices

- **ecoMAX810P-L TOUCH** controller from [Plum Sp. z o.o.](https://www.plum.pl/)
- **ecoMAX850R2-X** pellet boiler controller
- **ecoMAX360** boiler controller
- **ecoMAX860P2-N** boiler controller
- **ecoMAX860P3-V** boiler controller
- **ecoSOL 500** solar collector system controller
- **ecoSOL 301** solar controller (flat `regParams` / `T1`, `P1`, …)
- **ecoSOL** solar thermal controller
- **SControl MK1** control module
- Other ecoNET300 compatible devices

---

## 📋 Table of Contents

1. [Installation](#-installation)
2. [Upgrading](#-upgrading)
3. [Configuration](#-configuration)
4. [Entities](#-entities)
5. [Diagnostics](#-diagnostics)
6. [Documentation](#-documentation)
7. [Versions](#-versions)
8. [Contributing](#-contributing)
9. [Support](#-support)

---

## 🚀 Installation

### HACS (Recommended)

1. Install and configure [HACS](https://hacs.xyz/).
2. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) using:

```text
https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration
```

3. In HACS, search for **"ecoNET300"**, install the integration.
4. Restart Home Assistant.

### Manual Installation

1. Download or clone this repository.
2. Copy `custom_components/econet300` into your `<config_directory>/custom_components/`.
3. Restart Home Assistant.

---

## 🔄 Upgrading

**v1.2.0+ introduces significant new features** including 165+ dynamic entities, parameter locking, and the repair issues system. **No manual migration is required** — your existing configuration keeps working.

After upgrading:

1. Restart Home Assistant
2. Check **Settings → Devices & Services → ecoNET300** for new entities
3. New CONFIG category entities are disabled by default — enable as needed

**📖 [Complete Migration Guide](docs/MIGRATION.md)**

---

## 🧰 Configuration

Integrate ecoNET300 via the user interface:

[![Add integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=econet300)

Enter your local device **Host** (IP/domain) and **local** credentials — not your econet24.com cloud login.

After setup, open **Settings → Devices & Services → ecoNET300 → Configure** to adjust connection settings, polling intervals, device grouping, custom entities, and to generate diagnostics reports.

> Tip: For better graph granularity, lower the **regParams polling interval** in **Polling settings** (default 15s, minimum 5s).

**📖 [Complete Configuration Guide](docs/CONFIGURATION.md)** — manual setup steps, polling, device grouping, and custom entities.

---

## 🏠 Entities

The integration provides multiple entity types:

| Type           | Count | Description                            |
| -------------- | ----- | -------------------------------------- |
| Sensors        | 50+   | Temperature, status, alarms            |
| Binary Sensors | 25+   | Pumps, fans, connections, alarms       |
| Calendars      | 1-20  | Weekly heating schedules per component |
| Events         | 1     | Boiler alarm triggered / cleared       |
| Switches       | 1     | Boiler ON/OFF control                  |
| Select         | 1+    | Heater mode, dynamic parameters        |
| Number         | 15+   | Temperature setpoints                  |

Starting with v1.2.0, the integration automatically discovers **165+ additional entities** from your boiler's remote menu via the `mergedData` API endpoint, with automatic type detection, category grouping, parameter locking, and mixer/ecoSTER support.

**📖 [Complete Entity Reference](docs/ENTITIES.md)** — full list of all entities with descriptions.

Related usage guides:

- **[Heating Schedules](docs/SCHEDULES.md)** — display weekly schedules as calendar entities
- **[Alarms & Events](docs/ALARMS_AND_EVENTS.md)** — alarm monitoring and push notifications
- **[Fuel Consumption](docs/FUEL_CONSUMPTION.md)** — track total fuel usage with the Riemann Sum helper

---

## 🔧 Diagnostics

The integration includes comprehensive diagnostics support to help troubleshoot issues. Downloads include coordinator data, core endpoint snapshots, and **extended snapshots** (v1.2.5+): RM endpoints plus optional `editParams`, with automatic sensitive-data redaction.

To download: **Settings → Devices & Services → ecoNET300 → Download diagnostics**. For a one-click triage report (useful for GitHub issues, heat pumps, and controller variants), use **Configure → Generate diagnostics report**.

**📖 [Complete Diagnostics Documentation](docs/DIAGNOSTICS.md)**

---

## 📚 Documentation

All documentation lives in the [`docs/`](docs/) folder. Start here:

### Setup & Usage

| Guide | Description |
| ----- | ----------- |
| [Configuration](docs/CONFIGURATION.md) | Configure menu, polling, device grouping, custom entities |
| [Migration](docs/MIGRATION.md) | Upgrading between versions |
| [Entities](docs/ENTITIES.md) | Complete entity reference |
| [Heating Schedules](docs/SCHEDULES.md) | Display schedules as calendar entities |
| [Alarms & Events](docs/ALARMS_AND_EVENTS.md) | Alarm monitoring and automations |
| [Fuel Consumption](docs/FUEL_CONSUMPTION.md) | Track total fuel usage |
| [Boiler Control](docs/BOILER_CONTROL_README.md) | Boiler ON/OFF switch behavior |
| [Diagnostics](docs/DIAGNOSTICS.md) | Diagnostics and troubleshooting |

### Reference & API

| Guide | Description |
| ----- | ----------- |
| [API v1 Documentation](docs/API_V1_DOCUMENTATION.md) | Complete API documentation (80+ endpoints) |
| [API Construction Guide](docs/API_CONSTRUCTION_GUIDE.md) | How API requests are built |
| [Dynamic Entity Validation](docs/DYNAMIC_ENTITY_VALIDATION.md) | Dynamic entity system (v1.2.0+) |
| [New API Endpoints](docs/NEW_API_ENDPOINTS_DISCOVERED.md) | Newly discovered endpoints |

### Device-Specific

| Device | Description |
| ------ | ----------- |
| [ecoMAX810P-L](docs/devices/ecoMAX810P-L/README.md) | Most feature-rich pellet controller |
| [ecoMAX360](docs/devices/ecoMAX360/README.md) | Boiler / heat pump controller |
| [ecoSOL 500](docs/devices/ecoSOL500/README.md) | Solar collector controller |
| [ecoMAX850R2-X](docs/ecoMAX850R2-X_DOCUMENTATION.md) | Pellet boiler controller |
| [ecoSOL Discovery](docs/ecoSOL_DISCOVERY_SUMMARY.md) | ecoSOL line discovery summary |

### Developer

| Guide | Description |
| ----- | ----------- |
| [Architecture](docs/ARCHITECTURE.md) | High-level integration architecture |
| [Developer Tools](docs/DEVELOPER_TOOLS_GUIDE.md) | Scripts and tooling |
| [Cloud Translations](docs/CLOUD_TRANSLATIONS.md) | Translation references and workflow |

---

## 📋 Versions

### What's New in v1.3.0-beta.6

- **Schedule Calendar Entities**: Heating schedules are now native Home Assistant **Calendar** entities instead of text-based sensors. Each schedule type gets its own calendar entity with weekly recurring events. Supported controllers: ecoMAX810P-L, ecoMAX860 series, ecoMAX920 series, SControl MK1/EM892.
- **DRY refactoring**: Schedule decoding helpers extracted into reusable functions for future schedule editing support.
- **Multi-model test coverage**: Schedule tests run against all 9 fixture models with schedule data.

**📖 [Full Changelog](CHANGELOG.md)** — complete version history and release notes.

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch
3. Make your changes and test thoroughly
4. Submit a pull request

See the [Architecture](docs/ARCHITECTURE.md) and [Developer Tools](docs/DEVELOPER_TOOLS_GUIDE.md) guides to get started.

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

1. Check the [Documentation](#-documentation)
2. Search existing [Issues](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues)
3. Create a new issue with detailed information about your problem (attach a diagnostics report when possible)

---

_This README was last updated on 2026-06-30 for v1.3.0-beta.6._
