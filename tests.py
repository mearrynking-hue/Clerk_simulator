import pytest
from bureaucracy import Status, Document, Complaint, Application, Permit, Information, License

#testing if just document can be created
def test_document_creation():
    with pytest.raises(TypeError):
        Document("Olive", "Document")

#checking devault values
def test_initial_values():
    doc = Complaint("Olive", "Grand theft beverage")
    assert doc.status == Status.PENDING
    assert doc.notes == ""
    assert str(doc) == "[Complaint] Subject: 'Grand theft beverage' | Submitter: Olive | Status: Pending"

    