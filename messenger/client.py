from messenger.messenger import VkMessenger
from messenger import logger

APP_ID = '4841859'

class VkClient:
    def __init__(self, credentials):
        self.logger = logger.get(__name__)
        config = {
            'app_id': APP_ID,
            'login': credentials['login'],
            'pass': credentials['password'],
            'token': credentials["access_token"]
        }
        self.logger.debug("Creating VkMessenger obj with config: " + str(config))
        self.vk_messenger = VkMessenger(config)
        self.logger.debug("VkMessenger Succesfully created!")

    def comment_every_post(self, id, message, time_out=None, photo=None):
        self.vk_messenger.comment_every_post(id, message, time_out, photo)

    def get_userId(self):
        return self.vk_messenger.get_userId()

    def get_albumData(self):
        return self.vk_messenger.get_albumData()

    def get_photos(self, album):
        return self.vk_messenger.get_photos(album)

    def get_allPhotos(self):
        return self.vk_messenger.get_allPhotos()

    def get_group_name(self, g_id):
        return self.vk_messenger.get_group_name(g_id)

    def get_photo(self,album_id,photo_id):
        return self.vk_messenger.get_photo(album_id,photo_id)