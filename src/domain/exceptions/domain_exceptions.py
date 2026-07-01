class DomainException(Exception):
    pass

class PatientNotFound(DomainException):
    pass

class ExamNotFound(DomainException):
    pass

class ReportNotFound(DomainException):
    pass

class UserNotFound(DomainException):
    pass

class UnauthorizedAccess(DomainException):
    pass

class InvalidCredentials(DomainException):
    pass

class DuplicateCPF(DomainException):
    pass
