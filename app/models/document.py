from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False)

    nodes = relationship(
        "Node",
        back_populates="document",
        cascade="all, delete"
    )


class Node(Base):
    __tablename__ = "nodes"

    id = Column(String, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    number = Column(String)
    title = Column(String)
    level = Column(Integer)

    content = Column(Text)
    content_hash = Column(String)
    
    logical_key = Column(String, index=True)

    parent_id = Column(
        String,
        ForeignKey("nodes.id"),
        nullable=True
    )

    document = relationship(
        "Document",
        back_populates="nodes"
    )
    
class Selection(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    version = Column(Integer, nullable=False)

    nodes = relationship(
        "SelectionNode",
        back_populates="selection",
        cascade="all, delete-orphan"
    )


class SelectionNode(Base):
    __tablename__ = "selection_nodes"

    selection_id = Column(
        Integer,
        ForeignKey("selections.id"),
        primary_key=True
    )

    node_id = Column(
        String,
        ForeignKey("nodes.id"),
        primary_key=True
    )

    selection = relationship(
        "Selection",
        back_populates="nodes"
    )

    node = relationship("Node")