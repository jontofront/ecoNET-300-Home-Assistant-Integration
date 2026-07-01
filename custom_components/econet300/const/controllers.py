"""Device-specific sensor and binary-sensor key sets and their controller -> key-set mappings."""

from .core import COMPONENT_LAMBDA, SENSOR_FUEL_STREAM

# =============================================================================
# DEVICE-SPECIFIC SENSOR MAPPINGS
# =============================================================================
# ecoMAX360i specific sensors (regParams ``curr`` + common sysParams diagnostics)
ECOMAX360I_SENSORS = {
    "PS",
    "Circuit2thermostatTemp",
    "TempClutch",
    "Circuit3thermostatTemp",
    "Circuit4thermostatTemp",
    "Circuit5thermostatTemp",
    "Circuit6thermostatTemp",
    "Circuit7thermostatTemp",
    "TempWthr",
    "TempCircuit2",
    "TempCircuit3",
    "TempCircuit4",
    "TempCircuit5",
    "TempCircuit6",
    "TempCircuit7",
    "TempBuforUp",
    "TempCWU",
    "TempBuforDown",
    "heatingUpperTemp",
    "Circuit1thermostat",
    "heating_work_state_pump4",
    # 3-way valve and demand sensors
    "flapValveStates",
    "HeatDemanded",
    "WaterPumpRunning",
    # Heat pump (Axen) sensors
    "AxenOutdoorTemp",
    "AxenOutgoingTemp",
    "AxenReturnTemp",
    "AxenCompressorFreq",
    "AxenUpperPump",
    "AxenWorkState",
    "HeatSourceCalcPresetTemp",
    # Heat pump compressor temperatures
    "afterCompressorTemp",
    "beforeCompressorTemp",
    "exhaustGasTemp",
    "outdoorTemp",
    # Heat pump status sensors
    "HPStatusWorkMode",
    "HPStatusPresetTemp",
    "HPStatusControl",
    # SSA (weather compensation) sensors
    "ssaState",
    "ssaCorr",
    "ssaPrevTemp",
    # Circuit comfort/eco temperature setpoints (read-only from regParams)
    "Circuit1ComfortTemp",
    "Circuit1EcoTemp",
    "BufferTargetTemp",
    "Circuit2ComfortTemp",
    "Circuit2EcoTemp",
    "Circuit3ComfortTemp",
    "Circuit3EcoTemp",
    "Circuit4ComfortTemp",
    "Circuit4EcoTemp",
    "Circuit5ComfortTemp",
    "Circuit5EcoTemp",
    "Circuit6ComfortTemp",
    "Circuit6EcoTemp",
    "Circuit7ComfortTemp",
    "Circuit7EcoTemp",
    # Phoenix / extended heat-pump sensors (decomposed from sensor.py EXTRA_SENSORS)
    "BuforCalcSetTemp",
    "Circuit1CalcTemp",
    "Circuit2CalcTemp",
    "Circuit4CalcTemp",
    "Circuit5CalcTemp",
    "Circuit6CalcTemp",
    "Circuit7CalcTemp",
    "HDWsetpointcalculate",
    "CoolingPower",
    "HeatingPower",
    "ElectricPower",
    "currentFlow",
    "HPStatusBuffHeatStat",
    "HPStatusCircPStat0",
    "HPStatusCircPStat1",
    "HPStatusCircPStat2",
    "HPStatusCircPStat3",
    "HPStatusCircPStat4",
    "HPStatusCircPStat5",
    "HPStatusCircPStat6",
    "HPStatusFlowHeatStat",
    "HPStatusHdwHeatStat",
    "HPStatusUhsStat",
    "HP_work_state_set_pump2",
    "HP_work_state_set_pump3",
    "HP_work_state_set_pump4",
    "HP_work_state_set_pump5",
    "PHNXcoil_temp",
    "PHNXdischarge_temp",
    "PHNXinletTemp",
    "PHNXinletTemp_pump",
    "PHNXinletTemp_pump2",
    "PHNXinletTemp_pump3",
    "PHNXinletTemp_pump5",
    "PHNXoutletTemp",
    "PHNXoutletTemp_pump2",
    "PHNXoutletTemp_pump3",
    "PHNXoutletTemp_pump4",
    "PHNXoutletTemp_pump5",
    "PHNXreg2045",
    "PHNXreg2046",
    "PHNXreg2071",
    "PHNXreg2074",
    "PHNXsuctionTemp",
    # informationParams sensors (from editParams endpoint)
    "TargetFlowTemp",
    "ActualFlowTemp",
    "ActualReturnTemp",
    "FanSpeed",
    "HeatPumpAmbient",
    "ActualDHWTemp",
    "Circuit1DesiredLWT",
    "ElectricalPower",
    "ThermalPower",
    "COP",
    "SCOP",
    "FlowRate",
    # editParams.data sensors
    "AXENREGISTER64",
    "AXENREGISTER65",
    # sysParams diagnostics (same as DEFAULT_SENSORS subset)
    "controllerID",
    "moduleASoftVer",
    "moduleBSoftVer",
    "moduleCSoftVer",
    "moduleLambdaSoftVer",
    "modulePanelSoftVer",
    "moduleEcoSTERSoftVer",
    "protocolType",
    "quality",
    "routerType",
    "signal",
    "softVer",
}

# informationParams: sensor key -> parameter ID in editParams.informationParams
# These are read-only heat pump / status sensors for ecoMAX360i.
INFORMATION_PARAMS_SENSOR_MAP: dict[str, str] = {
    "TargetFlowTemp": "12",
    "ActualFlowTemp": "14",
    "ActualReturnTemp": "15",
    "FanSpeed": "22",
    "HeatPumpAmbient": "23",
    "HeatDemanded": "26",
    "ActualDHWTemp": "61",
    "Circuit1DesiredLWT": "93",
    "ElectricalPower": "211",
    "ThermalPower": "212",
    "COP": "221",
    "SCOP": "222",
    "FlowRate": "231",
}

# editParams.data: sensor key -> parameter ID in editParams["data"]
# These are read-only Axen register sensors for ecoMAX360i.
EDIT_PARAMS_DATA_SENSOR_MAP: dict[str, str] = {
    "AXENREGISTER64": "1211",
    "AXENREGISTER65": "1212",
}

# ecoSTER thermostat sensors (if moduleEcoSTERSoftVer is not None)
ECOSTER_SENSORS = {
    # ecoSTER temperature sensors
    "ecoSterTemp1",
    "ecoSterTemp2",
    "ecoSterTemp3",
    "ecoSterTemp4",
    "ecoSterTemp5",
    "ecoSterTemp6",
    "ecoSterTemp7",
    "ecoSterTemp8",
    # ecoSTER setpoint sensors
    "ecoSterSetTemp1",
    "ecoSterSetTemp2",
    "ecoSterSetTemp3",
    "ecoSterSetTemp4",
    "ecoSterSetTemp5",
    "ecoSterSetTemp6",
    "ecoSterSetTemp7",
    "ecoSterSetTemp8",
    # ecoSTER mode sensors
    "ecoSterMode1",
    "ecoSterMode2",
    "ecoSterMode3",
    "ecoSterMode4",
    "ecoSterMode5",
    "ecoSterMode6",
    "ecoSterMode7",
    "ecoSterMode8",
}

# Lambda sensor module
LAMBDA_SENSORS = {
    "lambdaStatus",
    "lambdaSet",
    "lambdaLevel",
}

# ecoSOL solar collector sensors (all ecoSOL [n] models with matching regParams)
ECOSOL_SENSORS = {
    # Temperature sensors
    "T1",  # Collector temperature
    "T2",  # Tank temperature
    "T3",  # Tank temperature
    "T4",  # Return temperature
    "T5",  # Collector temperature - power measurement
    "T6",  # Temperature sensor
    "TzCWU",  # Hot water temperature
    # Pump status sensors
    "P1",  # Pump 1 status
    "P2",  # Pump 2 status
    # Output status
    "H",  # Output status
    # Power / energy (regParams; ecoSOL 301 flat JSON uses subset)
    "Moc_chwilowa",  # Instantaneous solar collector power (kW)
    "Uzysk_ca_kowity",  # Cumulative solar heat yield (kWh)
    # Diagnostic sensors
    "ecosrvAddr",
    "quality",
    "signal",
    "softVer",
    "routerType",
    "protocolType",
    "controllerID",
    "ecosrvSoftVer",
}

# Reference-only dict key for SENSOR_MAP_KEY / BINARY_SENSOR_MAP_KEY (not a live controllerID)
ECOSOL_CONTROLLER_MAP_REFERENCE_KEY = "ecoSOL [n]"

# Default sensors for most controllers
DEFAULT_SENSORS = {
    "boilerPower",
    "boilerPowerKW",
    "tempFeeder",
    "fuelLevel",
    "tempCO",
    "tempCOSet",
    "statusCWU",
    "tempCWU",
    "tempCWUSet",
    "tempFlueGas",
    "mode",
    "fanPower",
    "thermostat",
    "tempExternalSensor",
    "tempLowerBuffer",
    "tempUpperBuffer",
    "quality",
    "signal",
    "softVer",
    "controllerID",
    "moduleASoftVer",
    "moduleBSoftVer",
    "moduleCSoftVer",
    "moduleLambdaSoftVer",
    "modulePanelSoftVer",
    "moduleEcoSTERSoftVer",
    # ecoMAX850R2-X specific sensors
    "fuelConsum",
    SENSOR_FUEL_STREAM,
    "tempBack",
    "transmission",
    "statusCO",
    # Diagnostic sensors
    "routerType",
    "protocolType",
}

# Main sensor mapping by controller type
# Sensor platform: is_ecosol_controller() → ECOSOL_SENSORS;
# is_ecomax360i_controller() → ECOMAX360I_SENSORS (see sensor.py); else DEFAULT_SENSORS.
# ecoSter / lambda entries remain reference-only for now.
SENSOR_MAP_KEY = {
    "ecoMAX360i": ECOMAX360I_SENSORS,  # Runtime via is_ecomax360i_controller()
    ECOSOL_CONTROLLER_MAP_REFERENCE_KEY: ECOSOL_SENSORS,  # Reference — runtime uses is_ecosol_controller()
    "ecoSter": ECOSTER_SENSORS,  # Reference only - not used
    COMPONENT_LAMBDA: LAMBDA_SENSORS,  # Reference only - not used
    "_default": DEFAULT_SENSORS,  # Default for non-ecoSOL controllers
}

# =============================================================================
# DEVICE-SPECIFIC BINARY SENSOR MAPPINGS
# =============================================================================
# Default binary sensors for most controllers
DEFAULT_BINARY_SENSORS = {
    "lighterWorks",
    "pumpCOWorks",
    "fanWorks",
    "feederWorks",
    "pumpFireplaceWorks",
    "pumpCWUWorks",
    "mainSrv",
    "wifi",
    "lan",
    "fuelConsumptionCalc",
    "ecosrvHttps",
    # ecoMAX850R2-X specific binary sensors
    "contactGZC",
    "contactGZCActive",
    "pumpCirculationWorks",
    "pumpSolarWorks",
    # Operational (running-now) outputs. The matching base keys (alarmOutput,
    # blowFan1, ...) mean "connected/present" and are filtered out of the plain
    # sensor sweep so they are not duplicated. See docs/ENTITIES.md.
    "alarmOutputWorks",
    "blowFan1Active",
    "blowFan2Active",
    "fan2ExhaustWorks",
    "feeder2AdditionalWorks",
    "feederOuterWorks",
    "outerBoilerWorks",
}

# ecoSTER thermostat binary sensors
ECOSTER_BINARY_SENSORS = {
    # ecoSTER contact sensors
    "ecoSterContacts1",
    "ecoSterContacts2",
    "ecoSterContacts3",
    "ecoSterContacts4",
    "ecoSterContacts5",
    "ecoSterContacts6",
    "ecoSterContacts7",
    "ecoSterContacts8",
    # ecoSTER day schedule sensors
    "ecoSterDaySched1",
    "ecoSterDaySched2",
    "ecoSterDaySched3",
    "ecoSterDaySched4",
    "ecoSterDaySched5",
    "ecoSterDaySched6",
    "ecoSterDaySched7",
    "ecoSterDaySched8",
}

# ecoSOL solar collector binary sensors (all ecoSOL [n] models)
ECOSOL_BINARY_SENSORS = {
    "wifi",
    "lan",
    "mainSrv",
    "fuelConsumptionCalc",
    "ecosrvHttps",
}

# Main binary sensor mapping by controller type
# All controllers use DEFAULT_BINARY_SENSORS (specific mappings are for reference only)
BINARY_SENSOR_MAP_KEY = {
    "_default": DEFAULT_BINARY_SENSORS,  # Always used for all controllers
    ECOSOL_CONTROLLER_MAP_REFERENCE_KEY: ECOSOL_BINARY_SENSORS,  # Reference — runtime uses is_ecosol_controller()
    "ecoSter": ECOSTER_BINARY_SENSORS,  # Reference only - not used
}
