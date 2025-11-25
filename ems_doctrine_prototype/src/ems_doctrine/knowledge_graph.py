"""
Knowledge graph storage and management system for EMS doctrine.
Uses SQLite for persistence and NetworkX for graph operations.
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import networkx as nx
from dataclasses import dataclass, asdict

from .config import config
from .entity_recognition import Entity


@dataclass
class Node:
    """Represents a node in the knowledge graph."""
    id: str
    label: str
    type: str
    properties: Dict[str, Any]
    source_document: str = ""
    confidence: float = 1.0


@dataclass
class Edge:
    """Represents an edge (relationship) in the knowledge graph."""
    source: str
    target: str
    relationship: str
    properties: Dict[str, Any]
    confidence: float = 1.0


class KnowledgeGraph:
    """Manages the EMS doctrine knowledge graph."""

    def __init__(self, db_path: str = None):
        """
        Initialize the knowledge graph.

        Args:
            db_path: Path to SQLite database file
        """
        self.logger = logging.getLogger(__name__)

        if db_path is None:
            db_path = config.database_path

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize NetworkX graph
        self.graph = nx.MultiDiGraph()

        # Initialize database
        self._init_database()

        # Load existing data
        self._load_from_database()

    def _init_database(self):
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create nodes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    type TEXT NOT NULL,
                    properties TEXT,
                    source_document TEXT,
                    confidence REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create edges table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    relationship TEXT NOT NULL,
                    properties TEXT,
                    confidence REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source) REFERENCES nodes (id),
                    FOREIGN KEY (target) REFERENCES nodes (id)
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes (type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_relationship ON edges (relationship)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges (source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges (target)")

            conn.commit()

        self.logger.info(f"Database initialized at {self.db_path}")

    def _load_from_database(self):
        """Load existing nodes and edges from database into NetworkX graph."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Load nodes
            cursor.execute("SELECT id, label, type, properties, source_document, confidence FROM nodes")
            for row in cursor.fetchall():
                node_id, label, node_type, properties_json, source_doc, confidence = row
                properties = json.loads(properties_json) if properties_json else {}

                self.graph.add_node(node_id,
                                  label=label,
                                  type=node_type,
                                  properties=properties,
                                  source_document=source_doc,
                                  confidence=confidence)

            # Load edges
            cursor.execute("SELECT source, target, relationship, properties, confidence FROM edges")
            for row in cursor.fetchall():
                source, target, relationship, properties_json, confidence = row
                properties = json.loads(properties_json) if properties_json else {}

                self.graph.add_edge(source, target,
                                  relationship=relationship,
                                  properties=properties,
                                  confidence=confidence)

        self.logger.info(f"Loaded {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")

    def add_node(self, node: Node) -> bool:
        """
        Add a node to the knowledge graph.

        Args:
            node: Node to add

        Returns:
            True if node was added, False if it already exists
        """
        if node.id in self.graph:
            self.logger.debug(f"Node {node.id} already exists")
            return False

        # Add to NetworkX graph
        self.graph.add_node(node.id,
                          label=node.label,
                          type=node.type,
                          properties=node.properties,
                          source_document=node.source_document,
                          confidence=node.confidence)

        # Add to database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO nodes (id, label, type, properties, source_document, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (node.id, node.label, node.type, json.dumps(node.properties),
                  node.source_document, node.confidence))
            conn.commit()

        self.logger.debug(f"Added node: {node.id}")
        return True

    def add_edge(self, edge: Edge) -> bool:
        """
        Add an edge to the knowledge graph.

        Args:
            edge: Edge to add

        Returns:
            True if edge was added, False if nodes don't exist
        """
        if edge.source not in self.graph or edge.target not in self.graph:
            self.logger.warning(f"Cannot add edge: missing nodes {edge.source} or {edge.target}")
            return False

        # Add to NetworkX graph
        self.graph.add_edge(edge.source, edge.target,
                          relationship=edge.relationship,
                          properties=edge.properties,
                          confidence=edge.confidence)

        # Add to database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO edges (source, target, relationship, properties, confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (edge.source, edge.target, edge.relationship,
                  json.dumps(edge.properties), edge.confidence))
            conn.commit()

        self.logger.debug(f"Added edge: {edge.source} -> {edge.target} ({edge.relationship})")
        return True

    def add_entities_from_document(self, entities: List[Entity], document_name: str):
        """
        Add entities from a document to the knowledge graph.

        Args:
            entities: List of entities to add
            document_name: Name of source document
        """
        nodes_added = 0
        for entity in entities:
            # Create unique node ID
            node_id = f"{entity.label}_{entity.text.replace(' ', '_').lower()}"

            node = Node(
                id=node_id,
                label=entity.text,
                type=entity.label,
                properties={
                    'original_text': entity.text,
                    'context': entity.context,
                    'start_pos': entity.start,
                    'end_pos': entity.end
                },
                source_document=document_name,
                confidence=entity.confidence
            )

            if self.add_node(node):
                nodes_added += 1

        self.logger.info(f"Added {nodes_added} nodes from document {document_name}")

    def add_relationships_from_data(self, relationships: List[Dict], document_name: str):
        """
        Add relationships from extracted data to the knowledge graph.

        Args:
            relationships: List of relationship dictionaries
            document_name: Name of source document
        """
        edges_added = 0
        for rel in relationships:
            # Create node IDs (simplified approach)
            source_id = f"entity_{rel['subject'].replace(' ', '_').lower()}"
            target_id = f"entity_{rel['object'].replace(' ', '_').lower()}"

            # Add nodes if they don't exist
            source_node = Node(
                id=source_id,
                label=rel['subject'],
                type='ENTITY',
                properties={'original_text': rel['subject']},
                source_document=document_name
            )
            target_node = Node(
                id=target_id,
                label=rel['object'],
                type='ENTITY',
                properties={'original_text': rel['object']},
                source_document=document_name
            )

            self.add_node(source_node)
            self.add_node(target_node)

            # Add edge
            edge = Edge(
                source=source_id,
                target=target_id,
                relationship=rel['predicate'],
                properties={'context': rel.get('context', '')},
                confidence=rel.get('confidence', 0.8)
            )

            if self.add_edge(edge):
                edges_added += 1

        self.logger.info(f"Added {edges_added} relationships from document {document_name}")

    def query_nodes(self, node_type: str = None, properties: Dict = None) -> List[Node]:
        """
        Query nodes by type and properties.

        Args:
            node_type: Filter by node type
            properties: Filter by node properties

        Returns:
            List of matching nodes
        """
        results = []

        for node_id, node_data in self.graph.nodes(data=True):
            # Filter by type
            if node_type and node_data.get('type') != node_type:
                continue

            # Filter by properties
            if properties:
                match = True
                node_props = node_data.get('properties', {})
                for key, value in properties.items():
                    if key not in node_props or node_props[key] != value:
                        match = False
                        break
                if not match:
                    continue

            # Create Node object
            node = Node(
                id=node_id,
                label=node_data.get('label', ''),
                type=node_data.get('type', ''),
                properties=node_data.get('properties', {}),
                source_document=node_data.get('source_document', ''),
                confidence=node_data.get('confidence', 1.0)
            )
            results.append(node)

        return results

    def query_relationships(self, source: str = None, target: str = None,
                          relationship: str = None) -> List[Edge]:
        """
        Query relationships by source, target, and relationship type.

        Args:
            source: Source node ID
            target: Target node ID
            relationship: Relationship type

        Returns:
            List of matching edges
        """
        results = []

        for s, t, edge_data in self.graph.edges(data=True):
            # Filter by source
            if source and s != source:
                continue

            # Filter by target
            if target and t != target:
                continue

            # Filter by relationship
            if relationship and edge_data.get('relationship') != relationship:
                continue

            # Create Edge object
            edge = Edge(
                source=s,
                target=t,
                relationship=edge_data.get('relationship', ''),
                properties=edge_data.get('properties', {}),
                confidence=edge_data.get('confidence', 1.0)
            )
            results.append(edge)

        return results

    def find_paths(self, source: str, target: str, max_length: int = 3) -> List[List[str]]:
        """
        Find paths between two nodes.

        Args:
            source: Source node ID
            target: Target node ID
            max_length: Maximum path length

        Returns:
            List of paths (each path is a list of node IDs)
        """
        if source not in self.graph or target not in self.graph:
            return []

        try:
            paths = list(nx.all_simple_paths(self.graph, source, target, cutoff=max_length))
            return paths
        except nx.NetworkXNoPath:
            return []

    def get_neighbors(self, node_id: str, relationship: str = None) -> List[str]:
        """
        Get neighboring nodes.

        Args:
            node_id: Node ID
            relationship: Filter by relationship type

        Returns:
            List of neighbor node IDs
        """
        if node_id not in self.graph:
            return []

        neighbors = []

        # Outgoing edges
        for target, edge_data in self.graph[node_id].items():
            if relationship is None or edge_data.get('relationship') == relationship:
                neighbors.append(target)

        # Incoming edges
        for source in self.graph.predecessors(node_id):
            edge_data = self.graph[source][node_id]
            if relationship is None or edge_data.get('relationship') == relationship:
                if source not in neighbors:
                    neighbors.append(source)

        return neighbors

    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics."""
        node_types = {}
        edge_types = {}

        # Count node types
        for _, node_data in self.graph.nodes(data=True):
            node_type = node_data.get('type', 'UNKNOWN')
            node_types[node_type] = node_types.get(node_type, 0) + 1

        # Count edge types
        for _, _, edge_data in self.graph.edges(data=True):
            edge_type = edge_data.get('relationship', 'UNKNOWN')
            edge_types[edge_type] = edge_types.get(edge_type, 0) + 1

        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'node_types': node_types,
            'edge_types': edge_types,
            'is_connected': nx.is_connected(self.graph.to_undirected()),
            'number_of_components': nx.number_connected_components(self.graph.to_undirected())
        }

    def export_graphml(self, file_path: str):
        """Export graph to GraphML format for visualization."""
        nx.write_graphml(self.graph, file_path)
        self.logger.info(f"Exported graph to {file_path}")

    def clear_all(self):
        """Clear all data from the knowledge graph."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM edges")
            cursor.execute("DELETE FROM nodes")
            conn.commit()

        self.graph.clear()
        self.logger.info("Cleared all data from knowledge graph")