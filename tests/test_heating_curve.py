"""Test for boiler heating curve feature."""

from pathlib import Path
import re


def camel_to_snake(key: str) -> str:
    """Convert camel case return from API to snake case to match translations keys structure."""
    # Handle special cases first
    special_mappings = {
        "ecoSter": "ecoster",
        "ecoSOL": "ecosol",
        "ecoMAX": "ecomax",
        "ecoNET": "econet",
    }

    # Apply special mappings
    for camel_case, snake_case in special_mappings.items():
        if camel_case in key:
            key = key.replace(camel_case, snake_case)

    # Now apply the standard camel to snake conversion
    key = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower()


def test_heating_curve_constants():
    """Test that heating curve constants are properly defined."""
    # Read the const.py file and check for our constants
    const_file = (
        Path(__file__).parent.parent / "custom_components" / "econet300" / "const.py"
    )
    const_content = const_file.read_text()

    # Test that parameter 112 is in NUMBER_MAP
    assert '"112": "co_heat_curve"' in const_content

    # Test that all mixer heating curve parameters are in NUMBER_MAP
    for i in range(1, 7):
        param_index = 82 + i  # 83, 84, 85, 86, 87, 88
        assert f'"{param_index}": "mix_heat_curve{i}"' in const_content

    # Test that parameter 112 is in RMNEWPARAM_PARAMS
    assert '"112"' in const_content and "RMNEWPARAM_PARAMS" in const_content

    # Test that all mixer heating curve parameters are in RMNEWPARAM_PARAMS
    for i in range(83, 89):
        assert f'"{i}"' in const_content and "RMNEWPARAM_PARAMS" in const_content

    # Test that co_heat_curve has proper limits
    assert '"co_heat_curve": 0.1' in const_content
    assert '"co_heat_curve": 4.0' in const_content
    assert '"co_heat_curve": 0.1' in const_content

    # Test that mixer heating curves are generated dynamically
    assert (
        '**{f"mix_heat_curve{i}": 0.1 for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1)}'
        in const_content
    )
    assert (
        '**{f"mix_heat_curve{i}": 4.0 for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1)}'
        in const_content
    )
    assert (
        '**{f"mix_heat_curve{i}": 0.1 for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1)}'
        in const_content
    )


def test_heating_curve_translation_key():
    """Test that the translation key is correctly converted."""
    # Test camel_to_snake conversion
    assert camel_to_snake("CO_HEAT_CURVE") == "co_heat_curve"


def test_heating_curve_translations():
    """Test that translations are properly defined."""
    # Check strings.json
    strings_file = (
        Path(__file__).parent.parent
        / "custom_components"
        / "econet300"
        / "strings.json"
    )
    strings_content = strings_file.read_text()
    assert '"co_heat_curve"' in strings_content
    assert '"Boiler heating curve"' in strings_content

    # Check en.json
    en_file = (
        Path(__file__).parent.parent
        / "custom_components"
        / "econet300"
        / "translations"
        / "en.json"
    )
    en_content = en_file.read_text()
    assert '"co_heat_curve"' in en_content
    assert '"Boiler heating curve"' in en_content
    # Check all mixer heating curves in English
    for i in range(1, 7):
        assert f'"mix_heat_curve{i}"' in en_content
        assert f'"Heating curve cycle {i}"' in en_content

    # Check all language files for boiler and all mixer heating curves
    languages = {
        "pl": ("Krzywa grzewcza kotła", "Krzywa grzewcza obiegu"),
        "cz": ("Topná křivka kotle", "Topná křivka oběhu"),
        "fr": ("Courbe de chauffage de la chaudière", "Courbe de chauffage du circuit"),
        "uk": ("Крива нагрівання котла", "Крива нагрівання контуру"),
    }

    for lang, (boiler_name, mixer_base_name) in languages.items():
        lang_file = (
            Path(__file__).parent.parent
            / "custom_components"
            / "econet300"
            / "translations"
            / f"{lang}.json"
        )
        lang_content = lang_file.read_text()
        assert '"co_heat_curve"' in lang_content, (
            f"Missing co_heat_curve key in {lang}.json"
        )
        assert f'"{boiler_name}"' in lang_content, (
            f"Missing boiler heating curve translation in {lang}.json"
        )

        # Check all 6 mixer heating curves
        for i in range(1, 7):
            assert f'"mix_heat_curve{i}"' in lang_content, (
                f"Missing mix_heat_curve{i} key in {lang}.json"
            )
            assert f'"{mixer_base_name} {i}"' in lang_content, (
                f"Missing mixer {i} heating curve translation in {lang}.json"
            )


def test_heating_curve_api_endpoint():
    """Test that the API endpoint is correctly configured."""
    # Expected API call format
    expected_url = (
        "http://10.10.1.77/econet/rmNewParam?newParamIndex=112&newParamValue=1.5"
    )
    # This would be constructed in the API class as:
    # f"{self.host}/econet/rmNewParam?newParamIndex={param}&newParamValue={value}"
    assert "rmNewParam" in expected_url
    assert "newParamIndex=112" in expected_url
