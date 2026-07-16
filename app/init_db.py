from app.database import Base, engine

# Import models ONLY here
from app.models.document import Document, Node

def init_db():
    Base.metadata.create_all(bind=engine)