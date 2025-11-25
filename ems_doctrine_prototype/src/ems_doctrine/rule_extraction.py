"""
Rule extraction engine for identifying obligations, permissions, and prohibitions
from EMS doctrine text using deontic logic patterns.
"""

import re
import logging
from enum import Enum
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
import spacy
from spacy.matcher import Matcher

from .config import config


class DeonticType(Enum):
    """Types of deontic modalities."""
    OBLIGATION = "obligation"     # must, shall, will, required
    PERMISSION = "permission"     # may, can, allowed, authorized
    PROHIBITION = "prohibition"   # must not, shall not, prohibited, forbidden


@dataclass
class Rule:
    """Represents a rule extracted from doctrine text."""
    id: str
    rule_type: DeonticType
    subject: str
    action: str
    object: str
    condition: str
    text: str
    confidence: float
    source_document: str
    section: str
    context: str


@dataclass
class RuleConflict:
    """Represents a conflict between two rules."""
    rule1_id: str
    rule2_id: str
    conflict_type: str
    description: str
    confidence: float


class RuleExtractor:
    """Extracts rules from EMS doctrine text."""

    def __init__(self):
        """Initialize the rule extractor."""
        self.logger = logging.getLogger(__name__)

        # Load spaCy model
        try:
            self.nlp = spacy.load(config.spacy_model)
        except OSError:
            self.nlp = spacy.load("en_core_web_sm")

        # Initialize matcher
        self.matcher = Matcher(self.nlp.vocab)

        # Load deontic keywords from config
        self.deontic_keywords = config.deontic_keywords

        # Set up rule patterns
        self._setup_rule_patterns()

        # Rule storage
        self.rules: List[Rule] = []
        self.rule_counter = 0

    def _setup_rule_patterns(self):
        """Set up spaCy patterns for rule extraction."""

        # Obligation patterns (must, shall, will, required)
        obligation_patterns = [
            # "X must Y"
            [{"LEMMA": {"IN": ["must", "shall", "will"]}}, {"POS": "VERB"}],
            # "X is required to Y"
            [{"LEMMA": "be"}, {"LEMMA": "require"}, {"LEMMA": "to"}, {"POS": "VERB"}],
            # "X shall ensure Y"
            [{"LEMMA": "shall"}, {"LEMMA": "ensure"}],
        ]

        # Permission patterns (may, can, allowed, authorized)
        permission_patterns = [
            # "X may Y"
            [{"LEMMA": {"IN": ["may", "can"]}}, {"POS": "VERB"}],
            # "X is authorized to Y"
            [{"LEMMA": "be"}, {"LEMMA": {"IN": ["authorize", "allow"]}}, {"LEMMA": "to"}, {"POS": "VERB"}],
            # "X has permission to Y"
            [{"LEMMA": "have"}, {"LEMMA": "permission"}, {"LEMMA": "to"}, {"POS": "VERB"}],
        ]

        # Prohibition patterns (must not, shall not, prohibited, forbidden)
        prohibition_patterns = [
            # "X must not Y" or "X shall not Y"
            [{"LEMMA": {"IN": ["must", "shall"]}}, {"LEMMA": "not"}, {"POS": "VERB"}],
            # "X is prohibited from Y"
            [{"LEMMA": "be"}, {"LEMMA": {"IN": ["prohibit", "forbid"]}}, {"LEMMA": "from"}, {"POS": "VERB"}],
            # "X cannot Y"
            [{"LEMMA": "can"}, {"LEMMA": "not"}, {"POS": "VERB"}],
        ]

        # Add patterns to matcher
        self.matcher.add("OBLIGATION", obligation_patterns)
        self.matcher.add("PERMISSION", permission_patterns)
        self.matcher.add("PROHIBITION", prohibition_patterns)

    def extract_rules(self, text: str, document_name: str = "", section: str = "") -> List[Rule]:
        """
        Extract rules from text.

        Args:
            text: Input text to analyze
            document_name: Source document name
            section: Document section

        Returns:
            List of extracted rules
        """
        extracted_rules = []
        doc = self.nlp(text)

        # Split text into sentences for better rule extraction
        sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]

        for sentence in sentences:
            sentence_doc = self.nlp(sentence)
            rules = self._extract_rules_from_sentence(sentence_doc, document_name, section)
            extracted_rules.extend(rules)

        # Post-process rules to improve quality
        extracted_rules = self._post_process_rules(extracted_rules)

        self.logger.info(f"Extracted {len(extracted_rules)} rules from text")
        return extracted_rules

    def _extract_rules_from_sentence(self, doc, document_name: str, section: str) -> List[Rule]:
        """Extract rules from a single sentence."""
        rules = []
        sentence_text = doc.text

        # Use pattern matching to identify deontic expressions
        matches = self.matcher(doc)

        for match_id, start, end in matches:
            pattern_label = self.nlp.vocab.strings[match_id]
            deontic_span = doc[start:end]

            # Determine rule type
            if pattern_label == "OBLIGATION":
                rule_type = DeonticType.OBLIGATION
            elif pattern_label == "PERMISSION":
                rule_type = DeonticType.PERMISSION
            elif pattern_label == "PROHIBITION":
                rule_type = DeonticType.PROHIBITION
            else:
                continue

            # Extract rule components
            rule_components = self._extract_rule_components(doc, start, end)

            if rule_components:
                self.rule_counter += 1
                rule_id = f"rule_{self.rule_counter:04d}"

                rule = Rule(
                    id=rule_id,
                    rule_type=rule_type,
                    subject=rule_components.get('subject', ''),
                    action=rule_components.get('action', ''),
                    object=rule_components.get('object', ''),
                    condition=rule_components.get('condition', ''),
                    text=sentence_text,
                    confidence=self._calculate_rule_confidence(rule_components),
                    source_document=document_name,
                    section=section,
                    context=sentence_text
                )

                rules.append(rule)

        # Also try regex-based extraction for common patterns
        regex_rules = self._extract_rules_with_regex(sentence_text, document_name, section)
        rules.extend(regex_rules)

        return rules

    def _extract_rule_components(self, doc, deontic_start: int, deontic_end: int) -> Optional[Dict[str, str]]:
        """Extract subject, action, object, and condition from rule."""
        components = {}

        # Find the subject (usually before the deontic expression)
        subject_candidates = []
        for token in doc[max(0, deontic_start-10):deontic_start]:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                subject_candidates.append(token.text)

        if subject_candidates:
            components['subject'] = ' '.join(subject_candidates[-2:])  # Take last 1-2 nouns
        else:
            components['subject'] = "entity"  # Default subject

        # Find the action (verb after deontic expression)
        action_candidates = []
        for token in doc[deontic_end:min(len(doc), deontic_end+5)]:
            if token.pos_ == "VERB":
                action_candidates.append(token.lemma_)
                break

        if action_candidates:
            components['action'] = action_candidates[0]
        else:
            # Look for action words in the entire sentence
            for token in doc:
                if token.pos_ == "VERB" and token.lemma_ not in ["be", "have", "do"]:
                    components['action'] = token.lemma_
                    break

        # Find the object (what the action is performed on)
        object_candidates = []
        action_found = False
        for token in doc[deontic_end:]:
            if token.pos_ == "VERB":
                action_found = True
            elif action_found and token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                object_candidates.append(token.text)

        if object_candidates:
            components['object'] = ' '.join(object_candidates[:3])  # Take first few nouns

        # Look for conditions (if, when, unless, etc.)
        condition_keywords = ["if", "when", "unless", "provided", "except", "during"]
        condition_text = ""

        for i, token in enumerate(doc):
            if token.lemma_.lower() in condition_keywords:
                # Extract condition from this point to end of sentence
                condition_tokens = [t.text for t in doc[i:]]
                condition_text = ' '.join(condition_tokens)
                break

        components['condition'] = condition_text

        return components if components.get('action') else None

    def _extract_rules_with_regex(self, text: str, document_name: str, section: str) -> List[Rule]:
        """Extract rules using regex patterns."""
        rules = []

        # Common military rule patterns
        patterns = [
            # "Commanders must ensure..."
            (r'(\w+(?:\s+\w+)*)\s+(must|shall|will)\s+(ensure|verify|confirm)\s+(.+)', DeonticType.OBLIGATION),

            # "Personnel may not..."
            (r'(\w+(?:\s+\w+)*)\s+(may\s+not|cannot|shall\s+not)\s+(.+)', DeonticType.PROHIBITION),

            # "Units are authorized to..."
            (r'(\w+(?:\s+\w+)*)\s+(?:are|is)\s+(authorized|permitted|allowed)\s+to\s+(.+)', DeonticType.PERMISSION),

            # "It is prohibited to..."
            (r'[Ii]t\s+is\s+(prohibited|forbidden)\s+to\s+(.+)', DeonticType.PROHIBITION),

            # "Frequency X must be coordinated..."
            (r'([Ff]requency\s+\w+)\s+(must|shall)\s+be\s+(.+)', DeonticType.OBLIGATION),

            # "EMS operations require..."
            (r'(EMS\s+operations?|Electronic\s+warfare)\s+(require|need)\s+(.+)', DeonticType.OBLIGATION),
        ]

        for pattern, rule_type in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                groups = match.groups()

                if len(groups) >= 2:
                    self.rule_counter += 1
                    rule_id = f"rule_regex_{self.rule_counter:04d}"

                    # Extract components based on pattern structure
                    if rule_type == DeonticType.PROHIBITION and "prohibited" in match.group(0):
                        subject = "entity"
                        action = groups[-1] if len(groups) >= 1 else ""
                        object_text = ""
                    else:
                        subject = groups[0] if len(groups) >= 1 else "entity"
                        action = groups[-1] if len(groups) >= 2 else ""
                        object_text = ""

                    rule = Rule(
                        id=rule_id,
                        rule_type=rule_type,
                        subject=subject.strip(),
                        action=action.strip(),
                        object=object_text.strip(),
                        condition="",
                        text=match.group(0),
                        confidence=0.7,  # Lower confidence for regex extraction
                        source_document=document_name,
                        section=section,
                        context=text
                    )

                    rules.append(rule)

        return rules

    def _calculate_rule_confidence(self, components: Dict[str, str]) -> float:
        """Calculate confidence score for an extracted rule."""
        confidence = 0.5  # Base confidence

        # Increase confidence for clear subjects
        if components.get('subject') and len(components['subject']) > 1:
            confidence += 0.2

        # Increase confidence for clear actions
        if components.get('action') and len(components['action']) > 2:
            confidence += 0.2

        # Increase confidence for clear objects
        if components.get('object') and len(components['object']) > 1:
            confidence += 0.1

        return min(confidence, 1.0)

    def _post_process_rules(self, rules: List[Rule]) -> List[Rule]:
        """Post-process rules to improve quality."""
        # Remove duplicate rules
        unique_rules = []
        seen_texts = set()

        for rule in rules:
            rule_signature = f"{rule.rule_type.value}_{rule.text.lower().strip()}"
            if rule_signature not in seen_texts:
                seen_texts.add(rule_signature)
                unique_rules.append(rule)

        # Filter out low-confidence rules
        filtered_rules = [rule for rule in unique_rules if rule.confidence >= 0.3]

        self.logger.info(f"Post-processing: {len(rules)} -> {len(filtered_rules)} rules")
        return filtered_rules

    def detect_conflicts(self, rules: List[Rule]) -> List[RuleConflict]:
        """
        Detect conflicts between rules.

        Args:
            rules: List of rules to analyze

        Returns:
            List of detected conflicts
        """
        conflicts = []

        for i, rule1 in enumerate(rules):
            for j, rule2 in enumerate(rules[i+1:], i+1):
                conflict = self._check_rule_conflict(rule1, rule2)
                if conflict:
                    conflicts.append(conflict)

        self.logger.info(f"Detected {len(conflicts)} rule conflicts")
        return conflicts

    def _check_rule_conflict(self, rule1: Rule, rule2: Rule) -> Optional[RuleConflict]:
        """Check if two rules conflict."""
        # Direct contradiction: obligation vs prohibition
        if (rule1.rule_type == DeonticType.OBLIGATION and
            rule2.rule_type == DeonticType.PROHIBITION):

            # Check if they involve similar actions/subjects
            similarity = self._calculate_rule_similarity(rule1, rule2)
            if similarity > 0.5:
                return RuleConflict(
                    rule1_id=rule1.id,
                    rule2_id=rule2.id,
                    conflict_type="OBLIGATION_PROHIBITION",
                    description=f"Rule {rule1.id} requires action while rule {rule2.id} prohibits it",
                    confidence=similarity
                )

        # Permission vs prohibition
        if (rule1.rule_type == DeonticType.PERMISSION and
            rule2.rule_type == DeonticType.PROHIBITION):

            similarity = self._calculate_rule_similarity(rule1, rule2)
            if similarity > 0.6:
                return RuleConflict(
                    rule1_id=rule1.id,
                    rule2_id=rule2.id,
                    conflict_type="PERMISSION_PROHIBITION",
                    description=f"Rule {rule1.id} permits action while rule {rule2.id} prohibits it",
                    confidence=similarity
                )

        return None

    def _calculate_rule_similarity(self, rule1: Rule, rule2: Rule) -> float:
        """Calculate similarity between two rules."""
        similarity = 0.0

        # Compare subjects
        if rule1.subject.lower() == rule2.subject.lower():
            similarity += 0.3
        elif rule1.subject.lower() in rule2.subject.lower() or rule2.subject.lower() in rule1.subject.lower():
            similarity += 0.2

        # Compare actions
        if rule1.action.lower() == rule2.action.lower():
            similarity += 0.4
        elif rule1.action.lower() in rule2.action.lower() or rule2.action.lower() in rule1.action.lower():
            similarity += 0.2

        # Compare objects
        if rule1.object.lower() == rule2.object.lower():
            similarity += 0.3
        elif rule1.object.lower() in rule2.object.lower() or rule2.object.lower() in rule1.object.lower():
            similarity += 0.1

        return similarity

    def get_rules_by_type(self, rule_type: DeonticType) -> List[Rule]:
        """Get rules filtered by type."""
        return [rule for rule in self.rules if rule.rule_type == rule_type]

    def get_rules_by_subject(self, subject: str) -> List[Rule]:
        """Get rules filtered by subject."""
        return [rule for rule in self.rules if subject.lower() in rule.subject.lower()]

    def export_rules_to_json(self, file_path: str):
        """Export rules to JSON format."""
        import json
        from dataclasses import asdict

        rules_data = []
        for rule in self.rules:
            rule_dict = asdict(rule)
            rule_dict['rule_type'] = rule.rule_type.value
            rules_data.append(rule_dict)

        with open(file_path, 'w') as f:
            json.dump(rules_data, f, indent=2)

        self.logger.info(f"Exported {len(self.rules)} rules to {file_path}")

    def get_statistics(self) -> Dict[str, any]:
        """Get statistics about extracted rules."""
        stats = {
            'total_rules': len(self.rules),
            'obligations': len(self.get_rules_by_type(DeonticType.OBLIGATION)),
            'permissions': len(self.get_rules_by_type(DeonticType.PERMISSION)),
            'prohibitions': len(self.get_rules_by_type(DeonticType.PROHIBITION)),
            'average_confidence': sum(rule.confidence for rule in self.rules) / len(self.rules) if self.rules else 0,
            'documents_processed': len(set(rule.source_document for rule in self.rules))
        }

        return stats