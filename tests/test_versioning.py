from app.services.versioning import VersionService


def test_versioning():

    service = VersionService()

    changes = service.compare(1, 2)

    assert len(changes) > 0

    statuses = [c["status"] for c in changes]

    assert "NEW" in statuses

    assert "MODIFIED" in statuses