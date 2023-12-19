from enum import Enum


class UsersError(str, Enum):
    NO_ERRORS = 'no errors'
    NO_CHANGES_MADE = 'no changes made'
    USER_WITH_USERNAME_ALREADY_EXISTS = 'username already exists'
    USER_WITH_EMAIL_ALREADY_EXISTS = 'email already exists'
    USER_ID_NOT_EXISTS = 'user with specified ID does not exist'
    MISSING_PARAMS = 'missing parameter'
    EMPTY_LIST_OF_PARAMS = 'empty list of params'


INTERNAL_ERROR = 'internal error'

USER_ID = 'user_id'
USERNAME = 'username'
USER_FIRST_NAME = 'first_name'
USER_LAST_NAME = 'last_name'
USER_EMAIL = 'email'
USER_PASSWORD = 'password'
USER_IMAGE = 'image'
USER_PROFILE_IMAGE_URL = 'profile_image_url'

AVAILABLE_PARAMETERS = [USERNAME, USER_FIRST_NAME, USER_LAST_NAME, USER_EMAIL, USER_PASSWORD,
                        USER_IMAGE, USER_PROFILE_IMAGE_URL]
