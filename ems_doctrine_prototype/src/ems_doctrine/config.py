"""
Configuration management for EMS Doctrine Prototype
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for the EMS Doctrine Prototype."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to configuration file. If None, uses default.
        """
        if config_path is None:
            # Get path relative to project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'nlp.spacy_model')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @property
    def project_name(self) -> str:
        """Get project name."""
        return self.get('project.name', 'EMS Doctrine Prototype')

    @property
    def version(self) -> str:
        """Get project version."""
        return self.get('project.version', '0.1.0')

    @property
    def spacy_model(self) -> str:
        """Get spaCy model name."""
        return self.get('nlp.spacy_model', 'en_core_web_sm')

    @property
    def database_path(self) -> str:
        """Get database path."""
        return self.get('knowledge_graph.database_path', 'data/processed/ems_knowledge.db')

    @property
    def frequency_bands(self) -> Dict[str, str]:
        """Get EMS frequency band definitions."""
        return self.get('ems_domain.frequency_bands', {})

    @property
    def equipment_types(self) -> list:
        """Get EMS equipment types."""
        return self.get('ems_domain.equipment_types', [])

    @property
    def operation_types(self) -> list:
        """Get EMS operation types."""
        return self.get('ems_domain.operation_types', [])

    @property
    def authorities(self) -> list:
        """Get EMS authorities."""
        return self.get('ems_domain.authorities', [])

    @property
    def deontic_keywords(self) -> Dict[str, list]:
        """Get deontic logic keywords."""
        return self.get('rule_extraction.deontic_keywords', {})


# Global configuration instance
config = Config()