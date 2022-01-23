from rest_framework.exceptions import APIException


class NotCarUser(APIException):
    status_code = 403
    default_detail = (
        "Missing credentials: You are not a user "
        "of this car"
    )
    default_code = "cannot_retrieve_car"


class NotUser(APIException):
    status_code = 403
    default_detail = (
        "Missing credentials: You are not allowed "
        "to access this user profile"
    )
    default_code = "cannot_retrieve_user"
