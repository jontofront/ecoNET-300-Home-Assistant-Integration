# ecoSOL Device Discovery Summary

## Overview
This document summarizes the ecoSOL-related information discovered from the ecoNET24 cloud JavaScript files (`dev_set1.js` through `dev_set5.js` and translation files).

## ecoSOL Device Types Identified

### Supported ecoSOL Models
- **ecoSOL 300** - Basic solar thermal system
- **ecoSOL 301** - Advanced solar thermal system (with specific client IDs: 118, 226-235, 237-242)
- **ecoSOL 400** - Solar thermal system with disinfection capabilities
- **ecoSOL 500** - High-capacity solar thermal system

### Device Schema Prefixes
```javascript
var ECOSOL_SCHEMA_PREFIX = 'ecoSOL300_';
var ECOSOL_400500_SCHEMA_PREFIX = 'ecoSOL400_';
```

## ecoSOL-Specific Parameters and Features

### Temperature Sensors
- **T1** - Collector temperature sensor
- **T2** - Storage tank temperature sensor  
- **T3** - Storage tank temperature sensor
- **T4** - Return temperature sensor
- **T6** - Additional temperature sensor (when flow meter is present)

### Pump Controls
- **P1** - Primary pump status
- **P2** - Secondary pump status
- **Cyrkulacja_ecoSol400** - Circulation pump operational during disinfection

### Flow Monitoring
- **przep_ywomierz** - Flow meter presence indicator
- **Przep_yw_pkt_A** - Flow point A
- **Przep_yw_pkt_B** - Flow point B
- **Przep_min_V** - Minimum flow V
- **Przep_maks_V** - Maximum flow V

### Special ecoSOL 400 Features
- **Disinfection mode** with circulation pump control
- **Presostat alarm controls**:
  - `T_tr_alarmu_p` - Presostat alarm time duration
  - `T_prz_alarmu_p` - Presostat alarm pause duration time

## ecoSOL Alarm System

### Complete Alarm List (16 alarms)
| Alarm | English | Polish | German | Czech | Spanish | Russian | Turkish | Latvian | Ukrainian |
|-------|---------|---------|---------|---------|---------|---------|---------|---------|-----------|
| **EcosolAlarm0** | DHW overheat | Przegrzanie zasobnika CWU | BW-Behälter überhitzt | Přehřátí zásobníku TUV | Sobrecalentamiento del depósito ACS | Перегрев бойлера ГВС | Boyler aşırı ısınma | KŪ tvertnes pārkaršana | Перегрів бойлера ГВП |
| **EcosolAlarm1** | Solar panel overheat | Przegrzanie panelu solarnego | Solarmodul überhitzt | Přehřátí solárního paneli | Sobrecalentamiento del panel solar | Перегрев солнечного коллектора | Güneş enerji paneli aşırı ısınma | Saules kolektoru pārkaršana | Перегрівання сонячного колектора |
| **EcosolAlarm2** | Solar panel critical temp. exceed | Temp. krytyczna na panelu solarnym | Kritische Temp. am Solarmodul | Kritická teplota na solárním kolektoru | Temp. crítica para el panel solar | Критическая темп. на солнечном коллекторе | Güneş enerji paneli kritik sıcaklık aşıldı | Temp. kritiska attiecībā uz saules kolektoru | Критичний темп. на сонячному колекторі |
| **EcosolAlarm3** | T1 sensor malfunction | Uszkodzenie czujnika T1 | Beschädigung vom T1-Sensor | Poškození čidla T1 | Daño en el sensor T1 | Неисправность датчика T1 | T1 sensör hatası | T1 sensora darbības traucējumi | Несправність датчика T1 |
| **EcosolAlarm4** | T2 sensor malfunction | Uszkodzenie czujnika T2 | Beschädigung vom T2-Sensor | Poškození čidla T2 | Daño en el sensor T2 | Неисправность датчика T2 | T2 sensör hatası | T2 sensora darbības traucējumi | Несправність датчика T2 |
| **EcosolAlarm5** | T3 sensor malfunction | Uszkodzenie czujnika T3 | Beschädigung vom T3-Sensor | Poškození čidla T3 | Daño en el sensor T3 | Неисправность датчика T3 | T3 sensör hatası | T3 sensora darbības traucējumi | Несправність датчика T3 |
| **EcosolAlarm6** | T4 sensor malfunction | Uszkodzenie czujnika T4 | Beschädigung vom T4-Sensor | Poškození čidla T4 | Daño en el sensor T4 | Неисправность датчика T4 | T4 sensör hatası | T4 sensora darbības traucējumi | Несправність датчика T4 |
| **EcosolAlarm7** | DHW A overheat | Przegrzanie zasobnika CWU A | BW-Behälter A überhitzt | Přehřátí zásobníku TUV A | Sobrecalentamiento del depósito A | Перегрев бойлера ГВС A | Boyler A aşırı ısınma | KŪ Tvertnes pārkaršana A | Перегрів бойлера ГВП A |
| **EcosolAlarm8** | DHW B overheat | Przegrzanie zasobnika CWU B | BW-Behälter B überhitzt | Přehřátí zásobníku TUV B | Sobrecalentamiento del depósito B | Перегрев бойлера ГВС B | Boyler B aşırı ısınma | KŪ Tvertnes pārkaršana B | Перегрів бойлера ГВП B |
| **EcosolAlarm9** | Solar panel A critical temp. exceed | Temp. krytyczna na panelu solarnym A | Kritische Temp. am Solarmodul A | Kritická teplota na solárním kolektoru A | Temp. crítica panel A | Критическая темп. на солнечном коллекторе A | Güneş enerji paneli A kritik sıcaklık aşıldı | Saules A kolektora Kritiskā temperatūra Pārsniega | Критичний темп. на сонячному колекторі A |
| **EcosolAlarm10** | Solar panel B critical temp. exceed | Temp. krytyczna na panelu solarnym B | Kritische Temp. am Solarmodul B | Kritická teplota na solárním kolektoru B | Temp. crítica panel B | Критическая температура солнечного коллектора B | Güneş enerji paneli B kritik sıcaklık aşıldı | Saules B kolektora Kritiskā temperatūra Pārsniega | Критична температура сонячного колектора B |
| **EcosolAlarm11** | Solar panel A overheat | Przegrzanie panelu solarnego A | Solarmodul überhitzt A | Přehřátí solárního paneli A | Sobrecalentamiento panel A | Перегрев солнечного коллектора A | Güneş enerji paneli A aşırı ısınma | Saules kolektora pārkaršana A | Перегрівання сонячного колектора A |
| **EcosolAlarm12** | Solar panel B overheat | Przegrzanie panelu solarnego B | Solarmodul überhitzt B | Přehřátí solárního paneli B | Sobrecalentamiento panel B | Перегрев солнечного коллектора B | Güneş enerji paneli B aşırı ısınma | Saules kolektora pārkaršana B | Перегрівання сонячного колектора B |
| **EcosolAlarm13** | Antifreeze STOP | Antyzamarzanie STOP | Antifrieren Stop | Antifreeze STOP | Anticongelante STOP | Анти змерзание СТОП | Antifriz DURDURULDU | Pretsasalšana STOP | Анти замерзання СТОП |
| **EcosolAlarm14** | Presostat alarm | Presostat alarm | Presostat alarm | Presostat alarm | Presostato alarma | Прессостат тревога | Presostat alarmı | Trauksmes spiediena slēdzis | Пресостат тривога |
| **EcosolAlarm15** | Anoda alarm | Anoda alarm | Anoda alarm | Anoda alarm | Anodo alarma | Анод тревога | Anot alarmı | Anoda trauksme | Анод тривога |

## ecoSOL Scheduling System

### Schedule Modes
```javascript
var scheduleEcosolModes = ["working_days", "saturday", "sunday"];
```

### Schedule Parameters
- **CWU** - DHW schedules (English: "DHW schedules", Polish: "Obniżenia nocne od CWU")
- **CWUC** - Circulation pump schedules (English: "Circulation pump schedules", Polish: "Harmonogramy pompy cyrkulacji")

## ecoSOL Chart and Monitoring

### Power Parameters
- **totalGain** - Total heat gain (English: "Total heat gain", Polish: "Całkowity uzysk ciepła")
- **UM1** - Power monitoring parameter for charts

### Chart Options
- **chartEcoSolUnit** - Chart time unit (default: "days")
- **chartEcoSolOptions** - Chart configuration for ecoSOL systems

## ecoSOL-Specific Functions

### Alarm Display
```javascript
function showEcoSolAlarms(alarms) {
    // Displays ecoSOL-specific alarm table
    // Handles 16 different alarm types with translations
}
```

### Schema File Naming
```javascript
function getEcoSolPrefix(contrId) {
    if (contrId.indexOf("400") != -1 || contrId.indexOf("500") != -1 || 
        (contrId.indexOf("301") && [118,226,227,228,229,230,231,232,233,234,235,237,238,239,240,241,242].includes(clientId))) {
        return ECOSOL_400500_SCHEMA_PREFIX;
    } else {
        return ECOSOL_SCHEMA_PREFIX;
    }
}
```

## Protocol Support

### GM3 Protocol
- ecoSOL devices support GM3 protocol
- Special handling for ecoSOL 400 with GM3 protocol
- Flow meter integration when available

## Integration Notes

### Home Assistant Considerations
1. **Binary Sensors**: All 16 ecoSOL alarms can be implemented as binary sensors
2. **Sensors**: Temperature sensors T1-T4, flow parameters, power monitoring
3. **Switches**: Pump controls P1, P2, circulation pump
4. **Numbers**: Presostat timing parameters, flow thresholds
5. **Translations**: Full multi-language support for all ecoSOL parameters

### Missing Information
- Specific parameter IDs/addresses for Home Assistant integration
- Real-time data structure format
- Historical data access methods
- Device configuration parameters

## Source Files
- `dev_set1.js` - Controller and basic device management
- `dev_set2.js` - Schema and device type handling
- `dev_set3.js` - Parameter management and charts
- `dev_set4.js` - Alarm system and scheduling
- `dev_set5.js` - Device-specific fixes and updates
- `econet_transp*.js` - Multi-language translations

## Next Steps
1. Extract specific parameter mappings from the JavaScript files
2. Identify Home Assistant entity types for each ecoSOL feature
3. Create translation files following the established pattern
4. Implement ecoSOL-specific device detection
5. Add ecoSOL alarm handling to the integration
