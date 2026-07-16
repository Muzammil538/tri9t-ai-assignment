from app.init_db import init_db
from app.services.ingestion import IngestionService


def test_ingestion():

    init_db()

    service = IngestionService()

    document_id = service.ingest(
        "data/ct200_manual.pdf",
        "CT200",
        1
    )

    assert document_id > 0