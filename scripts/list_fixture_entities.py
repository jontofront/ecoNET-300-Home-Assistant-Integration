"""Generate a markdown table of fixture parameters as pseudo-entities.

Uses ecoMAX810P-L fixtures to reconstruct parameter-to-category mapping:
- mergedData.json: Complete merged parameter data with names, keys, units, categories, etc.
- rmStructure.json: Structure mapping parameters to categories (supports multiple categories per parameter)
- rmCatsNames.json: Category names

Output columns:
- Device: Target device for the entity
- Via device: Parent device
- Entity name: Human-readable parameter name
- Entity key: Home Assistant entity key with category prefix (snake_case)
- Entity type: sensor (Information), number (basic/service/advanced), or sensor (read-only)
- Category: Category from rmCatsNames (parameters can appear in multiple categories)
- Unit: Parameter unit

Shows how multiple category entity creation works:
- Information categories → read-only sensors (always visible)
- Basic categories → editable numbers (always visible)
- Service/Advanced categories → editable numbers (controlled by show_service_parameters)

Also generates a separate endpoints list.

Usage (from repo root):
    python scripts/list_fixture_entities.py

Output is written to: tests/test_reports/fixture_entities_report.md
"""

from __future__ import annotations

import json
from pathlib import Path


def get_parameter_type(category: str) -> str:
    """Determine parameter type (basic/service/advanced) from category."""
    if not category:
        return "basic"
    cat_lower = category.lower()
    if "service" in cat_lower:
        return "service"
    if "advanced" in cat_lower:
        return "advanced"
    return "basic"


def is_information_category(category: str) -> bool:
    """Check if category is an Information category (read-only sensor)."""
    if not category:
        return False
    category_lower = category.lower()
    return "information" in category_lower


def get_device_name(category: str, param_type: str) -> str:
    """Determine device name based on category and parameter type."""
    if param_type == "service":
        return "Service Parameters"
    if param_type == "advanced":
        return "Advanced Parameters"
    # Check for mixer categories
    if "mixer" in category.lower():
        for i in range(1, 7):
            if str(i) in category:
                return f"Mixer device {i}"
    if "lambda" in category.lower():
        return "Module Lambda"
    if "ecoster" in category.lower():
        for i in range(1, 7):
            if str(i) in category:
                return f"ecoSTER {i}"
    return "PLUM ecoNET300"  # Main controller device


def get_via_device(category: str, param_type: str) -> str:
    """Determine via device (parent device)."""
    if param_type in ("service", "advanced"):
        return "PLUM ecoNET300"
    if any(x in category.lower() for x in ["mixer", "lambda", "ecoster"]):
        return "PLUM ecoNET300"
    return "-"


def main() -> None:
    """Main entry point for generating fixture entities report."""
    fixtures_root = Path("tests/fixtures/ecoMAX810P-L")
    structure_file = fixtures_root / "rmStructure.json"
    cats_file = fixtures_root / "rmCatsNames.json"
    merged_data_file = fixtures_root / "mergedData.json"

    structure = json.loads(structure_file.read_text(encoding="utf-8"))
    cats = json.loads(cats_file.read_text(encoding="utf-8"))["data"]

    # Load merged parameter data if available
    params_complete: dict = {}
    if merged_data_file.exists():
        merged_data = json.loads(merged_data_file.read_text(encoding="utf-8"))
        params_complete = merged_data.get("parameters", {})

    # Map param index -> category names using rmStructure:
    # type 7 = category (index -> cats array), type 1 = parameter
    # Parameters can appear in multiple categories (collects all)
    param_to_cats: dict[int, list[str]] = {}
    current_cat: int | None = None

    for entry in structure["data"]:
        if not isinstance(entry, dict):
            continue

        entry_type = entry.get("type")
        entry_index = entry.get("index")

        if entry_type == 7 and isinstance(entry_index, int) and entry_index < len(cats):
            current_cat = entry_index
        elif (
            entry_type == 1 and isinstance(entry_index, int) and current_cat is not None
        ):
            category_name = cats[current_cat]
            # Collect all categories for this parameter
            if entry_index not in param_to_cats:
                param_to_cats[entry_index] = []
            # Avoid duplicates
            if category_name not in param_to_cats[entry_index]:
                param_to_cats[entry_index].append(category_name)

    rows: list[tuple[str, str, str, str, str, str, str]] = []

    # Process each parameter with its categories
    for param_id, categories in sorted(param_to_cats.items(), key=lambda x: x[0]):
        # Get parameter data from mergedData.json
        param_data = params_complete.get(str(param_id), {})
        name = param_data.get("name", f"Parameter {param_id}")
        base_entity_key = param_data.get("key", f"param_{param_id}")
        unit = param_data.get("unit_name", "-")
        is_editable = param_data.get("edit", True)

        # Process each category for this parameter
        for category in categories:
            param_type = get_parameter_type(category)
            device_name = get_device_name(category, param_type)
            via_device = get_via_device(category, param_type)

            # Determine entity type based on category and editability
            if is_information_category(category):
                # Information categories always create sensors (read-only)
                entity_type = "sensor (Information)"
                entity_key = f"info_{base_entity_key}"
            elif param_type in ("service", "advanced"):
                # Service/advanced categories create numbers (if editable)
                entity_type = (
                    f"number ({param_type})" if is_editable else "sensor (read-only)"
                )
                entity_key = f"{param_type}_{base_entity_key}"
            else:
                # Basic categories create numbers (if editable)
                entity_type = "number (basic)" if is_editable else "sensor (read-only)"
                entity_key = f"basic_{base_entity_key}"

            rows.append(
                (device_name, via_device, name, entity_key, entity_type, category, unit)
            )

    # Group rows by device
    rows_by_device: dict[str, list[tuple]] = {}
    for row in rows:
        device = row[0]
        if device not in rows_by_device:
            rows_by_device[device] = []
        rows_by_device[device].append(row)

    # Setup output file
    output_dir = Path("tests/test_reports")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "fixture_entities_report.md"

    # Write to file
    with output_file.open("w", encoding="utf-8") as f:
        # Write header
        f.write("# Fixture Entities Report\n\n")
        f.write(
            "Generated from ecoMAX810P-L test fixtures showing how dynamic parameters would be organized as Home Assistant entities.\n\n"
        )
        f.write("---\n\n")

        # Print summary first
        f.write("## Summary\n\n")
        f.write(f"**Total entities: {len(rows)}**\n")
        f.write(f"**Total unique parameters: {len(param_to_cats)}**\n\n")

        # Count by device
        device_counts: dict[str, int] = {}
        for row in rows:
            device = row[0]
            device_counts[device] = device_counts.get(device, 0) + 1

        f.write("**Entities by device:**\n")
        for device, count in sorted(device_counts.items(), key=lambda x: -x[1]):
            f.write(f"- {device}: {count}\n")
        f.write("\n")

        # Count by category
        category_counts: dict[str, int] = {}
        for row in rows:
            cat = row[5]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        f.write("**Entities by category:**\n")
        for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
            f.write(f"- {cat}: {count}\n")
        f.write("\n")

        # Count by entity type
        entity_type_counts: dict[str, int] = {}
        for row in rows:
            entity_type = row[4]
            entity_type_counts[entity_type] = entity_type_counts.get(entity_type, 0) + 1

        f.write("**Entities by type:**\n")
        for entity_type, count in sorted(
            entity_type_counts.items(), key=lambda x: -x[1]
        ):
            f.write(f"- {entity_type}: {count}\n")
        f.write("\n")

        # Print tables grouped by device
        for device_name in sorted(rows_by_device.keys()):
            device_rows = rows_by_device[device_name]
            device_count = len(device_rows)

            f.write(f"## {device_name} ({device_count} entities)\n\n")

            f.write("```markdown\n")
            f.write("| Entity name | Entity key | Type | Category | Unit |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            for (
                _device,
                _via_device,
                entity_name,
                entity_key,
                entity_type,
                category,
                unit,
            ) in sorted(device_rows, key=lambda x: x[2]):
                f.write(
                    f"| {entity_name} | `{entity_key}` | {entity_type} | {category} | {unit} |\n"
                )
            f.write("```\n\n")

        # List all entity names
        f.write("## All Entity Names (copy-paste ready)\n\n")
        f.write("```python\n")
        entity_names = [row[2] for row in rows]  # Entity name is index 2
        for name in sorted(entity_names):
            f.write(f'"{name}",\n')
        f.write("```\n\n")

        # List all entity keys
        f.write("## All Entity Keys (copy-paste ready)\n\n")
        f.write("```python\n")
        entity_keys = [row[3] for row in rows]  # Entity key is index 3
        f.writelines(f'"{key}",\n' for key in sorted(entity_keys))
        f.write("```\n")

    # Console output
    print("[SUCCESS] Report generated successfully!")
    print(f"[OUTPUT] File written to: {output_file}")
    print(f"[STATS] Total entities: {len(rows)} across {len(rows_by_device)} devices")


if __name__ == "__main__":
    main()
