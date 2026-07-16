from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Document, Node

from app.schemas import NodeResponse

router = APIRouter(prefix="/browse", tags=["Browse"])

# List Sections
@router.get("/sections/{version}",response_model=list[NodeResponse])
def get_sections(version: int, db: Session = Depends(get_db)):

    document = (
        db.query(Document)
        .filter_by(version=version)
        .first()
    )

    if not document:
        raise HTTPException(404, "Version not found")

    sections = (
        db.query(Node)
        .filter_by(
            document_id=document.id,
            level=1
        )
        .all()
    )

    return sections
  
#  Get Nodes
@router.get("/node/{node_id}")
def get_node(node_id: str, db: Session = Depends(get_db)):

    node = db.query(Node).filter_by(id=node_id).first()

    if not node:
        raise HTTPException(404, "Node not found")

    children = (
        db.query(Node)
        .filter_by(parent_id=node.id)
        .all()
    )

    return {
        "node": node,
        "children": children
    }
    
# Search 
@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):

    result = (
        db.query(Node)
        .filter(
            or_(
                Node.title.contains(q),
                Node.content.contains(q)
            )
        )
        .all()
    )

    return result