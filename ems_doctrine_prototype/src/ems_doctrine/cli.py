"""
Command-line interface for EMS Doctrine Prototype.
"""

import click
import logging
from pathlib import Path

from .config import config
from .document_processing import DocumentProcessor
from .entity_recognition import EMSEntityRecognizer
from .knowledge_graph import KnowledgeGraph
from .rule_extraction import RuleExtractor
from .api import app


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """EMS Doctrine Prototype CLI."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output directory for results')
def process_document(file_path, output):
    """Process a document and extract entities, rules, and relationships."""
    click.echo(f"Processing document: {file_path}")

    # Initialize components
    doc_processor = DocumentProcessor()
    entity_recognizer = EMSEntityRecognizer()
    kg = KnowledgeGraph()
    rule_extractor = RuleExtractor()

    # Process document
    document = doc_processor.process_file(file_path)
    click.echo(f"Document: {document.title}")
    click.echo(f"Sections: {len(document.sections)}")
    click.echo(f"Word count: {document.metadata.get('word_count', 0)}")

    # Extract entities
    entities = entity_recognizer.extract_entities(document.content)
    click.echo(f"Entities extracted: {len(entities)}")

    # Show entity statistics
    entity_stats = entity_recognizer.get_entity_statistics(entities)
    for entity_type, count in entity_stats.items():
        click.echo(f"  {entity_type}: {count}")

    # Extract rules
    rules = rule_extractor.extract_rules(document.content, document.filename)
    click.echo(f"Rules extracted: {len(rules)}")

    # Show rule statistics
    rule_stats = rule_extractor.get_statistics()
    click.echo(f"  Obligations: {rule_stats.get('obligations', 0)}")
    click.echo(f"  Permissions: {rule_stats.get('permissions', 0)}")
    click.echo(f"  Prohibitions: {rule_stats.get('prohibitions', 0)}")

    # Add to knowledge graph
    kg.add_entities_from_document(entities, document.filename)

    # Extract relationships
    relationships = entity_recognizer.extract_relationships(document.content, entities)
    kg.add_relationships_from_data(relationships, document.filename)
    click.echo(f"Relationships extracted: {len(relationships)}")

    # Detect conflicts
    conflicts = rule_extractor.detect_conflicts(rules)
    if conflicts:
        click.echo(f"⚠️  Rule conflicts detected: {len(conflicts)}")
        for conflict in conflicts[:3]:  # Show first 3 conflicts
            click.echo(f"  {conflict.conflict_type}: {conflict.description}")

    # Save results if output directory specified
    if output:
        output_dir = Path(output)
        output_dir.mkdir(exist_ok=True)

        # Export rules
        rules_file = output_dir / f"{document.filename}_rules.json"
        rule_extractor.export_rules_to_json(str(rules_file))
        click.echo(f"Rules exported to: {rules_file}")

        # Export knowledge graph
        kg_file = output_dir / f"{document.filename}_graph.graphml"
        kg.export_graphml(str(kg_file))
        click.echo(f"Knowledge graph exported to: {kg_file}")

    click.echo("✅ Processing complete!")


@cli.command()
@click.argument('text')
def extract_entities(text):
    """Extract entities from text."""
    entity_recognizer = EMSEntityRecognizer()
    entities = entity_recognizer.extract_entities(text)

    click.echo(f"Entities found in text: {len(entities)}")
    for entity in entities:
        click.echo(f"  {entity.label}: {entity.text} (confidence: {entity.confidence:.2f})")


@cli.command()
@click.argument('text')
def extract_rules(text):
    """Extract rules from text."""
    rule_extractor = RuleExtractor()
    rules = rule_extractor.extract_rules(text, "cli_input")

    click.echo(f"Rules found in text: {len(rules)}")
    for rule in rules:
        click.echo(f"  {rule.rule_type.value}: {rule.subject} {rule.action} {rule.object}")
        click.echo(f"    Text: {rule.text}")
        click.echo(f"    Confidence: {rule.confidence:.2f}")
        click.echo()


@cli.command()
@click.option('--host', default='localhost', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def serve(host, port, debug):
    """Start the API server."""
    click.echo(f"Starting EMS Doctrine Prototype API on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


@cli.command()
def demo():
    """Run a demonstration using sample doctrine."""
    click.echo("🚀 EMS Doctrine Prototype Demonstration")
    click.echo("=" * 50)

    # Sample text for demonstration
    sample_text = """
    Electronic warfare officers must coordinate all jamming operations with the spectrum manager.
    Units may not transmit on guard frequencies except in emergency situations.
    The JFACC is authorized to approve electronic attack missions against enemy radar systems.
    All UHF communications require prior coordination with the air operations center.
    Personnel are prohibited from using commercial cellular frequencies in contested environments.
    """

    click.echo("Sample text:")
    click.echo(sample_text)
    click.echo()

    # Extract entities
    click.echo("🔍 Extracting entities...")
    entity_recognizer = EMSEntityRecognizer()
    entities = entity_recognizer.extract_entities(sample_text)

    for entity in entities:
        click.echo(f"  {entity.label}: '{entity.text}'")
    click.echo()

    # Extract rules
    click.echo("📋 Extracting rules...")
    rule_extractor = RuleExtractor()
    rules = rule_extractor.extract_rules(sample_text, "demo")

    for rule in rules:
        click.echo(f"  {rule.rule_type.value.upper()}: {rule.text}")
    click.echo()

    # Detect conflicts
    click.echo("⚠️  Checking for conflicts...")
    conflicts = rule_extractor.detect_conflicts(rules)

    if conflicts:
        click.echo(f"Found {len(conflicts)} potential conflicts:")
        for conflict in conflicts:
            click.echo(f"  {conflict.conflict_type}: {conflict.description}")
    else:
        click.echo("No conflicts detected.")
    click.echo()

    # Knowledge graph
    click.echo("🕸️  Building knowledge graph...")
    kg = KnowledgeGraph()
    kg.add_entities_from_document(entities, "demo")

    stats = kg.get_statistics()
    click.echo(f"Knowledge graph: {stats['total_nodes']} nodes, {stats['total_edges']} edges")
    click.echo()

    click.echo("✅ Demonstration complete!")
    click.echo("Run 'ems-doctrine serve' to start the API server.")


@cli.command()
def init():
    """Initialize the EMS Doctrine Prototype environment."""
    click.echo("🔧 Initializing EMS Doctrine Prototype")

    # Create necessary directories
    data_dir = Path("data")
    (data_dir / "raw").mkdir(parents=True, exist_ok=True)
    (data_dir / "processed").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    # Initialize knowledge graph database
    kg = KnowledgeGraph()
    click.echo("✅ Knowledge graph database initialized")

    # Check if sample data exists
    sample_file = data_dir / "raw" / "sample_ems_doctrine.txt"
    if sample_file.exists():
        click.echo(f"📄 Sample doctrine file found: {sample_file}")
        click.echo("Run 'ems-doctrine process-document data/raw/sample_ems_doctrine.txt' to process it")
    else:
        click.echo("⚠️  No sample doctrine file found")

    click.echo("🎉 Initialization complete!")


if __name__ == '__main__':
    cli()