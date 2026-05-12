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

#checking if complain will be approved when there is a complainant
def test_complainant_true():
    doc = Complaint("Olive", "Party noise", complainant=True)
    doc.verify()
    assert doc.status == Status.APPROVED

#checking if complain will be approved when there is no complainant
def test_complainant_false():
    doc = Complaint("Olive", "Party noise", complainant=False)
    doc.verify()
    assert doc.status == Status.REJECTED
    assert doc.notes == "Complainant must be specified"

#checking if application will be approved with attachements
def test_attachments_true():
    doc = Application("Larry", "Scholarship", attachments=True)
    doc.verify()
    assert doc.status== Status.APPROVED

#checking if application will be approved without attachements
def test_attachments_false():
    doc = Application("Larry", "Scholarship", attachments=False)
    doc.verify()
    assert doc.status== Status.REVISION
    assert doc.notes == "Missing required attachements"

#checking if permit will be approved with fee paid and low/medium danger level
def test_fee_paid_correct_danger():
    for level in ["low", "medium"]:
        doc = Permit("Sofi", "House building", fee_paid=True, danger_level=level)
        doc.verify()
        assert doc.status == Status.APPROVED

#checking if permit will be approved if fee is not paid
def test_fee_paid_false():
    for level in ["low", "medium"]:
        doc = Permit("Sofi", "House building", fee_paid=False, danger_level=level)
        doc.verify()
        assert doc.status == Status.REVISION
        assert doc.notes == "Fee is not paid"

#checking if permit will be approved with high level danger
def test_fee_paid_hight_danger():
    doc = Permit("Sofi", "Chemical factory", fee_paid=True, danger_level="high")
    doc.verify()
    assert doc.status == Status.REJECTED
    assert doc.notes == "High danger premit"

#checking if permit will be approved with invalid level danger
def test_fee_paid_invalid_danger():
    doc = Permit("Sofi", "Chemical factory", fee_paid=True, danger_level="super")
    doc.verify()
    assert doc.status == Status.REVISION
    assert doc.notes == "Invalid danger level"

#checking if infirmation will be given when its public/not secret
def test_information_not_secret():
    doc = Information("Eden", "History", secret=False)
    doc.verify()
    assert doc.status == Status.APPROVED

#checking if infirmation will be given when its secret, but with clearence
def test_information_secret_clearence_true():
    doc = Information("Eden", "Murder", secret=True, clearance=True)
    doc.verify()
    assert doc.status == Status.APPROVED

#checking if infirmation will be given when its secret, but without clearence
def test_information_secret_clearance_false():
    doc = Information("Eden", "Murder", secret=True, clearance=False)
    doc.verify()
    assert doc.status == Status.REJECTED
    assert doc.notes == "No clearance for required documents"

#checking if license will be approved if type of business and area correct
def test_business_approved_area_valid():
    doc = License("Iris", "Beauty Salon", business_approved=True, area=True)
    doc.verify()
    assert doc.status == Status.APPROVED

#checking if license will be approved if type of business is correct, bus area not
def test_business_approved_area_invalid():
    doc = License("Iris", "Club", business_approved=True, area=False)
    doc.verify()
    assert doc.status == Status.REJECTED
    assert doc.notes == "Connot open business in this area"

#checking if license will be approved if type of business is nor approved, bus area correct
def test_business_not_approved_area_valid():
    doc = License("Iris", "Club", business_approved=False, area=True)
    doc.verify()
    assert doc.status == Status.REVISION
    assert doc.notes == "Business type that is not in the approved list"