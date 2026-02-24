# Migration Guide

This guide helps you upgrade between versions of the ecoNET-300 Home Assistant Integration.

---

## Version Compatibility Matrix

| From Version | To Version | Migration Required | Notes                                |
| ------------ | ---------- | ------------------ | ------------------------------------ |
| v1.1.15      | v1.2.x     | No                 | Auto-discovery of new entities       |
| v1.1.x       | v1.1.15    | No                 | Direct upgrade                       |
| v0.3.3       | v1.x       | Recommended        | Re-add integration for full features |

---

## Upgrading from v1.1.15 to v1.2.x

### What's New in v1.2.x

**Major Features:**

- **Dynamic Entity System**: 165+ new entities from the boiler's remote menu (`mergedData` API)
- **Parameter Locking**: Device-locked settings displayed with lock icon (`mdi:lock`)
- **Repair Issues System**: Automatic detection of connection failures with one-click fix
- **Reconfiguration Flow**: Update connection settings via integration options
- **Mixer Device Support**: Entities correctly grouped by mixer device (Mixer 1-4)
- **ecoSTER Panel Detection**: Smart filtering for ecoSTER-related entities

**New Entity Types:**

- Dynamic Number entities (temperature setpoints, heating curves, etc.)
- Dynamic Switch entities (binary on/off parameters)
- Dynamic Select entities (multi-option parameters)
- Read-only sensors for locked parameters

### Upgrade Steps

#### Step 1: Backup (Recommended)

Before upgrading, download your current diagnostics:

1. Go to **Settings → Devices & Services**
2. Find your **ecoNET300** integration
3. Click **Download diagnostics**
4. Save the file for reference

#### Step 2: Update the Integration

**Via HACS (Recommended):**

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Find **ecoNET300**
4. Click **Update** (or reinstall if needed)

**Manual Installation:**

1. Download the latest release from [GitHub Releases](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/releases)
2. Replace the `custom_components/econet300/` folder with the new version
3. Ensure all files are replaced completely

#### Step 3: Restart Home Assistant

1. Go to **Settings → System → Restart**
2. Click **Restart**
3. Wait for Home Assistant to fully restart

#### Step 4: Verify the Upgrade

1. Go to **Settings → Devices & Services**
2. Find your **ecoNET300** integration
3. Check the device page for new entities
4. Verify existing entities still work correctly

### Entity Changes

| Aspect                | Before (v1.1.15) | After (v1.2.x)                        |
| --------------------- | ---------------- | ------------------------------------- |
| **Entity Count**      | ~50-80 entities  | 165+ entities (dynamic)               |
| **Entity IDs**        | Stable           | Stable (no changes to existing)       |
| **New Entities**      | N/A              | Disabled by default (CONFIG category) |
| **Existing Entities** | Working          | Continue working unchanged            |

### New Entity Categories

v1.2.x introduces entity categories with different default states:

| Category           | Default State | Visibility | Description                                 |
| ------------------ | ------------- | ---------- | ------------------------------------------- |
| **DIAGNOSTIC**     | Enabled       | Visible    | System information and status               |
| **CONFIG**         | Disabled      | Visible    | Configuration parameters (enable as needed) |
| **Uncategorized**  | Enabled       | Visible    | General sensors and controls                |
| **Service**        | Disabled      | Hidden     | Service-level parameters (require password) |
| **Advanced**       | Disabled      | Hidden     | Advanced configuration parameters           |

### Why Are Some Entities Disabled by Default?

Following Home Assistant best practices, configuration entities are **disabled by default** to:

- Keep the user interface clean and manageable
- Prevent accidental changes to boiler settings
- Allow users to enable only the entities they need
- Reduce system load from unused entities

**Affected entity types:**

- **Number entities** (temperature setpoints, heating curves, timers)
- **Switch entities** (on/off configuration parameters)
- **Select entities** (mode selections, multi-option settings)

### Service and Advanced Parameters

**Service Parameters** and **Advanced Parameters** are both **disabled AND hidden** by default:

| Parameter Type | Why Hidden                             | How to Access              |
| -------------- | -------------------------------------- | -------------------------- |
| **Service**    | Require service password on the boiler | Enable via entity registry |
| **Advanced**   | Technical settings for experts only    | Enable via entity registry |

These parameters appear under separate devices:

- **Service Parameters** device
- **Advanced Parameters** device

### How to Enable Disabled Entities

#### Method 1: Via Device Page

1. Go to **Settings → Devices & Services → ecoNET300**
2. Click on your boiler device (or Service/Advanced Parameters device)
3. Scroll down to see all entities
4. Disabled entities appear grayed out with a toggle icon
5. Click the entity → Click **Enable**

#### Method 2: Via Entity Registry

1. Go to **Settings → Devices & Services → Entities**
2. Search for "econet" to filter entities
3. Click on a disabled entity
4. Toggle **Enabled** to ON

#### Method 3: Enable Hidden Entities

For Service and Advanced parameters that are hidden:

1. Go to **Settings → Devices & Services → Entities**
2. Click the filter icon (three lines)
3. Check **Show disabled entities**
4. Find and enable the entities you need

### Parameter Locking

New in v1.2.x: Some parameters may be **locked by the boiler** and cannot be changed remotely.

**How to identify locked parameters:**

- Lock icon (`mdi:lock`) displayed on the entity
- Entity state shows as "unavailable" in Home Assistant
- `lock_reason` attribute explains why it's locked

**Common lock reasons:**

- "Locked by service mode"
- "Locked by hardware configuration"
- "Read-only parameter"

### Repair Issues System

New in v1.2.x: Automatic detection of connection problems.

**How it works:**

1. After 5 consecutive connection failures, a repair issue is created
2. Go to **Settings → System → Repairs**
3. Click on the ecoNET300 repair issue
4. Update connection settings if needed
5. Repair auto-resolves when connection is restored

---

## Upgrading from v0.3.3 to v1.x

### Recommended: Fresh Installation

Due to significant architectural changes, we recommend:

1. **Remove** the old integration:
   - Go to **Settings → Devices & Services**
   - Find ecoNET300 → Click **Delete**

2. **Delete** old files:
   - Remove `custom_components/econet300/` folder

3. **Install** the new version:
   - Follow the [Installation Guide](../README.md#installation)

4. **Re-add** the integration:
   - Follow the [Configuration Guide](../README.md#configuration)

### What's Changed Since v0.3.3

- Complete API refactoring with 48+ endpoints
- New entity types (Switches, Selects, Numbers)
- Multi-language support (6 languages)
- Diagnostics support
- ecoSTER thermostat support
- ecoSOL solar collector support
- Boiler ON/OFF control
- Temperature setpoint control

---

## Troubleshooting

### Entities Not Appearing After Upgrade

1. **Clear browser cache**: Hard refresh the Home Assistant UI
2. **Check integration status**: Ensure no errors in Settings → Devices & Services
3. **Review logs**: Check Home Assistant logs for errors
4. **Restart again**: Sometimes a second restart helps

### Entity IDs Changed

Entity IDs should remain stable between versions. If you notice changes:

1. Check if the entity was renamed (old entity may be orphaned)
2. Use **Settings → Devices → ecoNET300 → Entity** to find new IDs
3. Update automations/scripts with new entity IDs

### Connection Issues After Upgrade

1. **Verify device IP**: Ensure your ecoNET300 device IP hasn't changed
2. **Check credentials**: Verify local username/password (not econet24.com credentials)
3. **Use Repair Flow**: Go to integration options to update connection settings
4. **Check network**: Ensure Home Assistant can reach the device

### Dynamic Entities Not Loading

If the 165+ dynamic entities don't appear:

1. **Check controller support**: Not all controllers support the RM/mergedData API
2. **Supported controllers**: ecoMAX810P-L, ecoMAX850R2-X, ecoMAX860P2-N, ecoMAX860P3-V
3. **Unsupported controllers**: ecoSOL500, ecoSOL, SControl MK1, ecoMAX360i (limited support)
4. **Legacy-only modules**: Some ecoNET300 module firmware (e.g. v3.2.3879 on ecoMAX860D3-HB) only exposes sysParams, regParams, regParamsData. The integration auto-detects this (2s probe) and runs with legacy entities only; you will see "RM endpoint not available (legacy-only module)" in the logs. This is expected and the integration works normally with fewer entities.
5. **Review logs**: Search for "mergedData" or "RM endpoint" in Home Assistant logs

### Getting Help

If you encounter issues:

1. **Download diagnostics**: Settings → Devices → ecoNET300 → Download diagnostics
2. **Search issues**: Check [GitHub Issues](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues)
3. **Create new issue**: Include diagnostics file and describe the problem

---

## Migration Checklist

Use this checklist when upgrading:

- [ ] Downloaded diagnostics backup
- [ ] Updated integration files
- [ ] Restarted Home Assistant
- [ ] Verified existing entities work
- [ ] Checked for new entities
- [ ] Enabled desired CONFIG entities
- [ ] Updated automations if needed
- [ ] Tested boiler controls

---

## FAQ

### Q: Will I lose my automations?

**A:** No. Entity IDs remain stable, so existing automations continue to work.

### Q: Do I need to reconfigure the integration?

**A:** No. Your existing configuration (host, username, password) is preserved.

### Q: Why are some new entities disabled?

**A:** CONFIG category entities are disabled by default to keep the UI clean. Enable them as needed.

### Q: Can I downgrade back to v1.1.15?

**A:** Yes. Replace the files with the old version and restart. Your config entry is compatible.

### Q: What if my controller isn't supported?

**A:** Basic functionality works on all controllers. Dynamic entities require specific controller support.

---

<!-- Last updated: 2025-01-26 for v1.2.0a5 -->
