from abc import ABC, abstractmethod
from enum import Enum

class Status(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    REVISION = "Revision"

class Document(ABC):
    def __init__(self, submitter, subject, signed=None, notes=""):
        self.submitter = submitter
        self.subject = subject
        self.signed = signed
        self.notes = notes
        self.status = Status.PENDING

    @abstractmethod
    def verify(self):
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] Subject: '{self.subject} | Submitter: {self.submitter} | Status: {self.status.value}"
        
class Complaint(Document):
    def __init__(self, submitter, subject, complainant=True, **kwargs):
        super().__init__(submitter, subject, **kwargs)
        self.complainant = complainant

    def verify(self):
        if self.complainant:
            self.status = Status.APPROVED
        else:
            self.status = Status.REJECTED
            self.notes = "Complainant must be specified"

class Application(Document):
    def __innit__(self, submitter, subject, attachments=False, **kwargs):
        super().__init__(submitter, subject, **kwargs)
        self.attachments = attachments

    def verify(self):
        if self.attachments:
            self.status = Status.APPROVED
        else:
            self.status = Status.REVISION
            self.notes = "Missing required attachements"

class Permit(Document):
    def __init__(self, submitter, subject, fee_paid=False, danger_level="Low", **kwargs):
        super().__init__(submitter, subject, **kwargs)
        self.fee_paid = fee_paid
        self.danger_level = danger_level.lower()

    def verify(self):
        if not self.fee_paid:
            self.status = Status.REVISION
            self.notes = "Fee is not paid"
            return
        if self.danger_level == "High":
            self.status = Status.REJECTED
            self.notes = "High danger premit"
        elif self.danger_level in ["Low", "Medium"]:
            self.status = Status.APPROVED
        else:
            self.status = Status.REVISION
            self.notes = "Invalid danger level"

class Information(Document):
    def __init__(self, submitter, subject, secret=False, clearance=False, **kwargs):
        super().__init__(submitter, subject, **kwargs)
        self.secret = secret
        self.clearance = clearance

    def verify(self):
        if not self.secret:
            self.status = Status.APPROVED
        elif self.secret and self.clearance:
            self.status = Status.APPROVED
        else:
            self.status = Status.REJECTED
            self.notes = "No clearance for required documents"

class License(Document):
    def __init__(self, submitter, subject, business_approved=False, area=False, **kwargs):
        super().__init__(submitter, subject, **kwargs)
        self.business_approved = business_approved
        self.area = area

    def verify(self):
        if self.business_approved and self.area:
            self.status = Status.APPROVED
        elif not self.area:
            self.status = Status.REJECTED
            self.notes = "Connot open business in this area"
        elif not self.business_approved:
            self.status = Status.REVISION
            self.notes = "Business type that is not in the approved list"
