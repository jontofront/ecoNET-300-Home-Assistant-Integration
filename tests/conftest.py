"""Test configuration for ecoNET300 integration tests."""

from pathlib import Path
import sys

# Add the project root to the Python path so tests can import custom_components
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
