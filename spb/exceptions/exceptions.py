import logging

class CustomBaseException(Exception):
    def __init__(self, message, code=None):
        super(CustomBaseException, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.message = message
        self.code = code


class SDKException(CustomBaseException):
    def __init__(self, message, code='200400'):
        super(SDKException, self).__init__(message, code)


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

class APIUnknowException(APIException):
  def __init__(self, message, code='200003'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class ClientCustomException(SDKException):
  def __init__(self, message, code = '000000'):
    super().__init__(message, code)


class CustomAPIException(APIException):
  def __init__(self, message, code='000001'):
    super().__init__(message, code)


class ImmutableValueChangeException(SDKException):
  def __init__(self, message, code = '100000'):
    super().__init__(message, code)
    # self.logger.error(message, code)


class AttribureTypeException(SDKException):
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

class ImageIsNotExistsException(SDKException):
  def __init__(self, message, code = '100006'):
    super().__init__(message, code)
    # self.logger.error(message, code)