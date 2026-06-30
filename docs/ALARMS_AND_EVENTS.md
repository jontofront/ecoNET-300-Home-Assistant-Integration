# Alarms and Event Notifications

> **Since v1.2.3** — [GitHub Issue #71](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration/issues/71)

The integration monitors boiler alarms from the `sysParams.alarms` endpoint and
resolves numeric alarm codes to human-readable descriptions via `rmAlarmsNames`.

---

## Entities Overview

| Entity Key     | Platform      | Description                                  | Category   |
| -------------- | ------------- | -------------------------------------------- | ---------- |
| `last_alarm`   | Sensor        | Most recent alarm description                | Diagnostic |
| `alarm_count`  | Sensor        | Total number of alarms (recent 5 in attrs)   | Diagnostic |
| `alarm_active` | Binary Sensor | ON when any alarm is currently active        | Diagnostic |
| `boiler_alarm` | Event         | Fires events on alarm changes                | Diagnostic |

---

## Sensor: Last Alarm

Shows the description of the most recent alarm entry.

**State:** Human-readable alarm description (e.g. "Unsuccessful boiler firing-up attempt. Empty the ashtray.")

**Attributes:**

| Attribute      | Type    | Description                                        |
| -------------- | ------- | -------------------------------------------------- |
| `alarm_code`   | int     | Numeric alarm code from the device                 |
| `from_date`    | string  | Timestamp when the alarm started                   |
| `to_date`      | string  | Timestamp when alarm ended (`null` if still active) |
| `is_active`    | boolean | `true` when the alarm is currently ongoing         |
| `total_alarms` | int     | Total number of alarms in the device history       |

---

## Sensor: Alarm Count

Shows the total number of alarms stored on the device.

**State:** Integer count of all alarms.

**Attributes:**

| Attribute       | Type | Description                                          |
| --------------- | ---- | ---------------------------------------------------- |
| `recent_alarms` | list | Up to 5 most recent alarms with code, description, dates |

Each item in `recent_alarms` is a dictionary:

| Field         | Type    | Description                                         |
| ------------- | ------- | --------------------------------------------------- |
| `alarm_code`  | int     | Numeric alarm code from the device                  |
| `description` | string  | Human-readable alarm description                    |
| `from_date`   | string  | Timestamp when the alarm started                    |
| `to_date`     | string  | Timestamp when the alarm ended (`null` if active)   |
| `is_active`   | boolean | `true` when the alarm is currently ongoing          |
| `service`     | boolean | `true` when the alarm requires service intervention |

The sensor intentionally exposes only **structured data**. Following Home
Assistant guidelines, presentation (tables, formatting) is left to the
dashboard. See the Markdown card below to render a history list.

---

## Dashboard: Alarm History List

The recommended way to show a list/table of recent alarms is a
[Markdown card](https://www.home-assistant.io/dashboards/markdown/) that
renders the `recent_alarms` attribute with a Jinja template. This keeps the
integration clean while giving you full control over the layout.

```yaml
type: markdown
title: ecoNET alarms
content: >
  {% set alarms = state_attr('sensor.econet300_alarm_count', 'recent_alarms') %}
  {% if alarms %}
  | Time | Code | Alarm | Status |
  | --- | --- | --- | --- |
  {% for a in alarms -%}
  | {{ a.from_date }} | {{ a.alarm_code }} | {{ a.description }} | {{ 'Active' if a.is_active else 'Cleared' }} |
  {% endfor %}
  {% else %}
  No alarms
  {% endif %}
```

> Adjust `sensor.econet300_alarm_count` to match your entity ID.

---

## Binary Sensor: Alarm Active

ON when any alarm has `toDate == null` (still active / unresolved).

**Device class:** `problem`

**Attributes (when ON):**

| Attribute                  | Type   | Description                         |
| -------------------------- | ------ | ----------------------------------- |
| `active_alarm_code`        | int    | Numeric code of the active alarm    |
| `active_alarm_description` | string | Human-readable description          |
| `active_since`             | string | Start timestamp of the active alarm |

---

## Event Entity: Boiler Alarm

The `BoilerAlarmEvent` entity fires Home Assistant events when alarms change.
This enables **instant push notifications** without polling delays.

**Event types:**

| Event Type        | When                                       | Attributes                                         |
| ----------------- | ------------------------------------------ | -------------------------------------------------- |
| `alarm_triggered` | A new alarm appears in the alarm history   | `alarm_code`, `description`, `from_date`, `is_active` |
| `alarm_cleared`   | The previously active alarm is resolved    | *(none)*                                           |

**Detection logic:**

- On each coordinator update, the entity compares the current alarm list with
  the previous snapshot (count + latest `fromDate` + active status).
- The very first update after integration startup is used to seed the baseline —
  no false-positive events fire on restart.
- If both a new alarm and an alarm clearance happen in the same update cycle,
  `alarm_triggered` takes priority.

---

## Automation Examples

### 1. Push Notification on New Alarm

```yaml
automation:
  - alias: "Boiler alarm notification"
    triggers:
      - trigger: state
        entity_id: event.econet300_boiler_alarm
    conditions:
      - condition: template
        value_template: >
          {{ trigger.to_state.attributes.event_type == 'alarm_triggered' }}
    actions:
      - action: notify.mobile_app_your_phone
        data:
          title: "Boiler Alarm!"
          message: >
            {{ trigger.to_state.attributes.description }}
            (code {{ trigger.to_state.attributes.alarm_code }},
            since {{ trigger.to_state.attributes.from_date }})
          data:
            priority: high
            ttl: 0
```

### 2. Notification When Alarm Clears

```yaml
automation:
  - alias: "Boiler alarm cleared"
    triggers:
      - trigger: state
        entity_id: event.econet300_boiler_alarm
    conditions:
      - condition: template
        value_template: >
          {{ trigger.to_state.attributes.event_type == 'alarm_cleared' }}
    actions:
      - action: notify.mobile_app_your_phone
        data:
          title: "Boiler OK"
          message: "Active boiler alarm has been resolved"
```

### 3. Flash a Light When Alarm Is Active

```yaml
automation:
  - alias: "Flash light on active alarm"
    triggers:
      - trigger: state
        entity_id: binary_sensor.econet300_alarm_active
        to: "on"
    actions:
      - action: light.turn_on
        target:
          entity_id: light.warning_lamp
        data:
          flash: long
          color_name: red
```

### 4. Log All Alarms to Logbook

```yaml
automation:
  - alias: "Log boiler alarm to logbook"
    triggers:
      - trigger: state
        entity_id: event.econet300_boiler_alarm
    conditions:
      - condition: template
        value_template: >
          {{ trigger.to_state.attributes.event_type == 'alarm_triggered' }}
    actions:
      - action: logbook.log
        data:
          name: "Boiler"
          message: >
            Alarm {{ trigger.to_state.attributes.alarm_code }}:
            {{ trigger.to_state.attributes.description }}
          entity_id: event.econet300_boiler_alarm
```

### 5. Combine With Binary Sensor for Persistent Alert

```yaml
automation:
  - alias: "Persistent notification while alarm active"
    triggers:
      - trigger: state
        entity_id: binary_sensor.econet300_alarm_active
        to: "on"
    actions:
      - action: persistent_notification.create
        data:
          title: "Boiler Alarm Active"
          message: >
            Code: {{ state_attr('binary_sensor.econet300_alarm_active', 'active_alarm_code') }}
            — {{ state_attr('binary_sensor.econet300_alarm_active', 'active_alarm_description') }}
            (since {{ state_attr('binary_sensor.econet300_alarm_active', 'active_since') }})
          notification_id: "boiler_alarm_active"

  - alias: "Dismiss notification when alarm clears"
    triggers:
      - trigger: state
        entity_id: binary_sensor.econet300_alarm_active
        to: "off"
    actions:
      - action: persistent_notification.dismiss
        data:
          notification_id: "boiler_alarm_active"
```

---

## How Alarm Data Flows

```text
ecoNET module
    │
    ├── GET /econet/sysParams      → { alarms: [ {code, fromDate, toDate, service}, ... ] }
    └── GET /econet/rmAlarmsNames  → { "0": "Power outage", "1": "...", ... }
            │
            ▼
    EconetDataCoordinator (polls every 30s)
            │
            ├── LastAlarmSensor        → state = description of alarms[0]
            ├── AlarmCountSensor       → state = len(alarms)
            ├── AlarmActiveBinarySensor → is_on = any(toDate is None)
            └── BoilerAlarmEvent       → fires alarm_triggered / alarm_cleared
```

---

## Troubleshooting

| Symptom | Cause | Solution |
| ------- | ----- | -------- |
| No alarm entities appear | Device has no `alarms` key in sysParams | Older firmware may not expose alarms — check diagnostics |
| Event fires on every restart | Should not happen (initial state is seeded) | Check logs for `async_added_to_hass` errors |
| Alarm description shows "Alarm 42" | `rmAlarmsNames` endpoint unavailable | Check that the alarm names endpoint returns data |
| Binary sensor stuck ON | Active alarm not yet resolved on the device | Check device panel — clear the alarm there |
