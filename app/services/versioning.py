from app.database import SessionLocal
from app.models import Document, Node


class VersionService:

    def compare(self, old_version, new_version):

        db = SessionLocal()

        try:
            old_doc = db.query(Document).filter_by(version=old_version).first()
            new_doc = db.query(Document).filter_by(version=new_version).first()

            if not old_doc or not new_doc:
                raise ValueError("Document version not found.")

            old_nodes = db.query(Node).filter_by(document_id=old_doc.id).all()
            new_nodes = db.query(Node).filter_by(document_id=new_doc.id).all()

            old_lookup = {
                (n.number, n.title): n
                for n in old_nodes
            }

            changes = []

            for node in new_nodes:

                key = (node.number, node.title)

                if key not in old_lookup:
                    changes.append({
                        "node": node.number,
                        "status": "NEW"
                    })

                elif old_lookup[key].content_hash != node.content_hash:
                    changes.append({
                        "node": node.number,
                        "status": "MODIFIED"
                    })

            return changes

        finally:
            db.close()