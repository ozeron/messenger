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
    def comment_every_post(self, id, message):
        self.vk_messenger.comment_every_post(id, message)

