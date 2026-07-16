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

    parent_id = Column(
        String,
        ForeignKey("nodes.id"),
        nullable=True
    )

    document = relationship(
        "Document",
        back_populates="nodes"
    )