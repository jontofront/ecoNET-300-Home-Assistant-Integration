"""Entity category mappings."""

from homeassistant.const import EntityCategory as _EntityCategory

ENTITY_CATEGORY = {
    "signal": _EntityCategory.DIAGNOSTIC,
    "quality": _EntityCategory.DIAGNOSTIC,
    "softVer": _EntityCategory.DIAGNOSTIC,
    "moduleASoftVer": _EntityCategory.DIAGNOSTIC,
    "moduleBSoftVer": _EntityCategory.DIAGNOSTIC,
    "modulePanelSoftVer": _EntityCategory.DIAGNOSTIC,
    "moduleLambdaSoftVer": _EntityCategory.DIAGNOSTIC,
    "protocolType": _EntityCategory.DIAGNOSTIC,
    "controllerID": _EntityCategory.DIAGNOSTIC,
    "moduleCSoftVer": _EntityCategory.DIAGNOSTIC,
    "mainSrv": _EntityCategory.DIAGNOSTIC,
    "wifi": _EntityCategory.DIAGNOSTIC,
    "lan": _EntityCategory.DIAGNOSTIC,
    "fuelConsumptionCalc": _EntityCategory.DIAGNOSTIC,
    "ecosrvHttps": _EntityCategory.DIAGNOSTIC,
    "ecosrvAddr": _EntityCategory.DIAGNOSTIC,
    "routerType": _EntityCategory.DIAGNOSTIC,
    "ecosrvSoftVer": _EntityCategory.DIAGNOSTIC,
    "moduleEcoSTERSoftVer": _EntityCategory.DIAGNOSTIC,
    # Device registration/config values from the all-sensors sweep. These are
    # internal metadata (not operational readings), so group them as diagnostics.
    "prodLogo": _EntityCategory.DIAGNOSTIC,
    "regAllowed": _EntityCategory.DIAGNOSTIC,
    "regImgID": _EntityCategory.DIAGNOSTIC,
    "regProd": _EntityCategory.DIAGNOSTIC,
    "regRefresh": _EntityCategory.DIAGNOSTIC,
    "regType": _EntityCategory.DIAGNOSTIC,
    "remoteMenu": _EntityCategory.DIAGNOSTIC,
}
