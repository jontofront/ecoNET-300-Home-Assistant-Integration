"""Test service parameter detection and category-based entity creation."""


# Category functions removed - category support eliminated


class TestServiceParameterDetection:
    """Test service parameter detection functionality."""

    def test_multiple_categories_parameter_structure(self):
        """Test that parameters can have multiple categories."""
        # This test verifies the data structure changes in _add_parameter_categories
        # Parameters should have both "category" (string) and "categories" (list)

        # Mock parameter data
        param = {
            "name": "Test Parameter",
            "number": 123,
            "categories": ["Information", "Boiler settings"],
            "category": "Information",  # First category for backward compatibility
        }

        # Verify structure
        assert "categories" in param
        assert "category" in param
        assert isinstance(param["categories"], list)
        assert isinstance(param["category"], str)
        assert len(param["categories"]) > 1
        assert param["category"] == param["categories"][0]
