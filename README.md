# CT200 Document Parser & Test Case Generator

## Overview

This project is a backend application developed as part of the Tri9T AI Assignment.

The system parses medical device manuals (PDF), stores the document hierarchy, tracks document versions, allows users to browse and select sections, generates QA test cases using an LLM (Groq), and detects whether generated test cases become outdated after document updates.

---

## Features

- Parse PDF manuals into hierarchical sections
- Store document hierarchy in SQLite
- Compare document versions
- Browse document sections
- Search document content
- Create reusable selections
- Generate QA test cases using Groq LLM
- Retrieve generated test cases
- Detect stale generated outputs using content hashing
- REST API with Swagger documentation
- Unit tests using Pytest

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- PyMuPDF (fitz)
- Groq API
- Pytest

---

## Project Structure

```
app/
├── api/
│      __init__.py
│     browse.py
│     selection.py
│     generation.py
│     retrieval.py
│
├── parser/
│     __init__.py
│     pdf_parser.py
│
├── llm/
│     groq_client.py
│
├── services/
│     __init__.py
│     versioning.py
│     llm_service.py
│     staleness.py
|     ingestion.py
│
├── models/
│     __init__.py
│     document.py
│     selection.py
│
│__ __init__.py
│__ init_db.py
├── database.py
├── schemas.py
└── main.py

generated/
tests/
data/
```

---

## Installation

Create a virtual environment

```bash
python -m venv venv
```

Activate

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Application

```bash
python -m uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Workflow

```
PDF
   │
   ▼
PDF Parser
   │
   ▼
SQLite Database
   │
   ▼
Browse API
   │
   ▼
Create Selection
   │
   ▼
Groq LLM
   │
   ▼
Generated JSON
   │
   ▼
Retrieval API
   │
   ▼
Staleness Detection
```

---

## API Endpoints

### Browse

```
GET /browse/sections/{version}
GET /browse/node/{id}
GET /browse/search
```

### Selection

```
POST /selection
GET /selection/{id}
DELETE /selection/{id}
```

### Generation

```
POST /generate/{selection_id}
GET /generation/{selection_id}
```

### Validation

```
GET /stale/{selection_id}
```

---

## Running Tests

Run all tests

```bash
python -m pytest
```

---

## Assumptions

- Documents follow numbered section hierarchy.
- Content hashing is performed using SHA-256.
- Generated outputs are stored as JSON files.
- Groq API is available during generation.

---

## Future Improvements

- MongoDB support for generated outputs
- Authentication
- Background task processing
- Multiple LLM providers
- Docker deployment
