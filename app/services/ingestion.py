from app.database import SessionLocal
from app.models import Document, Node
from app.parser.pdf_parser import PDFParser


class IngestionService:

    def ingest(self, pdf_path, name, version):

        parser = PDFParser(pdf_path)
        parsed_nodes = parser.parse()

        db = SessionLocal()

        document = Document(
            name=name,
            version=version
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        for item in parsed_nodes:

            node = Node(
                id=item["id"],
                document_id=document.id,
                number=item["number"],
                title=item["title"],
                level=item["level"],
                content=item["content"],
                content_hash=item["hash"],
                parent_id=item["parent"],
                logical_key=f"{item['number']}|{item['title']}",
            )

            db.add(node)

        db.commit()
        document_id = document.id
        db.close()

        return document_id