# Heating Schedules

> **Since v1.3.0** — Heating schedules are exposed as native Home Assistant
> **Calendar** entities. (In v1.2.3–v1.2.x they were text-based sensors; those
> have been replaced by calendars.)

The integration automatically reads all heating schedules from your ecoMAX
controller and creates a **calendar entity** for each one. No configuration
needed — just restart Home Assistant after updating and the calendars appear.

---

## What You Get Automatically

After restarting Home Assistant, you will see new calendar entities on your
device page. The exact calendars depend on which schedules your boiler has
configured.

**Common schedule calendars:**

| Calendar Name             | What It Shows                |
| ------------------------- | ---------------------------- |
| Boiler                    | When the boiler is active    |
| Water Heater              | Hot water heating times      |
| Boiler Work               | Boiler operating hours       |
| Circulation Pump          | Pump running times           |
| Mixer 1                   | Mixer circuit 1 schedule     |
| Thermostat 1              | Thermostat 1 schedule        |

Each calendar shows the configured weekly active periods as recurring events.
When a schedule is disabled on the device (`on_off_mode = 0`), its events are
prefixed with `[OFF]`.

---

## How to Find Your Schedule Calendars

1. Open **Home Assistant**
2. Go to **Settings** > **Devices & Services**
3. Click on **ecoNET300**
4. Click on your device (e.g. "ecoNET300 Controller")
5. Scroll down to the **Calendar** entities — you will see **"Boiler"**,
   **"Water Heater"**, etc.
6. Click on any calendar to see its events and attributes

---

## How to Display Schedules on Your Dashboard

Because schedules are now calendar entities, the easiest way to show them is the
built-in [Calendar card](https://www.home-assistant.io/dashboards/calendar/).

### Step 1: Open Your Dashboard

1. Go to your Home Assistant dashboard
2. Click the **three dots** (top right) > **Edit Dashboard**
3. Click **+ Add Card**
4. Search for **"Calendar"** and select it

### Step 2: Select Your Schedule Calendars

Pick the schedule calendars you want to display, or paste this YAML and adjust
the entity IDs to match yours:

```yaml
type: calendar
title: Heating Schedules
initial_view: dayGridMonth
entities:
  - calendar.econet300_boiler
  - calendar.econet300_water_heater
```

### Step 3: Save

Click **Save**. The card shows each active period as an event in day, week, or
month view.

---

## Finding Your Calendar Entity ID

If the card shows nothing, the entity ID might be different on your system.
Here's how to find the correct one:

1. Go to **Settings** > **Devices & Services** > **ecoNET300**
2. Click your device
3. Find the schedule calendar (e.g. "Boiler")
4. Click on it
5. Click the **gear icon** (top right)
6. Copy the **Entity ID** — it looks like `calendar.econet300_boiler`
7. Use that exact name in your Calendar card

---

## Calendar Attributes

Each schedule calendar exposes these attributes you can use in automations:

| Attribute          | Example                | Description                                  |
| ------------------ | ---------------------- | -------------------------------------------- |
| `schedule_enabled` | `true`                 | `false` when the schedule is disabled        |
| `metadata`         | `{on_off_mode: 1, ...}`| Raw schedule configuration from the device   |

To act on whether the boiler schedule is currently active, trigger on the
calendar entity state (`on` while an event is running, `off` otherwise):

```yaml
automation:
  - alias: "Notify when boiler schedule starts"
    triggers:
      - trigger: state
        entity_id: calendar.econet300_boiler
        to: "on"
    actions:
      - action: notify.mobile_app_your_phone
        data:
          message: "Boiler schedule active period started"
```

---

## Using the Schedule Service (Advanced)

You can also call the `econet300.get_schedule` service to get detailed schedule
data (48 half-hour slots per day). This is useful for automations or advanced
displays.

1. Go to **Developer Tools** > **Actions**
2. Select **ecoNET300: Get schedule**
3. Choose a **Schedule type** (e.g. "boiler")
4. Optionally pick a **Weekday**
5. Click **Perform action**

The response contains the full slot-by-slot schedule with `start`, `end`, and
`active` for each 30-minute time slot.

---

## Troubleshooting

### I don't see any schedule calendars

- Make sure you are running **v1.3.0** or newer (check in Settings > Devices > ecoNET300)
- Your controller must have schedules configured — not all controllers support schedules
- Restart Home Assistant after updating the integration

### The card is empty

- Check that the **Entity ID** in the card matches your actual calendar
- Go to Developer Tools > States, search for "calendar" to find the correct entity names
- Make sure the integration has loaded — check the ecoNET300 device page for calendar entities

### I only see some schedule types

- The integration only creates calendars for schedules that exist on your device
- If your boiler only has boiler + water heater schedules configured, you will only see those two

### Events are prefixed with `[OFF]`

- This means the schedule exists but is disabled on the boiler (`on_off_mode = 0`)
- Check your boiler's control panel to enable the schedule

---

## Supported Schedule Types

| Schedule Type     | Description                  |
| ----------------- | ---------------------------- |
| Boiler            | Main boiler heating schedule |
| Boiler clean      | Boiler self-cleaning schedule|
| Boiler work       | Boiler operating schedule    |
| Circulation pump  | Hot water circulation pump   |
| Exchanger clean   | Heat exchanger cleaning      |
| Mixer 1–10        | Mixer circuit schedules      |
| Thermostat 1–3    | Room thermostat schedules    |
| Water heater      | Domestic hot water schedule  |
| Water heater 2    | Second water heater schedule |

---

## Languages

Schedule calendar names are translated into 5 languages:

- English
- Polish (Polski)
- French (Français)
- Ukrainian (Українська)
- Czech (Čeština)

The language is set in your Home Assistant general settings (Settings > System > General > Language).
