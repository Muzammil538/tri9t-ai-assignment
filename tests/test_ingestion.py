from app.init_db import init_db
from app.services.ingestion import IngestionService

init_db()

service = IngestionService()

doc_id = service.ingest(
    "data/ct200_manual.pdf",
    "CT200",
    1
)

print("Document ID:", doc_id)