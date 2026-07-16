import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Selection,
    Node
)

from app.llm.groq_client import generate_test_cases

router = APIRouter(
    prefix="/generate",
    tags=["Generation"]
)

@router.post("/{selection_id}")
def generate(selection_id: int,
             db: Session = Depends(get_db)):

    selection = (
        db.query(Selection)
        .filter_by(id=selection_id)
        .first()
    )

    if not selection:
        raise HTTPException(404, "Selection not found")

    text = ""

    hashes = []

    for item in selection.nodes:

        node = item.node

        text += f"{node.number} {node.title}\n"

        text += node.content

        text += "\n\n"

        hashes.append(node.content_hash)

    try:
        result = generate_test_cases(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM generation failed: {str(e)}"
        )

    output = {
        "selection_id": selection.id,
        "version": selection.version,
        "content_hashes": hashes,
        "test_cases": result["test_cases"]
    }

    Path("generated").mkdir(exist_ok=True)

    with open(
        f"generated/selection_{selection.id}.json",
        "w"
    ) as f:

        json.dump(
            output,
            f,
            indent=4
        )

    return output