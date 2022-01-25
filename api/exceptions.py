from rest_framework.exceptions import APIException


class NotCarUser(APIException):
    status_code = 403
    default_detail = "Missing credentials: You are not a user " "of this car"
    default_code = "cannot_retrieve_car"


class NotUser(APIException):
    status_code = 403
    default_detail = (
        "Missing credentials: You are not allowed " "to access this user profile"
    )
    default_code = "cannot_retrieve_user"


class NoPairBrandModel(APIException):
    status_code = 400
    default_detail = "Bad Request: Car model not available for this brand"
    default_code = "cannot_pair_brand_and_model"


class CannotCreateOrEditCarForSuperUserOrAnotherAdmin(APIException):
    status_code = 403
    default_detail = "Missing Credentials: Cannot create or edit a car for superuser or another admin"
    default_code = "cannot_create_or_edit_car_for_superuser_or_another_admin"


class CannotCreateCarForAnotherUser(APIException):
    status_code = 403
    default_detail = "Missing Credentials: Cannot create a car for another user"
    default_code = "cannot_create_car_for_another_user"
