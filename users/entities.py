from utils import (USER_ID, USER_FIRST_NAME, USER_LAST_NAME, USERNAME, USER_EMAIL, USER_PASSWORD,
                   USER_PROFILE_IMAGE_URL)


class User(object):
    def __init__(self, params):
        self.user_id = params.get(USER_ID)
        self.first_name = params.get(USER_FIRST_NAME)
        self.last_name = params.get(USER_LAST_NAME)
        self.username = params.get(USERNAME)
        self.email = params.get(USER_EMAIL)
        self.password = params.get(USER_PASSWORD)
        self.image_url = params.get(USER_PROFILE_IMAGE_URL)

    def set_image_url(self, image_url):
        self.image_url = image_url

    def set_user_id(self, user_id):
        self.user_id = user_id

    def to_json(self):
        self_dict = self.__dict__
        self_dict.pop(USER_PASSWORD)

        return self.__dict__
