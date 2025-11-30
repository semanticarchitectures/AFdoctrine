# EMS Doctrine Prototype

Phase 0 prototype for digitizing Air Force electromagnetic spectrum operations doctrine.

## Overview

This prototype demonstrates the feasibility of converting static PDF doctrine into machine-readable, semantically structured formats that enable automated analysis and AI agent integration. The system focuses specifically on electromagnetic spectrum (EMS) operations doctrine as a proof-of-concept for broader doctrinal digitization.

## Features

- **Document Processing**: Extract text and structure from PDF documents
- **Entity Recognition**: Identify EMS-specific entities (frequencies, equipment, authorities, operations)
- **Rule Extraction**: Extract obligations, permissions, and prohibitions using deontic logic patterns
- **Knowledge Graph**: Store entities and relationships in a queryable graph database
- **Conflict Detection**: Identify conflicts between extracted rules
- **REST API**: Query and interact with extracted knowledge via HTTP endpoints
- **Command Line Interface**: Process documents and extract information via CLI

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   Entity         │    │   Rule          │
│   Processing    │───▶│   Recognition    │───▶│   Extraction    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   REST API      │◄───│   Knowledge      │◄───│   Conflict      │
│                 │    │   Graph          │    │   Detection     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Document Processing | PyMuPDF, pdfplumber | PDF text extraction |
| NLP | spaCy, NLTK | Entity recognition, text processing |
| Knowledge Graph | SQLite + NetworkX | Data storage and graph operations |
| API | Flask | REST endpoints |
| Database | SQLite | Persistent storage |

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ems_doctrine_prototype
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Install package in development mode**:
   ```bash
   pip install -e .
   ```

## Quick Start

1. **Initialize the environment**:
   ```bash
   ems-doctrine init
   ```

2. **Run demonstration**:
   ```bash
   ems-doctrine demo
   ```

3. **Process sample document**:
   ```bash
   ems-doctrine process-document data/raw/sample_ems_doctrine.txt --output results/
   ```

4. **Start API server**:
   ```bash
   ems-doctrine serve
   ```

5. **View API documentation**:
   Open http://localhost:5000 in your browser

## Command Line Usage

### Process a Document
```bash
ems-doctrine process-document path/to/document.pdf --output results/
```

### Extract Entities from Text
```bash
ems-doctrine extract-entities "JFACC must coordinate all EMS operations on UHF frequencies"
```

### Extract Rules from Text
```bash
ems-doctrine extract-rules "Electronic warfare officers are prohibited from using commercial frequencies"
```

### Start API Server
```bash
ems-doctrine serve --host 0.0.0.0 --port 8080 --debug
```

## API Usage

### Extract Entities
```bash
curl -X POST http://localhost:5000/extract_entities \
  -H "Content-Type: application/json" \
  -d '{"text": "JFACC must coordinate all EMS operations on UHF frequencies"}'
```

### Extract Rules
```bash
curl -X POST http://localhost:5000/extract_rules \
  -H "Content-Type: application/json" \
  -d '{"text": "Electronic warfare officers are prohibited from using commercial frequencies"}'
```

### Query Knowledge Graph Nodes
```bash
curl "http://localhost:5000/knowledge_graph/nodes?type=FREQUENCY"
```

### Query Relationships
```bash
curl "http://localhost:5000/knowledge_graph/relationships?relationship=COORDINATES"
```

### Get System Status
```bash
curl "http://localhost:5000/status"
```

## EMS Domain Coverage

The prototype recognizes and processes the following EMS domain entities:

### Frequency Bands
- HF (3-30 MHz)
- VHF (30-300 MHz)
- UHF (300-3000 MHz)
- SHF (3-30 GHz)
- EHF (30-300 GHz)

### Equipment Types
- Jammers and jamming systems
- Radios and communication equipment
- Radars and sensors
- Antennas and transmitters

### Operations
- Electronic Attack (EA)
- Electronic Protection (EP)
- Electronic Warfare Support (ES)
- Spectrum Management
- SEAD (Suppression of Enemy Air Defenses)

### Authorities
- JFACC (Joint Force Air Component Commander)
- JFC (Joint Force Commander)
- JEMSO (Joint Electronic Warfare Staff Officer)
- Spectrum Manager
- EWO (Electronic Warfare Officer)

## Rule Types

The system extracts three types of deontic logic rules:

1. **Obligations** (`must`, `shall`, `will`, `required`)
   - "Commanders must ensure frequency coordination"

2. **Permissions** (`may`, `can`, `authorized`, `allowed`)
   - "Units may transmit on designated frequencies"

3. **Prohibitions** (`must not`, `shall not`, `prohibited`, `forbidden`)
   - "Personnel are prohibited from using commercial frequencies"

## Sample Results

### Entity Extraction Example
Input: "JFACC must coordinate all EMS operations on UHF frequencies"

Output:
```json
{
  "entities": [
    {"text": "JFACC", "label": "AUTHORITY", "confidence": 1.0},
    {"text": "EMS operations", "label": "EMS_OPERATION", "confidence": 0.9},
    {"text": "UHF", "label": "FREQUENCY", "confidence": 1.0}
  ]
}
```

### Rule Extraction Example
Input: "Electronic warfare officers are prohibited from using commercial frequencies"

Output:
```json
{
  "rules": [
    {
      "id": "rule_0001",
      "type": "prohibition",
      "subject": "Electronic warfare officers",
      "action": "use",
      "object": "commercial frequencies",
      "confidence": 0.85
    }
  ]
}
```

## Configuration

Configuration is managed through `config/config.yaml`. Key settings include:

- **NLP Model**: spaCy model for text processing
- **Entity Types**: Custom EMS entity categories
- **Database Path**: SQLite database location
- **API Settings**: Host, port, debug mode
- **Deontic Keywords**: Words that indicate obligations, permissions, prohibitions

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=ems_doctrine --cov-report=html
```

## Phase 0 Limitations

This is a proof-of-concept prototype with the following limitations:

- **Limited Document Format Support**: Currently only supports PDF and text files
- **Simplified Knowledge Graph**: Uses SQLite + NetworkX instead of enterprise graph database
- **Basic Conflict Detection**: Simple pattern-based conflict identification
- **No Authentication**: API endpoints are not secured
- **Single Document Focus**: Not optimized for large document corpora

## Future Expansion

### Phase 1 (Months 7-12)
- Upgrade to full Akoma Ntoso document structure
- Implement Common Core Ontology (CCO) semantic modeling
- Add PostgreSQL + Neo4j for enterprise-scale storage
- Multi-domain doctrine integration (C2, Airspace Control)

### Phase 2 (Months 13-18)
- LegalRuleML for formal rule representation
- Advanced reasoning and inference capabilities
- "Doctrinal Governor" for AI agent compliance
- Integration with operational systems

### Phase 3 (Months 19-24)
- Full Air Force doctrine corpus
- Cloud deployment and enterprise security
- Real-time doctrine updating capabilities
- Operational integration and validation

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `pytest`
5. Submit pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions about this prototype or the broader doctrinal digitization initiative, contact the AF Doctrine Digitization Team.

## Acknowledgments

This prototype was developed as part of the Air Force's initiative to modernize doctrine for AI-enabled operations, supporting the Joint All-Domain Command and Control (JADC2) vision.