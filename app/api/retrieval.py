import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Selection, Node

router = APIRouter(
    prefix="",
    tags=["Retrieval"]
)

@router.get("/generation/{selection_id}")
def get_generation(selection_id: int):

    file_path = Path(f"generated/selection_{selection_id}.json")

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Generated output not found."
        )

    with open(file_path, "r") as f:
        return json.load(f)
      
@router.get("/stale/{selection_id}")
def check_stale(
    selection_id: int,
    db: Session = Depends(get_db)
):

    selection = (
        db.query(Selection)
        .filter_by(id=selection_id)
        .first()
    )

    if not selection:
        raise HTTPException(
            status_code=404,
            detail="Selection not found."
        )

    file_path = Path(f"generated/selection_{selection_id}.json")

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Generated output not found."
        )

    with open(file_path, "r") as f:
        generated = json.load(f)

    old_hashes = generated["content_hashes"]

    current_hashes = []

    for item in selection.nodes:
        current_hashes.append(item.node.content_hash)

    stale = old_hashes != current_hashes

    return {
        "selection_id": selection_id,
        "stale": stale,
        "stored_hashes": old_hashes,
        "current_hashes": current_hashes
    }