"""
Entity recognition system for extracting EMS-specific entities from doctrine text.
"""

import re
import logging
from typing import List, Dict, Set, Tuple
import spacy
from spacy.matcher import Matcher
from spacy.lang.en import English
from dataclasses import dataclass

from .config import config


@dataclass
class Entity:
    """Represents a recognized entity."""
    text: str
    label: str
    start: int
    end: int
    confidence: float = 1.0
    context: str = ""


class EMSEntityRecognizer:
    """Recognizes EMS-specific entities in doctrine text."""

    def __init__(self):
        """Initialize the entity recognizer."""
        self.logger = logging.getLogger(__name__)

        # Load spaCy model
        try:
            self.nlp = spacy.load(config.spacy_model)
        except OSError:
            self.logger.warning(f"spaCy model {config.spacy_model} not found. Using basic English model.")
            self.nlp = English()

        # Initialize matcher
        self.matcher = Matcher(self.nlp.vocab)

        # Set up domain-specific patterns
        self._setup_ems_patterns()

        # Load domain knowledge
        self.frequency_bands = config.frequency_bands
        self.equipment_types = set(config.equipment_types)
        self.operation_types = set(config.operation_types)
        self.authorities = set(config.authorities)

    def _setup_ems_patterns(self):
        """Set up pattern matching for EMS entities."""

        # Frequency patterns
        frequency_patterns = [
            [{"TEXT": {"REGEX": r"\d+\.?\d*"}, "OP": "?"}, {"LOWER": {"IN": ["mhz", "ghz", "khz", "hz"]}}],
            [{"TEXT": {"REGEX": r"\d+\.?\d*"}}, {"TEXT": "-"}, {"TEXT": {"REGEX": r"\d+\.?\d*"}}, {"LOWER": {"IN": ["mhz", "ghz", "khz", "hz"]}}],
            [{"LOWER": {"IN": ["hf", "vhf", "uhf", "shf", "ehf"]}}],
        ]

        # Equipment patterns
        equipment_patterns = [
            [{"LOWER": {"IN": ["jammer", "jammers", "jamming"]}}, {"LOWER": "system", "OP": "?"}],
            [{"LOWER": {"IN": ["radar", "radars"]}}],
            [{"LOWER": {"IN": ["radio", "radios"]}}],
            [{"LOWER": {"IN": ["antenna", "antennas"]}}, {"LOWER": "system", "OP": "?"}],
            [{"LOWER": {"IN": ["transmitter", "transmitters"]}}],
            [{"LOWER": {"IN": ["receiver", "receivers"]}}],
        ]

        # Operation patterns
        operation_patterns = [
            [{"LOWER": "electronic"}, {"LOWER": {"IN": ["attack", "warfare", "protection"]}}],
            [{"LOWER": "spectrum"}, {"LOWER": "management"}],
            [{"LOWER": "sead"}],  # Suppression of Enemy Air Defenses
            [{"LOWER": "electromagnetic"}, {"LOWER": "warfare"}],
        ]

        # Authority patterns
        authority_patterns = [
            [{"TEXT": {"IN": ["JFACC", "JFC", "JEMSO"]}}],
            [{"LOWER": "spectrum"}, {"LOWER": "manager"}],
            [{"LOWER": "electronic"}, {"LOWER": "warfare"}, {"LOWER": "officer"}],
            [{"TEXT": "EWO"}],
        ]

        # Add patterns to matcher
        self.matcher.add("FREQUENCY", frequency_patterns)
        self.matcher.add("EMS_EQUIPMENT", equipment_patterns)
        self.matcher.add("EMS_OPERATION", operation_patterns)
        self.matcher.add("AUTHORITY", authority_patterns)

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract EMS entities from text.

        Args:
            text: Input text to analyze

        Returns:
            List of recognized entities
        """
        entities = []

        # Process text with spaCy
        doc = self.nlp(text)

        # Extract entities using pattern matching
        matches = self.matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            label = self.nlp.vocab.strings[match_id]

            # Get context (surrounding words)
            context_start = max(0, start - 5)
            context_end = min(len(doc), end + 5)
            context = doc[context_start:context_end].text

            entity = Entity(
                text=span.text,
                label=label,
                start=span.start_char,
                end=span.end_char,
                context=context
            )
            entities.append(entity)

        # Extract specific frequency values
        freq_entities = self._extract_frequency_values(text)
        entities.extend(freq_entities)

        # Extract military units and roles
        military_entities = self._extract_military_entities(text)
        entities.extend(military_entities)

        # Remove duplicates and sort by position
        entities = self._deduplicate_entities(entities)
        entities.sort(key=lambda e: e.start)

        self.logger.info(f"Extracted {len(entities)} entities from text")
        return entities

    def _extract_frequency_values(self, text: str) -> List[Entity]:
        """Extract specific frequency values and ranges."""
        entities = []

        # Pattern for frequency values with units
        freq_pattern = r'(\d+(?:\.\d+)?)\s*(MHz|GHz|KHz|Hz|mhz|ghz|khz|hz)\b'

        for match in re.finditer(freq_pattern, text):
            start, end = match.span()
            frequency_text = match.group(0)

            entity = Entity(
                text=frequency_text,
                label="FREQUENCY",
                start=start,
                end=end,
                context=text[max(0, start-20):end+20]
            )
            entities.append(entity)

        # Pattern for frequency ranges
        range_pattern = r'(\d+(?:\.\d+)?)\s*[-–—]\s*(\d+(?:\.\d+)?)\s*(MHz|GHz|KHz|Hz|mhz|ghz|khz|hz)\b'

        for match in re.finditer(range_pattern, text):
            start, end = match.span()
            range_text = match.group(0)

            entity = Entity(
                text=range_text,
                label="FREQUENCY_RANGE",
                start=start,
                end=end,
                context=text[max(0, start-20):end+20]
            )
            entities.append(entity)

        return entities

    def _extract_military_entities(self, text: str) -> List[Entity]:
        """Extract military-specific entities and acronyms."""
        entities = []

        # Common military EMS acronyms and terms
        military_terms = {
            'EA': 'ELECTRONIC_ATTACK',
            'EP': 'ELECTRONIC_PROTECTION',
            'ES': 'ELECTRONIC_SUPPORT',
            'EW': 'ELECTRONIC_WARFARE',
            'SEAD': 'EMS_OPERATION',
            'DEAD': 'EMS_OPERATION',
            'ECM': 'EMS_EQUIPMENT',
            'ECCM': 'EMS_EQUIPMENT',
            'ESM': 'EMS_EQUIPMENT',
            'ELINT': 'EMS_OPERATION',
            'COMINT': 'EMS_OPERATION',
            'SIGINT': 'EMS_OPERATION'
        }

        # Pattern for military acronyms (2-6 uppercase letters)
        acronym_pattern = r'\b([A-Z]{2,6})\b'

        for match in re.finditer(acronym_pattern, text):
            acronym = match.group(1)
            if acronym in military_terms:
                start, end = match.span()

                entity = Entity(
                    text=acronym,
                    label=military_terms[acronym],
                    start=start,
                    end=end,
                    context=text[max(0, start-20):end+20]
                )
                entities.append(entity)

        return entities

    def _deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """Remove duplicate entities based on text span overlap."""
        if not entities:
            return entities

        # Sort by start position
        sorted_entities = sorted(entities, key=lambda e: e.start)

        deduplicated = []
        for entity in sorted_entities:
            # Check for overlap with existing entities
            overlap = False
            for existing in deduplicated:
                if (entity.start < existing.end and entity.end > existing.start):
                    # Overlapping entities - keep the longer one or the one with higher confidence
                    if (entity.end - entity.start) > (existing.end - existing.start):
                        deduplicated.remove(existing)
                        deduplicated.append(entity)
                    overlap = True
                    break

            if not overlap:
                deduplicated.append(entity)

        return deduplicated

    def get_entity_statistics(self, entities: List[Entity]) -> Dict[str, int]:
        """Get statistics about extracted entities."""
        stats = {}

        for entity in entities:
            label = entity.label
            if label in stats:
                stats[label] += 1
            else:
                stats[label] = 1

        return stats

    def extract_relationships(self, text: str, entities: List[Entity]) -> List[Dict]:
        """
        Extract relationships between entities.

        Args:
            text: Source text
            entities: List of entities

        Returns:
            List of relationship dictionaries
        """
        relationships = []
        doc = self.nlp(text)

        # Look for common relationship patterns
        relationship_patterns = [
            # "X operates on Y frequency"
            (r'(\w+)\s+operates?\s+on\s+(\d+(?:\.\d+)?\s*(?:MHz|GHz|KHz|Hz))', 'OPERATES_ON'),

            # "X jams Y"
            (r'(\w+)\s+jams?\s+(\w+)', 'JAMS'),

            # "X coordinates Y"
            (r'(\w+)\s+coordinates?\s+(\w+)', 'COORDINATES'),

            # "X controls Y"
            (r'(\w+)\s+controls?\s+(\w+)', 'CONTROLS'),
        ]

        for pattern, relation_type in relationship_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                subject = match.group(1)
                object_text = match.group(2)

                relationships.append({
                    'subject': subject,
                    'predicate': relation_type,
                    'object': object_text,
                    'confidence': 0.8,
                    'context': text[max(0, match.start()-30):match.end()+30]
                })

        return relationships