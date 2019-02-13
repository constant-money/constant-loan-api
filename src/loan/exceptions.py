from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidVerificationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid verification'
    default_code = 'invalid_verification'


class AlreadyVerifiedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Already verified'
    default_code = 'already_verified'


class ExceedLimitException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Exceed limit'
    default_code = 'exceed_limit'


class AlreadyPaidException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Already paid'
    default_code = 'already_paid'


class InvalidStatusException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid status'
    default_code = 'invalid_status'


class AlreadyInAnotherApplicationException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Already in another application'
    default_code = 'already_in_another_application'


class InvalidEmailException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid email'
    default_code = 'invalid_email'


class DuplicatedEmailInFormException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Duplicated email in form'
    default_code = 'duplicated_email'
