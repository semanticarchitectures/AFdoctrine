"""
EMS Doctrine Prototype

A Phase 0 prototype for digitizing Air Force electromagnetic spectrum operations doctrine.
"""

__version__ = "0.1.0"
__author__ = "AF Doctrine Digitization Team"

from .config import Config
from .document_processing import DocumentProcessor
from .entity_recognition import EMSEntityRecognizer
from .knowledge_graph import KnowledgeGraph
from .rule_extraction import RuleExtractor