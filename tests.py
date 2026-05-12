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

#checking of complain will be approved when there is a complainant
def test_complainant_true():
    doc = Complaint("Olive", "Party noise", complainant=True)
    doc.verify()
    assert doc.status == Status.APPROVED

#checking of complain will be approved when there is no complainant
def test_complainant_false():
    doc = Complaint("Olive", "Party noise", complainant=False)
    doc.verify()
    assert doc.status == Status.REJECTED
    assert doc.notes == "Complainant must be specified"