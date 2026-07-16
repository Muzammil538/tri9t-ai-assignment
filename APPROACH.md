# Design Approach

## Objective

The goal of this project is to automate the generation of QA test cases from medical device documentation while maintaining traceability across multiple document versions.

---

# System Architecture

```
PDF
 │
 ▼
Parser
 │
 ▼
SQLite Database
 │
 ├───────────────┐
 ▼               ▼
Browse API   Version Comparison
 │
 ▼
Selection
 │
 ▼
Groq LLM
 │
 ▼
Generated Test Cases
 │
 ▼
JSON Storage
 │
 ▼
Staleness Detection
```

---

# Design Decisions

## PDF Parsing

PyMuPDF was selected because it provides reliable text extraction while preserving document structure and page ordering.

---

## Database

SQLite was chosen because:

- Lightweight
- Zero configuration
- Sufficient for assignment requirements
- Easy local deployment

The database stores:

- Documents
- Nodes
- Parent-child relationships
- Selections

Generated outputs are intentionally stored outside SQLite.

---

## Hierarchy Reconstruction

Document sections are identified using numbered headings such as:

```
1
1.1
1.1.1
2
2.3
```

A stack-based approach reconstructs the parent-child hierarchy efficiently.

---

## Version Comparison

Each node stores a SHA-256 hash of its content.

Comparing two document versions involves matching logical sections and comparing hashes.

Possible outcomes:

- NEW
- MODIFIED
- UNCHANGED

This avoids expensive full-text comparisons.

---

## Selection

Selections allow users to group related document sections.

A many-to-many relationship is implemented between:

- Selection
- Node

This enables generating test cases for arbitrary document subsets.

---

## Test Case Generation

The selected document content is combined into a single prompt and sent to the Groq API.

The LLM is instructed to return structured JSON containing exactly five QA test cases.

The response is validated before being stored.

---

## Storage of Generated Output

Generated test cases are stored as JSON files.

Each file contains:

- Selection ID
- Version
- Content hashes
- Generated test cases

This simplifies retrieval and satisfies the assignment requirement for storing generated outputs separately from the relational database.

---

## Staleness Detection

Each generated file stores the content hashes used during generation.

When checking staleness:

1. Current hashes are retrieved from SQLite.
2. Stored hashes are loaded from the generated JSON.
3. Hashes are compared.

If differences exist, the generated output is marked as stale.

---

## Testing Strategy

The project includes tests for:

- PDF parsing
- Document ingestion
- Version comparison
- Browse API
- Generation API
- Retrieval API
- Staleness detection

Testing was performed using Pytest and FastAPI TestClient.

---

## Scalability

The architecture separates:

- Parsing
- Storage
- Business logic
- API
- LLM integration

This makes future migration to PostgreSQL, MongoDB, or another LLM provider straightforward without significant architectural changes.

---

## Conclusion

The implemented solution provides a modular backend capable of parsing structured medical documentation, tracking revisions, generating AI-assisted QA test cases, and detecting when generated outputs require regeneration after document updates.