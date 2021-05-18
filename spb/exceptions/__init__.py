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
    def __init__(self, message, code='200400'):
        super(SDKException, self).__init__(message, code)


class ParameterException(SDKException):
  def __init__(self, message, code='200401'):
    super(ParameterException, self).__init__(message, code)


class APIException(CustomBaseException):
    def __init__(self, message, code='200500'):
        super(APIException, self).__init__(message, code)


class AuthenticateFailedException(APIException):
  def __init__(self, message, code='200001'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class APILimitExceededException(APIException):
  def __init__(self, message ='API Call limit exceeded.', code='200002'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class APIUnknownException(APIException):
  def __init__(self, message, code='200003'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class NotFoundException(APIException):
  def __init__(self, message, code='200004'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class ClientCustomException(SDKException):
  def __init__(self, message, code = '000000'):
    super().__init__(message, code)


class CustomAPIException(APIException):
  def __init__(self, message, code='000001'):
    super().__init__(message, code)


class APIFormatException(APIException):
  def __init__(self, message, code='000002'):
    super().__init__(message, code)


class ImmutableValueChangeException(SDKException):
  def __init__(self, message, code = '100000'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class AttributeTypeException(SDKException):
  def __init__(self, message, code = '100001'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class CommandInitiationFailedException(SDKException):
  def __init__(self, message, code = '100002'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class ResourceIsNotExistedException(SDKException):
  def __init__(self, message, code = '100003'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class ModelInitiationFailedException(SDKException):
  def __init__(self, message, code = '100004'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class SDKInitiationFailedException(SDKException):
  def __init__(self, message, code = '100005'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class ImageDoesNotExistsException(SDKException):
  def __init__(self, message, code = '100006'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class TypeInitiationFailedException(SDKException):
  def __init__(self, message, code = '100007'):
    super().__init__(message, code)


class AttributeNameException(SDKException):
  def __init__(self, message: str = None, code = '100008'):
    super().__init__(message, code)


class DoesNotExistsAttribute(SDKException):
  def __init__(self, message: str = None, code = '100009'):
    super().__init__(message, code)


class NotImplementedException(SDKException):
  def __init__(self, message: str = None, code = '100010'):
    super().__init__(message, code)


class QueryTypeException(SDKException):
  def __init__(self, message: str = None, code = '100008'):
    super().__init__(message, code)