"""Schedule (ecomaxSchedules) name/key maps and weekday ordering."""

# =============================================================================
# SCHEDULE CONSTANTS (ecoMAX "em" protocol)
# =============================================================================
# User-friendly name -> API key mapping for ecomaxSchedules
SCHEDULE_TYPE_MAP: dict[str, str] = {
    "boiler": "boilerTZ",
    "boiler_clean": "boilerCleanTZ",
    "boiler_work": "boilerWorkTZ",
    "circulation_pump": "circPumpTZ",
    "exchanger_clean": "exchangerCleanTZ",
    "mixer_1": "mixer1TZ",
    "mixer_2": "mixer2TZ",
    "mixer_3": "mixer3TZ",
    "mixer_4": "mixer4TZ",
    "mixer_5": "mixer5TZ",
    "mixer_6": "mixer6TZ",
    "mixer_7": "mixer7TZ",
    "mixer_8": "mixer8TZ",
    "mixer_9": "mixer9TZ",
    "mixer_10": "mixer10TZ",
    "thermostat_1": "thermostat1TZ",
    "thermostat_2": "thermostat2TZ",
    "thermostat_3": "thermostat3TZ",
    "water_heater": "cwuTZ",
    "water_heater_2": "cwu2TZ",
}

# Reverse map: API key -> user-friendly name
SCHEDULE_TYPE_REVERSE_MAP: dict[str, str] = {v: k for k, v in SCHEDULE_TYPE_MAP.items()}

# Day ordering matches the ecoNET web interface (index 0 = Sunday)
SCHEDULE_WEEKDAYS: list[str] = [
    "sunday",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
]

