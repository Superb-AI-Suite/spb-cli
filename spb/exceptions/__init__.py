import logging


class CustomBaseException(Exception):
    def __init__(self, message, code=None):
        super(CustomBaseException, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.message = message
        self.code = code

    def __str__(self):
        return f"[{self.code}] {self.message}"


class SDKException(CustomBaseException):
    def __init__(self, message, code="001000"):
        super(SDKException, self).__init__(message, code)


class ParameterException(SDKException):
    def __init__(self, message, code="001001"):
        super(ParameterException, self).__init__(message, code)


class NotSupportedException(SDKException):
    def __init__(self, message, code="001002"):
        super(NotSupportedException, self).__init__(message, code)


class ImmutableValueChangeException(SDKException):
    def __init__(self, message, code="001003"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class AttributeTypeException(SDKException):
    def __init__(self, message, code="001004"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class CommandInitiationFailedException(SDKException):
    def __init__(self, message, code="001005"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class ResourceIsNotExistedException(SDKException):
    def __init__(self, message, code="001006"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class ModelInitiationFailedException(SDKException):
    def __init__(self, message, code="001007"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class SDKInitiationFailedException(SDKException):
    def __init__(self, message, code="001008"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class ImageDoesNotExistsException(SDKException):
    def __init__(self, message, code="001009"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class TypeInitiationFailedException(SDKException):
    def __init__(self, message, code="001010"):
        super().__init__(message, code)


class AttributeNameException(SDKException):
    def __init__(self, message: str = None, code="001011"):
        super().__init__(message, code)


class DoesNotExistsAttribute(SDKException):
    def __init__(self, message: str = None, code="001012"):
        super().__init__(message, code)


class NotImplementedException(SDKException):
    def __init__(self, message: str = None, code="001013"):
        super().__init__(message, code)


class QueryTypeException(SDKException):
    def __init__(self, message: str = None, code="001014"):
        super().__init__(message, code)


class ClientCustomException(SDKException):
    def __init__(self, message, code="001015"):
        super().__init__(message, code)


class APIException(CustomBaseException):
    def __init__(self, message, code="002000"):
        super(APIException, self).__init__(message, code)


class BadRequestException(APIException):
    def __init__(self, message, code="002400"):
        super().__init__(message, code)


class APIFormatException(APIException):
    def __init__(self, message, code="002400"):
        super().__init__(message, code)

class UnauthorizedException(APIException):
    def __init__(self, message, code="002401"):
        super().__init__(message, code)


class AuthenticateFailedException(APIException):
    def __init__(self, message, code="002401"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class ForbiddenException(APIException):
    def __init__(self, message, code="002403"):
        super().__init__(message, code)


class NotFoundException(APIException):
    def __init__(self, message, code="002404"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class ConflictException(APIException):
    def __init__(self, message, code="002409"):
        super().__init__(message, code)


class APILimitExceededException(APIException):
    def __init__(self, message="API Call limit exceeded.", code="002429"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class APIUnknownException(APIException):
    def __init__(self, message, code="002500"):
        super().__init__(message, code)
        # self.logger.error(message, code)


class NotAvailableServerException(APIException):
    def __init__(self, message, code="002503"):
        super().__init__(message, code)
        # self.logger.error(message, code)