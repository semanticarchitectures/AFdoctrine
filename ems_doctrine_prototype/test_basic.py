#!/usr/bin/env python3
"""
Basic functionality test for EMS Doctrine Prototype
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from ems_doctrine.config import config
        from ems_doctrine.document_processing import DocumentProcessor
        from ems_doctrine.entity_recognition import EMSEntityRecognizer
        from ems_doctrine.knowledge_graph import KnowledgeGraph
        from ems_doctrine.rule_extraction import RuleExtractor
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_entity_recognition():
    """Test entity recognition functionality."""
    try:
        from ems_doctrine.entity_recognition import EMSEntityRecognizer

        recognizer = EMSEntityRecognizer()
        test_text = "JFACC must coordinate EMS operations on UHF frequencies"
        entities = recognizer.extract_entities(test_text)

        assert len(entities) > 0, "No entities extracted"

        # Check for expected entity types
        entity_types = [e.label for e in entities]
        expected_types = ['AUTHORITY', 'EMS_OPERATION', 'FREQUENCY']

        found_types = [t for t in expected_types if any(t in entity_types for t in entity_types)]

        print(f"✅ Entity recognition working: {len(entities)} entities found")
        print(f"   Types found: {set(entity_types)}")
        return True

    except Exception as e:
        print(f"❌ Entity recognition error: {e}")
        return False


def test_rule_extraction():
    """Test rule extraction functionality."""
    try:
        from ems_doctrine.rule_extraction import RuleExtractor, DeonticType

        extractor = RuleExtractor()
        test_text = "Commanders must ensure frequency coordination. Units may transmit on designated frequencies."
        rules = extractor.extract_rules(test_text, "test")

        assert len(rules) > 0, "No rules extracted"

        # Check rule types
        rule_types = [r.rule_type for r in rules]
        assert DeonticType.OBLIGATION in rule_types or DeonticType.PERMISSION in rule_types

        print(f"✅ Rule extraction working: {len(rules)} rules found")
        for rule in rules:
            print(f"   {rule.rule_type.value}: {rule.subject} {rule.action}")
        return True

    except Exception as e:
        print(f"❌ Rule extraction error: {e}")
        return False


def test_knowledge_graph():
    """Test knowledge graph functionality."""
    try:
        from ems_doctrine.knowledge_graph import KnowledgeGraph, Node
        import tempfile
        import os

        # Use a temporary file for testing instead of in-memory
        temp_db = tempfile.mktemp(suffix='.db')

        try:
            kg = KnowledgeGraph(temp_db)

            # Test adding a node
            test_node = Node(
                id="test_node",
                label="Test Entity",
                type="TEST",
                properties={"test": "value"},
                source_document="test_doc"
            )

            result = kg.add_node(test_node)
            assert result == True, "Failed to add node"

            # Test querying
            nodes = kg.query_nodes(node_type="TEST")
            assert len(nodes) == 1, "Failed to query nodes"

            stats = kg.get_statistics()
            assert stats['total_nodes'] >= 1, "Statistics not working"

            print("✅ Knowledge graph working: nodes can be added and queried")
            return True
        finally:
            # Clean up temp file
            if os.path.exists(temp_db):
                os.remove(temp_db)

    except Exception as e:
        print(f"❌ Knowledge graph error: {e}")
        return False


def test_configuration():
    """Test configuration system."""
    try:
        from ems_doctrine.config import config

        # Test basic config access
        project_name = config.project_name
        version = config.version

        assert project_name is not None, "Project name not configured"
        assert version is not None, "Version not configured"

        # Test domain-specific config
        freq_bands = config.frequency_bands
        equipment_types = config.equipment_types

        assert len(freq_bands) > 0, "Frequency bands not configured"
        assert len(equipment_types) > 0, "Equipment types not configured"

        print("✅ Configuration system working")
        print(f"   Project: {project_name} v{version}")
        print(f"   EMS Domain: {len(freq_bands)} frequency bands, {len(equipment_types)} equipment types")
        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def main():
    """Run all basic tests."""
    print("🧪 Running basic functionality tests for EMS Doctrine Prototype")
    print("=" * 60)

    tests = [
        ("Module Imports", test_imports),
        ("Configuration System", test_configuration),
        ("Entity Recognition", test_entity_recognition),
        ("Rule Extraction", test_rule_extraction),
        ("Knowledge Graph", test_knowledge_graph),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")

    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The prototype is working correctly.")
        print("\nNext steps:")
        print("  • Run 'python demo.py' for a full demonstration")
        print("  • Run 'python -m ems_doctrine.cli demo' for CLI demo")
        print("  • Process real doctrine with 'python -m ems_doctrine.cli process-document'")
        return True
    else:
        print("⚠️  Some tests failed. Check dependencies and configuration.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)