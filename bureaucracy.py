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