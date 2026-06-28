# Configuration Options

After the integration is set up, you can change its options from Home Assistant:

```text
Settings > Devices & services > ecoNET300 > Configure
```

## Available Options

- **Connection Settings** - update the local ecoNET300 host, username, or password.
- **Polling settings** - adjust how often the integration refreshes data from the controller.
- **Device settings** - choose how entities are grouped into Home Assistant devices.
- **Custom Entities** - expose additional parameters discovered from your controller.
- **Generate diagnostics report** - create a redacted diagnostics report for troubleshooting or GitHub issues.

## Polling Settings

Use **Polling settings** when you want to change how often Home Assistant reads data from the controller.

| Option | Default | Range | Description |
| ------ | ------- | ----- | ----------- |
| `regParams` polling interval | 15 seconds | 2-300 seconds | Live sensor values, such as temperatures, pumps, fans, and statuses. |
| `sysParams` polling interval | 300 seconds | 10-3600 seconds | Controller metadata and system information. |
| `editParams` polling interval | 300 seconds | 0-3600 seconds | Editable parameter catalog and values. Use `0` to disable periodic polling. |

For better graph granularity, reduce the **regParams polling interval**. This controls the live sensor values shown in Home Assistant history graphs.

The effective minimum for live polling is **5 seconds**, even if a lower value is entered.

## Connection Settings

Use **Connection Settings** to update the local device connection details without removing and re-adding the integration.

- **Host** - local IP address or hostname of the ecoNET300 module.
- **Username** - local ecoNET300 username.
- **Password** - local ecoNET300 password.

These are local device credentials, not econet24.com cloud credentials.

## Device Settings

Use **Device settings** to choose how Home Assistant groups entities:

- **Split** - keep separate devices for boiler, mixers, lambda, ecoSTER, and other components.
- **Single** - expose all entities under one merged ecoNET300 device.

Changing this option does not change entity IDs.

## Custom Entities

Use **Custom Entities** to expose additional parameters discovered from your controller that are not included by default.

The flow lets you:

- Choose an API endpoint to browse.
- Select parameters available on your controller.
- Configure the entity name, device group, entity type, category, unit, device class, and precision where applicable.

## Diagnostics Report

Use **Generate diagnostics report** when opening a GitHub issue or troubleshooting a controller-specific problem.

The action creates a redacted diagnostics report and writes it to `homeassistant.log` with the marker:

```text
ECONET300_DIAGNOSTICS_REPORT
```

Attach the matching log block or the standard Home Assistant diagnostics download when reporting an issue.
