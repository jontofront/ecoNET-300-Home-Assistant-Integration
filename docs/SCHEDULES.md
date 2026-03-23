# Heating Schedules

> **Since v1.2.3** — View your boiler's configured schedules directly in Home Assistant.

The integration automatically reads all heating schedules from your ecoMAX controller
and creates a sensor for each one. No configuration needed — just restart Home Assistant
after updating and the sensors appear.

---

## What You Get Automatically

After restarting Home Assistant, you will see new sensors in your device page.
The exact sensors depend on which schedules your boiler has configured.

**Common schedule sensors:**

| Sensor Name | What It Shows |
| --- | --- |
| Boiler schedule | When the boiler is active |
| Water heater schedule | Hot water heating times |
| Boiler work schedule | Boiler operating hours |
| Circulation pump schedule | Pump running times |
| Mixer 1 schedule | Mixer circuit 1 schedule |
| Thermostat 1 schedule | Thermostat 1 schedule |

Each sensor shows **today's active hours** as the state, for example:

- `06:00-08:00, 16:00-22:00` — active in the morning and evening
- `all_on` — active 24 hours
- `all_off` — not active today

---

## How to Find Your Schedule Sensors

1. Open **Home Assistant**
2. Go to **Settings** > **Devices & Services**
3. Click on **ecoNET300**
4. Click on your device (e.g. "ecoNET300 Controller")
5. Scroll down — you will see sensors named **"Boiler schedule"**, **"Water heater schedule"**, etc.
6. Click on any sensor to see its details and attributes

---

## How to Display Schedules on Your Dashboard

The best way to show a weekly schedule is with a **Markdown card**. Here's how:

### Step 1: Open Your Dashboard

1. Go to your Home Assistant dashboard
2. Click the **three dots** (top right) > **Edit Dashboard**
3. Click **+ Add Card**
4. Search for **"Markdown"** and select it

### Step 2: Paste This Code

Copy and paste this into the Markdown card editor:

```yaml
type: markdown
title: Boiler Schedule
content: |
  | Day | Active Hours |
  |-----|-------------|
  | **Sun** | {{ state_attr('sensor.econet300_schedule_boiler', 'sunday') }} |
  | **Mon** | {{ state_attr('sensor.econet300_schedule_boiler', 'monday') }} |
  | **Tue** | {{ state_attr('sensor.econet300_schedule_boiler', 'tuesday') }} |
  | **Wed** | {{ state_attr('sensor.econet300_schedule_boiler', 'wednesday') }} |
  | **Thu** | {{ state_attr('sensor.econet300_schedule_boiler', 'thursday') }} |
  | **Fri** | {{ state_attr('sensor.econet300_schedule_boiler', 'friday') }} |
  | **Sat** | {{ state_attr('sensor.econet300_schedule_boiler', 'saturday') }} |
```

### Step 3: Save

Click **Save** and you will see a table like this:

| Day | Active Hours |
| --- | --- |
| **Sun** | 06:00-08:00, 16:00-22:00 |
| **Mon** | 06:00-08:00, 16:00-22:00 |
| **Tue** | 06:00-08:00, 16:00-22:00 |
| **Wed** | 06:00-08:00, 16:00-22:00 |
| **Thu** | 06:00-08:00, 16:00-22:00 |
| **Fri** | 06:00-22:00 |
| **Sat** | 08:00-22:00 |

---

## Multiple Schedules on One Card

If you want to show several schedules together, use this template:

```yaml
type: markdown
title: All Schedules
content: |
  ## Boiler
  {% set s = 'sensor.econet300_schedule_boiler' %}
  | Day | Hours |
  |-----|-------|
  | Mon | {{ state_attr(s, 'monday') }} |
  | Tue | {{ state_attr(s, 'tuesday') }} |
  | Wed | {{ state_attr(s, 'wednesday') }} |
  | Thu | {{ state_attr(s, 'thursday') }} |
  | Fri | {{ state_attr(s, 'friday') }} |
  | Sat | {{ state_attr(s, 'saturday') }} |
  | Sun | {{ state_attr(s, 'sunday') }} |

  ## Water Heater
  {% set s = 'sensor.econet300_schedule_water_heater' %}
  | Day | Hours |
  |-----|-------|
  | Mon | {{ state_attr(s, 'monday') }} |
  | Tue | {{ state_attr(s, 'tuesday') }} |
  | Wed | {{ state_attr(s, 'wednesday') }} |
  | Thu | {{ state_attr(s, 'thursday') }} |
  | Fri | {{ state_attr(s, 'friday') }} |
  | Sat | {{ state_attr(s, 'saturday') }} |
  | Sun | {{ state_attr(s, 'sunday') }} |
```

---

## Finding Your Sensor Entity ID

If the Markdown card shows "None" or "unknown", the sensor name might be different
on your system. Here's how to find the correct name:

1. Go to **Settings** > **Devices & Services** > **ecoNET300**
2. Click your device
3. Find the schedule sensor (e.g. "Boiler schedule")
4. Click on it
5. Click the **gear icon** (top right)
6. Copy the **Entity ID** — it looks like `sensor.econet300_schedule_boiler`
7. Use that exact name in your Markdown card

---

## Sensor Attributes

Each schedule sensor has these attributes you can use in cards and automations:

| Attribute | Example | Description |
| --- | --- | --- |
| `sunday` | `06:00-22:00` | Sunday's active hours |
| `monday` | `06:00-08:00, 16:00-22:00` | Monday's active hours |
| `tuesday` | `all_on` | Tuesday (active 24h) |
| `wednesday` | `all_off` | Wednesday (not active) |
| `thursday` | `06:00-22:00` | Thursday's active hours |
| `friday` | `06:00-22:00` | Friday's active hours |
| `saturday` | `08:00-22:00` | Saturday's active hours |
| `metadata` | `{on_off_mode: 0, ...}` | Schedule configuration |

---

## Using the Schedule Service (Advanced)

You can also call the `econet300.get_schedule` service to get detailed schedule data
(48 half-hour slots per day). This is useful for automations or advanced displays.

1. Go to **Developer Tools** > **Services**
2. Select **ecoNET300: Get schedule**
3. Choose a **Schedule type** (e.g. "boiler")
4. Optionally pick a **Weekday**
5. Click **Call Service**

The response contains the full slot-by-slot schedule with `start`, `end`, and `active`
for each 30-minute time slot.

---

## Troubleshooting

### I don't see any schedule sensors

- Make sure you are running **v1.2.3** or newer (check in Settings > Devices > ecoNET300)
- Your controller must have schedules configured — not all controllers support schedules
- Restart Home Assistant after updating the integration

### The card shows "None" for all days

- Check that the **Entity ID** in the card matches your actual sensor
- Go to Developer Tools > States, search for "schedule" to find the correct entity names
- Make sure the integration has loaded — check the ecoNET300 device page for schedule sensors

### I only see some schedule types

- The integration only creates sensors for schedules that exist on your device
- If your boiler only has boiler + water heater schedules configured, you will only see those two

### Values show "all_off" everywhere

- This means the schedule exists but all time slots are disabled on the boiler
- Check your boiler's control panel to verify the schedule configuration

---

## Supported Schedule Types

| Schedule Type | Description |
| --- | --- |
| Boiler | Main boiler heating schedule |
| Boiler cleaning | Boiler self-cleaning schedule |
| Boiler work | Boiler operating schedule |
| Circulation pump | Hot water circulation pump |
| Exchanger cleaning | Heat exchanger cleaning |
| Mixer 1–10 | Mixer circuit schedules |
| Thermostat 1–3 | Room thermostat schedules |
| Water heater | Domestic hot water schedule |
| Water heater 2 | Second water heater schedule |

---

## Languages

Schedule sensor names are translated into 5 languages:

- English
- Polish (Polski)
- French (Français)
- Ukrainian (Українська)
- Czech (Čeština)

The language is set in your Home Assistant general settings (Settings > System > General > Language).
