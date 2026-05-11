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
        