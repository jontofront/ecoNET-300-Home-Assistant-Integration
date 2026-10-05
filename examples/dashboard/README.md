# Boiler Dashboard Example

This example shows how to build a simple Home Assistant `picture-elements` dashboard for an ecoNET300-controlled heating system.

It uses only built-in Home Assistant Lovelace functionality and does **not** require a custom frontend card.

## Files

- `boiler-schema.svg` — generic heating schematic created for this repository
- `boiler-picture-elements.yaml` — example Home Assistant card configuration

## Installation

1. Create a directory in your Home Assistant configuration:

   ```text
   /config/www/boiler/
   ```

2. Copy `boiler-schema.svg` to:

   ```text
   /config/www/boiler/boiler-schema.svg
   ```

3. In Home Assistant, the file should then be available as:

   ```text
   /local/boiler/boiler-schema.svg
   ```

4. Add a **Manual card** to a dashboard and paste the contents of `boiler-picture-elements.yaml`.

5. Replace the example entity IDs with the entities from your own ecoNET300 installation.

## Important: entity IDs may differ

Home Assistant entity IDs depend on your device name, existing entities and migration history. The IDs in the YAML are examples only.

Use **Settings → Devices & services → ecoNET300 → Entities** or **Developer tools → States** to find the correct entities.

Relevant ecoNET keys commonly used by this dashboard include:

| ecoNET key | Purpose |
| --- | --- |
| `tempCO` | Heating / boiler temperature |
| `tempCOSet` | Heating target temperature |
| `tempBack` | Return temperature |
| `tempFlueGas` | Flue gas temperature |
| `tempExternalSensor` | Outside temperature |
| `tempCWU` | Domestic hot water temperature |
| `tempCWUSet` | Domestic hot water target temperature |
| `mixerTemp1` | Mixer 1 temperature |
| `pumpCWUWorks` | DHW pump running state |
| `mixerPumpWorks1` / controller-specific mixer running key | Mixer pump running state |

See the full [Entity Reference](../../docs/ENTITIES.md) for the entities supported by the integration.

## Browser cache note

Home Assistant serves files from `/config/www/` under `/local/`. When replacing an SVG, your browser may continue showing an older cached version.

If that happens, change the version query in the card:

```yaml
image: /local/boiler/boiler-schema.svg?v=2
```

Increment the number again whenever necessary.

## Customizing the layout

The example uses percentages for all element positions:

```yaml
style:
  left: 48.75%
  top: 9.5%
```

This keeps the overlay aligned with the SVG when the card is resized.

You can adjust the positions visually by changing `left` and `top`. For temperature labels, the example uses small white bold text. Pump icons use Home Assistant state coloring.

## License

The SVG in this directory is an original generic schematic created for this repository and is covered by the repository's MIT License. It is not copied from the ecoNET24 web interface.
