from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Selection,
    SelectionNode,
    Document,
    Node
)
from app.schemas import SelectionCreate

router = APIRouter(
    prefix="/selection",
    tags=["Selection"]
)

@router.post("/")
def create_selection(
    data: SelectionCreate,
    db: Session = Depends(get_db)
):

    document = (
        db.query(Document)
        .filter_by(version=data.version)
        .first()
    )

    if not document:
        raise HTTPException(404, "Document version not found")

    selection = Selection(
        name=data.name,
        version=data.version
    )

    db.add(selection)
    db.commit()
    db.refresh(selection)

    for node_id in data.node_ids:

        node = db.query(Node).filter_by(id=node_id).first()

        if not node:
            continue

        db.add(
            SelectionNode(
                selection_id=selection.id,
                node_id=node.id
            )
        )

    db.commit()

    return {
        "selection_id": selection.id,
        "message": "Selection created"
    }
    
@router.get("/{selection_id}")
def get_selection(
    selection_id: int,
    db: Session = Depends(get_db)
):

    selection = (
        db.query(Selection)
        .filter_by(id=selection_id)
        .first()
    )

    if not selection:
        raise HTTPException(404, "Selection not found")

    nodes = []

    for item in selection.nodes:

        nodes.append({
            "id": item.node.id,
            "number": item.node.number,
            "title": item.node.title
        })

    return {
        "id": selection.id,
        "name": selection.name,
        "version": selection.version,
        "nodes": nodes
    }
    
@router.delete("/{selection_id}")
def delete_selection(
    selection_id: int,
    db: Session = Depends(get_db)
):

    selection = (
        db.query(Selection)
        .filter_by(id=selection_id)
        .first()
    )

    if not selection:
        raise HTTPException(404, "Selection not found")

    db.delete(selection)
    db.commit()

    return {
        "message": "Selection deleted"
    }