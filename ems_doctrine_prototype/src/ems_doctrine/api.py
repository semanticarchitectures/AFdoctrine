"""
Flask API for EMS Doctrine Prototype.
Provides REST endpoints for document processing, entity recognition, and knowledge graph queries.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import tempfile

from .config import config
from .document_processing import DocumentProcessor
from .entity_recognition import EMSEntityRecognizer
from .knowledge_graph import KnowledgeGraph
from .rule_extraction import RuleExtractor, DeonticType


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
doc_processor = DocumentProcessor()
entity_recognizer = EMSEntityRecognizer()
knowledge_graph = KnowledgeGraph()
rule_extractor = RuleExtractor()


@app.route('/')
def index():
    """Home page with API documentation."""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>EMS Doctrine Prototype API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1, h2 { color: #2c3e50; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #27ae60; font-weight: bold; }
            code { background: #ecf0f1; padding: 2px 5px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>EMS Doctrine Prototype API</h1>
        <p>Phase 0 prototype for digitizing Air Force electromagnetic spectrum operations doctrine.</p>

        <h2>Available Endpoints</h2>

        <div class="endpoint">
            <h3><span class="method">GET</span> /status</h3>
            <p>Get system status and statistics</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> /process_document</h3>
            <p>Process a document and extract entities and rules</p>
            <p><strong>Body:</strong> <code>{"file_path": "path/to/document.pdf"}</code></p>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> /extract_entities</h3>
            <p>Extract entities from text</p>
            <p><strong>Body:</strong> <code>{"text": "EMS operations must coordinate on VHF frequencies"}</code></p>
        </div>

        <div class="endpoint">
            <h3><span class="method">POST</span> /extract_rules</h3>
            <p>Extract rules from text</p>
            <p><strong>Body:</strong> <code>{"text": "Commanders must ensure frequency coordination"}</code></p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> /knowledge_graph/nodes</h3>
            <p>Query knowledge graph nodes</p>
            <p><strong>Parameters:</strong> <code>type</code> (optional)</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> /knowledge_graph/relationships</h3>
            <p>Query knowledge graph relationships</p>
            <p><strong>Parameters:</strong> <code>source</code>, <code>target</code>, <code>relationship</code> (all optional)</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> /rules</h3>
            <p>Get extracted rules</p>
            <p><strong>Parameters:</strong> <code>type</code> (obligation/permission/prohibition)</p>
        </div>

        <div class="endpoint">
            <h3><span class="method">GET</span> /conflicts</h3>
            <p>Get detected rule conflicts</p>
        </div>

        <h2>Example Usage</h2>
        <pre>
# Extract entities from text
curl -X POST http://localhost:5000/extract_entities \\
  -H "Content-Type: application/json" \\
  -d '{"text": "JFACC must coordinate all EMS operations on UHF frequencies"}'

# Query knowledge graph nodes
curl "http://localhost:5000/knowledge_graph/nodes?type=FREQUENCY"
        </pre>
    </body>
    </html>
    """)


@app.route('/status')
def get_status():
    """Get system status and statistics."""
    try:
        kg_stats = knowledge_graph.get_statistics()
        rule_stats = rule_extractor.get_statistics()

        return jsonify({
            'status': 'healthy',
            'version': config.version,
            'knowledge_graph': kg_stats,
            'rules': rule_stats,
            'components': {
                'document_processor': 'active',
                'entity_recognizer': 'active',
                'knowledge_graph': 'active',
                'rule_extractor': 'active'
            }
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/process_document', methods=['POST'])
def process_document():
    """Process a document and extract all information."""
    try:
        data = request.get_json()
        if not data or 'file_path' not in data:
            return jsonify({'error': 'file_path is required'}), 400

        file_path = data['file_path']
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 404

        # Process document
        document = doc_processor.process_file(file_path)

        # Extract entities
        entities = entity_recognizer.extract_entities(document.content)

        # Extract rules
        rules = rule_extractor.extract_rules(document.content, document.filename)

        # Add to knowledge graph
        knowledge_graph.add_entities_from_document(entities, document.filename)

        # Extract relationships
        relationships = entity_recognizer.extract_relationships(document.content, entities)
        knowledge_graph.add_relationships_from_data(relationships, document.filename)

        # Detect conflicts
        conflicts = rule_extractor.detect_conflicts(rules)

        return jsonify({
            'document': {
                'filename': document.filename,
                'title': document.title,
                'sections': len(document.sections),
                'word_count': document.metadata.get('word_count', 0)
            },
            'entities': {
                'total': len(entities),
                'by_type': entity_recognizer.get_entity_statistics(entities)
            },
            'rules': {
                'total': len(rules),
                'obligations': len([r for r in rules if r.rule_type == DeonticType.OBLIGATION]),
                'permissions': len([r for r in rules if r.rule_type == DeonticType.PERMISSION]),
                'prohibitions': len([r for r in rules if r.rule_type == DeonticType.PROHIBITION])
            },
            'relationships': len(relationships),
            'conflicts': len(conflicts),
            'processing_complete': True
        })

    except Exception as e:
        logger.error(f"Error processing document: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/extract_entities', methods=['POST'])
def extract_entities():
    """Extract entities from text."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'text is required'}), 400

        text = data['text']
        entities = entity_recognizer.extract_entities(text)

        entities_data = []
        for entity in entities:
            entities_data.append({
                'text': entity.text,
                'label': entity.label,
                'start': entity.start,
                'end': entity.end,
                'confidence': entity.confidence,
                'context': entity.context
            })

        return jsonify({
            'entities': entities_data,
            'total': len(entities),
            'statistics': entity_recognizer.get_entity_statistics(entities)
        })

    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/extract_rules', methods=['POST'])
def extract_rules():
    """Extract rules from text."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'text is required'}), 400

        text = data['text']
        document_name = data.get('document_name', 'api_input')
        section = data.get('section', '')

        rules = rule_extractor.extract_rules(text, document_name, section)

        rules_data = []
        for rule in rules:
            rules_data.append({
                'id': rule.id,
                'type': rule.rule_type.value,
                'subject': rule.subject,
                'action': rule.action,
                'object': rule.object,
                'condition': rule.condition,
                'text': rule.text,
                'confidence': rule.confidence,
                'source_document': rule.source_document,
                'section': rule.section
            })

        return jsonify({
            'rules': rules_data,
            'total': len(rules),
            'statistics': {
                'obligations': len([r for r in rules if r.rule_type == DeonticType.OBLIGATION]),
                'permissions': len([r for r in rules if r.rule_type == DeonticType.PERMISSION]),
                'prohibitions': len([r for r in rules if r.rule_type == DeonticType.PROHIBITION])
            }
        })

    except Exception as e:
        logger.error(f"Error extracting rules: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/knowledge_graph/nodes')
def query_nodes():
    """Query knowledge graph nodes."""
    try:
        node_type = request.args.get('type')
        properties = {}

        # Parse property filters from query parameters
        for key, value in request.args.items():
            if key.startswith('prop_'):
                prop_name = key[5:]  # Remove 'prop_' prefix
                properties[prop_name] = value

        nodes = knowledge_graph.query_nodes(node_type, properties if properties else None)

        nodes_data = []
        for node in nodes:
            nodes_data.append({
                'id': node.id,
                'label': node.label,
                'type': node.type,
                'properties': node.properties,
                'source_document': node.source_document,
                'confidence': node.confidence
            })

        return jsonify({
            'nodes': nodes_data,
            'total': len(nodes)
        })

    except Exception as e:
        logger.error(f"Error querying nodes: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/knowledge_graph/relationships')
def query_relationships():
    """Query knowledge graph relationships."""
    try:
        source = request.args.get('source')
        target = request.args.get('target')
        relationship = request.args.get('relationship')

        edges = knowledge_graph.query_relationships(source, target, relationship)

        edges_data = []
        for edge in edges:
            edges_data.append({
                'source': edge.source,
                'target': edge.target,
                'relationship': edge.relationship,
                'properties': edge.properties,
                'confidence': edge.confidence
            })

        return jsonify({
            'relationships': edges_data,
            'total': len(edges)
        })

    except Exception as e:
        logger.error(f"Error querying relationships: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/knowledge_graph/paths')
def find_paths():
    """Find paths between two nodes."""
    try:
        source = request.args.get('source')
        target = request.args.get('target')
        max_length = int(request.args.get('max_length', 3))

        if not source or not target:
            return jsonify({'error': 'source and target parameters are required'}), 400

        paths = knowledge_graph.find_paths(source, target, max_length)

        return jsonify({
            'paths': paths,
            'total': len(paths),
            'source': source,
            'target': target,
            'max_length': max_length
        })

    except Exception as e:
        logger.error(f"Error finding paths: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/rules')
def get_rules():
    """Get extracted rules."""
    try:
        rule_type = request.args.get('type')
        subject = request.args.get('subject')

        rules = rule_extractor.rules

        if rule_type:
            try:
                deontic_type = DeonticType(rule_type.lower())
                rules = [r for r in rules if r.rule_type == deontic_type]
            except ValueError:
                return jsonify({'error': f'Invalid rule type: {rule_type}'}), 400

        if subject:
            rules = [r for r in rules if subject.lower() in r.subject.lower()]

        rules_data = []
        for rule in rules:
            rules_data.append({
                'id': rule.id,
                'type': rule.rule_type.value,
                'subject': rule.subject,
                'action': rule.action,
                'object': rule.object,
                'condition': rule.condition,
                'text': rule.text,
                'confidence': rule.confidence,
                'source_document': rule.source_document,
                'section': rule.section
            })

        return jsonify({
            'rules': rules_data,
            'total': len(rules)
        })

    except Exception as e:
        logger.error(f"Error getting rules: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/conflicts')
def get_conflicts():
    """Get detected rule conflicts."""
    try:
        conflicts = rule_extractor.detect_conflicts(rule_extractor.rules)

        conflicts_data = []
        for conflict in conflicts:
            conflicts_data.append({
                'rule1_id': conflict.rule1_id,
                'rule2_id': conflict.rule2_id,
                'conflict_type': conflict.conflict_type,
                'description': conflict.description,
                'confidence': conflict.confidence
            })

        return jsonify({
            'conflicts': conflicts_data,
            'total': len(conflicts)
        })

    except Exception as e:
        logger.error(f"Error getting conflicts: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/knowledge_graph/statistics')
def get_kg_statistics():
    """Get knowledge graph statistics."""
    try:
        stats = knowledge_graph.get_statistics()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting KG statistics: {e}")
        return jsonify({'error': str(e)}), 500


def create_app():
    """Application factory function."""
    return app


if __name__ == '__main__':
    # Run the Flask app
    host = config.get('api.host', 'localhost')
    port = config.get('api.port', 5000)
    debug = config.get('api.debug', True)

    logger.info(f"Starting EMS Doctrine Prototype API on {host}:{port}")
    app.run(host=host, port=port, debug=debug)