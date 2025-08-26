# ecoNET Manual Translation Reference

## Overview
This file contains all available translation keys and their corresponding translations in English, Polish, and French extracted from the ecoNET cloud JavaScript files. Use this as a reference when implementing new entities or features in Home Assistant.

## Translation Statistics
- **English (EN)**: 1105 parameters - Complete coverage
- **Polish (PL)**: 1101 parameters - Complete coverage
- **French (FR)**: 872 parameters - Partial coverage

## Usage Notes
- **Primary Languages**: Use English and Polish for complete coverage
- **French**: Available for most common parameters but not complete
- **Key Format**: Use `camel_to_snake` format for Home Assistant entities
- **Example**: `tempCO` → `temp_co` for entity names

---

## 🔧 System & Interface

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `savingSchedule` | Saving schedule | Trwa zapisywanie harmonogramu | - |
| `scheduleSaved` | Schedule saved | Harmonogram zapisany! | - |
| `copy` | Copy | Kopiuj | - |
| `Stop` | Stop | Postój | - |
| `save` | Save | Zapisz | Enregistrer |
| `apply` | Apply | Zastosuj | Appliquer |
| `refresh` | Refresh network list | Odśwież listę sieci | Actualiser la liste de réseau |
| `parameters` | Parameters | Parametry | Paramètres |
| `settings` | Settings | Ustawienia | Réglages |
| `status` | Status: | Status: | Statut: |
| `cancel` | Cancel | Anuluj | Annuler |
| `ok` | OK | OK | OK |
| `yes` | Yes | Tak | - |
| `no` | No | Nie | - |
| `on` | On | - | - |
| `off` | Off | - | - |
| `error` | Error! | Błąd! | Erreur! |
| `none` | None | Brak | Aucun |

## 🌐 Network & WiFi

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `wifi_info` | WiFi information | Informacje WiFi | - |
| `network_name` | Network name: | Nazwa sieci: | Nom du réseau: |
| `security_type` | Type of protection: | Typ zabezpieczeń: | Type de sécurité: |
| `quality` | Signal quality: | Jakość sygnału: | Puissance du signal: |
| `signal_strength` | Signal strength: | Siła sygnału: | - |
| `password` | Password | Hasło | Mot de passe: |
| `connect` | Connect | Połącz | Connecter |
| `connecting` | Connecting... | Trwa łączenie... | Connexion en cours... |
| `connection_error` | Connection error! | Błąd połączenia! | Erreur de connexion! |
| `disconnected` | Disconnected | Rozłączono | Déconnecté |
| `connected` | Connected | Połączono | Connecté |
| `network` | Network | Sieć | Réseau |

## 🔐 Authentication & Users

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `User1` | User 1 | Użytkownik 1 | - |
| `User2` | User 2 | Użytkownik 2 | - |
| `User3` | User 3 | Użytkownik 3 | - |
| `User4` | User 4 | Użytkownik 4 | - |
| `user` | User | Użytkownik | - |
| `login_title` | Log on to Your account | - | - |
| `login` | Login | - | - |
| `login_btn` | Login | - | - |
| `logout` | logout | - | - |
| `create_new_account` | Register | - | - |
| `forgot_passwd` | Forgot password | - | - |
| `first_name` | First name: | - | - |
| `last_name` | Last name: | - | - |
| `email` | E-mail: | - | - |
| `phone` | Phone: | - | - |
| `country` | Country: | - | - |
| `language` | Language of alarm notifications: | - | - |

## 🏠 Address & Location

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `address` | Address: | Adres: | Adresse: |
| `street` | Street: | - | - |
| `house` | House no: | - | - |
| `apartment` | Apartment (optional): | - | - |
| `city` | City: | - | - |
| `postal_code` | Postal code: | - | - |
| `house_apartment` | House / apartment: | - | - |
| `postal_code_city` | Postal code / city: | - | - |

## 🚨 Alarms & Notifications

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `alarm` | Alarm | - | - |
| `alarmContinues` | Alarm continues | - | - |
| `alarmsHeader` | Alarms | - | - |
| `alarm_notifications` | Alarm notifications: | - | - |
| `alarm_notifications_label` | Permit alarm notifications via e-mail. | - | - |

## 🔧 Device Management

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `devices` | Devices | - | - |
| `device_uid` | Device UID: | - | - |
| `device_settings` | Device settings | - | - |
| `add_new_device` | Add new device | - | - |
| `remove_selected_device` | Remove selected device | - | - |
| `device_added` | Device has been added | - | - |
| `device_deleted` | The device has been successfully deleted. | - | - |
| `type` | Type: | Typ: | Type: |
| `id` | ID: | Identyfikator: | id: |
| `label` | Label: | - | - |
| `name` | Name: | - | - |

## 🌡️ Temperature Sensors

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `tempCO` | - | - | Température chaudière |
| `tempCWU` | - | - | Température ECS |
| `tempOpticalSensor` | - | - | Visibilité flamme |
| `tempFeeder` | - | - | Température du dispositif d'alimentation |
| `tempFlueGas` | - | - | Température des fumées |
| `tempExternalSensor` | - | - | Température extérieure |
| `tempBack` | - | - | Température de retour |
| `tempUpperBuffer` | - | - | Température haute du ballon tampon |
| `tempLowerBuffer` | - | - | Température basse du ballon tampon |
| `tempUpperSolar` | - | - | Température panneaux solaire |
| `tempLowerSolar` | - | - | Température ballon solaire |
| `tempFireplace` | - | - | Température de l'énergie d'appoint |
| `boiler_temp` | Enter new value of boiler temperature setting: | Ustaw nową wartość temperatury zadanej kotła: | Définir la nouvelle température de consigne chaudière: |
| `water_temp` | Enter new value of HUW temperature setting: | Ustaw nową wartość temperatury zadanej CWU: | Définir la nouvelle température de consigne ECS: |

## 🔥 Boiler & Heating

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `boiler` | Boiler | Kocioł | Chaudière |
| `boilerPower` | - | - | Puissance chaudière |
| `mode` | - | - | Marche / Arrêt chaudière |
| `totalGain` | - | - | Rendement thermique total |
| `lambdaLevel` | - | - | Sonde Lambda O2 |
| `fuelLevel` | - | - | Niveau de combustible |
| `fuelStream` | - | - | Débit de combustible |

## 💨 Fans & Ventilation

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `fanPower` | - | - | Puissance du ventilateur |
| `fanPowerExhaust` | - | - | Puissance de soufflage du ventilateur |

## ⚡ Power & Control

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `refresh_rate` | Refresh rate [s]: | Częstotliwość odświeżania [s]: | - |
| `refresh_period` | Refresh period [s]: | - | - |
| `set_refresh_period` | Set refresh period | - | - |

## 🏗️ System & Configuration

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `controller` | Controller: | Kontroler: | - |
| `em` | ecoMax | ecoMax | biocontrol |
| `gm3` | GazModem | GazModem | - |
| `gm3_pomp` | GazModem | GazModem | - |
| `application` | Application | Aplikacja | - |
| `panels_conf` | Panels configuration version | Wersja konfiguracji panelu | - |
| `software_version` | Module ecoNET version: | Wersja modułu ecoNET: | - |
| `software_version_short` | Soft ver.: | - | - |
| `module_version` | Module @module version: | Wersja modułu @module: | - |
| `module_not_connected` | module not connected | moduł nie jest podłączony | - |
| `server_version` | server version: | - | - |
| `db_version` | database version: | - | - |

## 📊 Data & History

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `data` | Current data | Dane bieżące | Données actuelles |
| `data_history` | Data history | - | - |
| `data_bounds_err` | The value should be within [@minVal, @maxVal]. | Wartość powinna zawierać się w przedziale [@minVal, @maxVal]. | La valeur doit être comprise dans la plage [@minVal, @maxVal]. |
| `int_expected_err` | The value should be an integer. | Wartość powinna być liczbą całkowitą. | La valeur doit être un nombre entier |
| `value_within_range` | The value should be within [1, | - | - |

## 🔄 Updates & Maintenance

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `new_soft_ver` | New software version available (@newVer) | Istnieje nowa wersja oprogramowania (@newVer) | - |
| `download` | Download | Pobierz | - |
| `downloadingFile` | Downloading new software @percent%. | Pobieranie nowej wersji oprogramowania @percent% | - |
| `updateSoftTile` | Software update | Aktualizacja oprogramowania | - |
| `update` | Update | Aktualizuj | - |
| `rebootWait` | ecoNET is being rebooted, please wait for @seconds seconds. | Następuje restart systemu ecoNET, ponowne uruchomienie za @seconds sekund. | - |

## 🌤️ Weather & Environment

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `weather_ctrl` | Weather control enabled. | Sterowanie pogodowe włączone. | - |
| `temp_set_editing_off` | Temperature editing is off. | Edycja temperatury zadanej jest wyłączona. | - |

## 🎛️ Advanced Settings

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `service` | Service | - | - |
| `producer` | Producer | - | - |
| `service_password_msg` | You cannot edit service parameters because you do not have the appropriate authorization, please provide service password in device settings. | - | - |
| `parameters_modification_not_allowed` | Modification of parameters is forbidden by user. | - | - |
| `advanced_user` | Advanced user: | - | - |
| `service_params_edit` | Service parameters edition | - | - |
| `advanced_user_pass` | Advanced user password: | - | - |
| `service_access` | Service access: | - | - |
| `service_access_label` | Permit remote access of to the controller. | - | - |

## 📱 User Interface

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `management` | Management | - | - |
| `about` | About | - | - |
| `other_name` | Different name... | Inna nazwa... | Autre nom... |
| `choose` | Select | Wybierz | Sélectionner |
| `other_settings` | Other settings | - | - |
| `images` | Images | - | - |
| `users` | Users | - | - |
| `schema` | Diagram | Schemat | Schéma |

## ⚠️ Error Messages

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `params_err` | Error while reading parameters! | Błąd odczytu parametrów! | Erreur de lecture des paramètres! |
| `save_error` | Error while saving data! | Błąd zapisu danych! | Erreur d'enregistrement des données! |
| `network_settings_error` | Network connection error, check the settings! | Błąd połączenia z siecią, sprawdź ustawienia! | Impossible de se connecter au réseau, vérifier les paramètres! |
| `wrong_password` | Wrong password! | Błędne hasło! | - |
| `empty_passwd` | Password cannot be empty. | Hasło nie może być puste. | - |
| `incorrect_passwd_psk2_err` | Password should contain 8 to 63 characters. | Hasło powinno zawierać od 8 do 63 znaków. | - |
| `incorrect_passwd_psk_err` | Password should contain 8 to 63 characters. | Hasło powinno zawierać od 8 do 63 znaków. | - |
| `incorrect_passwd_wep_err` | Password can contain exactly 5 or exactly 13 characters (letters or digits). | Hasło może zawierać wyłącznie 5 lub 13 znaków (liter lub cyfr). | - |
| `passwordTooShort` | New password must have more than 4 characters. | - | Le nouveau mot de passe doit contenir 4 caractères minimum. |
| `passwordTooLong` | New password must have less than 18 characters. | - | Le nouveau mot de passe doit contenir 18 caractères maximum. |
| `passwordDoNotMatch` | Password fields don't match | - | Password fields don't match |
| `fillAllFields` | Please fill in all fields. | - | Remplir tous les champs. |
| `fill_all_fields` | Fill in all required fields. | - | - |

## 🔒 Security & Access

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `title_password` | Password | Hasło | - |
| `enter_password` | Enter password for service parameters: | Wprowadź hasło dla parametrów serwisowych: | - |
| `enter_new_password` | enter new password | - | - |
| `change_advanced_pass` | Enter the password to access the service parameters in the controller: | - | - |
| `old_passwd` | Old password: | - | - |
| `new_passwd` | New password: | - | - |
| `verify_password` | Verify Password: | - | - |
| `input_password_again` | please enter your password again | - | - |
| `change_passwd` | Change password | - | - |

## 📋 Forms & Input

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `enter_new_value` | Enter a new value: | Podaj nową wartość: | - |
| `from` | From: | Od: | - |
| `to` | To: | Do: | - |
| `parameter` | Parameter: | Parametr: | - |
| `value_change` | Value change | Zmiana wartości | - |
| `choose_company` | Select manufacturing company. | - | - |

## 🏢 Business & Registration

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `client` | Client | - | - |
| `registration_reg_subtitle` | Fill the form to add a device | - | - |
| `registration_accepted_title` | Registration accepted | - | - |
| `account_activation_window` | Account activation | - | - |
| `account_activation_sub` | Confirmation message is being emailed to you. Check your email to finish registration. | - | - |
| `account_send_mail_again` | Click here | - | - |
| `account_activation` | Your account is not active. To send activation email again: | - | - |
| `accountActivationTitle` | Registration | - | - |
| `terms_of_service_button` | Regulations | - | - |
| `accept_policy` | *ACCEPTING THE REGULATIONS OF ECONET SYSTEM * I have read the ecoNET regulations and the https://www.econet24.com/ regulations and the Privacy Policy. I hereby state that I have understood those documents and agree to comply with them. | - | - |
| `term_of_service` | Terms of Service | - | - |
| `register` | Register | - | - |

## 🔄 Account Management

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `delete_account` | Delete account | Usuwanie konta | - |
| `delete_account_warning` | Are you sure you want to delete user account? | Czy na pewno chcesz usunąć konto użytkownika? | - |
| `deleting_account_impossible` | User account cannot be deleted. | Nie można usunąć konta | - |
| `logged_as` | logged in as | - | - |
| `not_logged_id` | not logged in | - | - |
| `change_user_addr` | Change of user address | - | - |
| `change_user_addr_error` | Error while changing user address. | - | - |

## 📱 Device Status & Messages

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `popup_not_active_dev` | You cannot change parameters of an inactive device! | Nie można zmieniać parametru nieaktywnego urządzenia! | - |
| `dev_owned` | Device cannot be added because it is owned by another user. | - | - |
| `dev_not_available` | No device in the system, make sure it is properly connected to the Internet. | - | - |
| `device_uid_empty_error` | Device UID cannot be empty | - | - |
| `device_deletion_error` | Error while deleting device. | - | - |
| `device_deletion_not_allowed` | Device deletion is not allowed. | - | - |
| `device_addition_not_allowed` | It is not allowed to add a device | - | - |

## 🌐 Server & Network Status

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `main_server` | Main server | Główny serwer | Serveur principal |
| `check_main_server` | Check server availability | Sprawdź dostępność serwera | Vérifiez le serveur |
| `server_available` | Server available | Serwer dostępny | Serveur disponible |
| `server_unavailable` | Server not available | Serwer niedostępny | Serveur indisponible |
| `range_exceeded` | Too large range | Zbyt duży zakres | limite dépassée |
| `maximum_range` | The maximum range of the data presented in the graph is 1 month | Maksymalny zakres danych prezentowanych na wykresie to 1 miesiąc | La période maximale d'affichage du graphe est d'1 mois |

## 📊 Data & Charts

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `data_bounds_err` | The value should be within [@minVal, @maxVal]. | Wartość powinna zawierać się w przedziale [@minVal, @maxVal]. | La valeur doit être comprise dans la plage [@minVal, @maxVal]. |
| `refresh_rate_out_err` | Refresh rate outside range, should be within [1, 100] | Częstotliwość odświeżania poza zakresem, powinna zawierać się w przedziale [1, 100] | - |

## 🔧 Advanced Parameters

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `regulator_uid` | Regulator UID: | - | - |
| `regulator_label` | Regulator label: | - | - |
| `regulator_installation_address` | Regulator installation address: | - | - |
| `regulator_adr_checkbox` | Same as user address | - | - |

## 📱 Navigation & UI

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `back` | Back | - | - |
| `back_to_main` | Back to main page | - | - |
| `apply_changes` | Apply changes | - | - |
| `changes_saved` | Changes saved. | Zmiany zapisane. | Modifications enregistrées |

## 🌍 Multi-language Support

| Key | English | Polish | French |
|-----|---------|---------|---------|
| `cookTitle` | - | - | Politique de cookies |

---

## 📝 Implementation Notes

### For Home Assistant Integration
1. **Use English and Polish** for complete coverage
2. **Convert keys** from camelCase to snake_case
3. **Update all three files**: strings.json, en.json, pl.json
4. **Test translations** after implementation

### Key Conversion Examples
- `tempCO` → `temp_co`
- `lambdaLevel` → `lambda_level`
- `fanPower` → `fan_power`
- `boilerPower` → `boiler_power`

### File Update Order
1. `custom_components/econet300/strings.json`
2. `custom_components/econet300/translations/en.json`
3. `custom_components/econet300/translations/pl.json`

---

*Last updated: 2025*
*Source: ecoNET cloud JavaScript files*
*Total parameters: EN (1105), PL (1101), FR (872)*
