from app.services.ingestion import IngestionService
from app.services.versioning import VersionService

ingestion = IngestionService()

ingestion.ingest(
    "data/ct200_manual_v2.pdf",
    "CT200",
    2
)

service = VersionService()

changes = service.compare(1, 2)

for change in changes:
    print(change)