"""
Document processing pipeline for extracting text from PDF files and other formats.
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import fitz  # PyMuPDF
import pdfplumber
from dataclasses import dataclass

from .config import config


@dataclass
class Document:
    """Represents a processed document."""
    filename: str
    title: str
    content: str
    sections: List[Dict[str, str]]
    metadata: Dict[str, str]


@dataclass
class DocumentSection:
    """Represents a section of a document."""
    title: str
    content: str
    level: int
    page_number: int


class DocumentProcessor:
    """Processes documents and extracts structured content."""

    def __init__(self):
        """Initialize the document processor."""
        self.logger = logging.getLogger(__name__)
        self.supported_formats = config.get('document_processing.supported_formats', ['pdf'])

    def process_file(self, file_path: str) -> Document:
        """
        Process a document file and extract structured content.

        Args:
            file_path: Path to the document file

        Returns:
            Document object with extracted content
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = file_path.suffix.lower().lstrip('.')

        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")

        if file_extension == 'pdf':
            return self._process_pdf(file_path)
        else:
            raise NotImplementedError(f"Processing for {file_extension} not yet implemented")

    def _process_pdf(self, file_path: Path) -> Document:
        """
        Process a PDF file using PyMuPDF.

        Args:
            file_path: Path to the PDF file

        Returns:
            Document object with extracted content
        """
        self.logger.info(f"Processing PDF: {file_path}")

        try:
            doc = fitz.open(file_path)
            full_text = ""
            sections = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                full_text += text + "\n"

            doc.close()

            # Extract sections from the text
            sections = self._extract_sections(full_text)

            # Extract metadata
            metadata = self._extract_metadata(full_text, file_path.name)

            return Document(
                filename=file_path.name,
                title=metadata.get('title', file_path.stem),
                content=full_text,
                sections=[{'title': s.title, 'content': s.content, 'level': s.level} for s in sections],
                metadata=metadata
            )

        except Exception as e:
            self.logger.error(f"Error processing PDF {file_path}: {e}")
            raise

    def _extract_sections(self, text: str) -> List[DocumentSection]:
        """
        Extract sections from document text using pattern matching.

        Args:
            text: Full document text

        Returns:
            List of DocumentSection objects
        """
        sections = []

        # Patterns for different section types
        patterns = [
            # Chapter/Section patterns for military doctrine
            (r'^(\d+\.?\s+[A-Z][A-Z\s]+)$', 1),  # "1. INTRODUCTION"
            (r'^(\d+\.\d+\.?\s+[A-Z][A-Z\s]+)$', 2),  # "1.1. OVERVIEW"
            (r'^(\d+\.\d+\.\d+\.?\s+[A-Z][A-Z\s]+)$', 3),  # "1.1.1. PURPOSE"
            (r'^([A-Z][A-Z\s]+)$', 1),  # "CHAPTER 1"
        ]

        lines = text.split('\n')
        current_section = None
        current_content = []

        for i, line in enumerate(lines):
            line = line.strip()

            if not line:
                continue

            # Check if line matches any section pattern
            for pattern, level in patterns:
                match = re.match(pattern, line)
                if match:
                    # Save previous section if exists
                    if current_section:
                        sections.append(DocumentSection(
                            title=current_section,
                            content='\n'.join(current_content).strip(),
                            level=level,
                            page_number=i // 50  # Rough page estimation
                        ))

                    # Start new section
                    current_section = match.group(1).strip()
                    current_content = []
                    break
            else:
                # Add line to current section content
                if current_section:
                    current_content.append(line)

        # Add final section
        if current_section:
            sections.append(DocumentSection(
                title=current_section,
                content='\n'.join(current_content).strip(),
                level=1,
                page_number=len(lines) // 50
            ))

        self.logger.info(f"Extracted {len(sections)} sections")
        return sections

    def _extract_metadata(self, text: str, filename: str) -> Dict[str, str]:
        """
        Extract metadata from document content.

        Args:
            text: Document text
            filename: Original filename

        Returns:
            Dictionary of metadata
        """
        metadata = {
            'filename': filename,
            'word_count': len(text.split()),
            'character_count': len(text)
        }

        # Try to extract title from first few lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Look for all-caps title in first few lines
            for line in lines[:10]:
                if line.isupper() and len(line) > 10:
                    metadata['title'] = line
                    break

        # Extract publication information
        pub_patterns = [
            (r'AFDP\s+(\d+[-\d]*)', 'afdp_number'),
            (r'AFTTP\s+(\d+[-\d]*)', 'afttp_number'),
            (r'JP\s+(\d+[-\d]*)', 'jp_number'),
            (r'(\d{1,2}\s+\w+\s+\d{4})', 'publication_date'),  # "15 April 2021"
        ]

        text_sample = text[:2000]  # Check first 2000 characters
        for pattern, key in pub_patterns:
            match = re.search(pattern, text_sample)
            if match:
                metadata[key] = match.group(1)

        return metadata

    def extract_ems_content(self, document: Document) -> Dict[str, str]:
        """
        Extract EMS-specific content from a document.

        Args:
            document: Processed document

        Returns:
            Dictionary of EMS-specific content sections
        """
        ems_content = {}

        # Keywords that indicate EMS-related sections
        ems_keywords = [
            'electromagnetic',
            'spectrum',
            'frequency',
            'jamming',
            'electronic warfare',
            'ems',
            'electronic attack',
            'electronic protection',
            'sead'
        ]

        for section in document.sections:
            section_title = section['title'].lower()
            section_content = section['content'].lower()

            # Check if section contains EMS content
            if any(keyword in section_title or keyword in section_content
                   for keyword in ems_keywords):
                ems_content[section['title']] = section['content']

        self.logger.info(f"Extracted {len(ems_content)} EMS-related sections")
        return ems_content