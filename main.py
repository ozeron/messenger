import sys
import os
import json

from PyQt5.QtWidgets import *

from messenger.client import VkClient
from messenger import logger
from controllers.main_dialog import MainDialog


# TODO: add quequ adding
# Token reqeust
# https://oauth.vk.com/authorize?client_id=4841859&scope=266240&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.33&response_type=token
logger = logger.get(__name__)


def start():
    if len(sys.argv) > 1:
      path = sys.argv[1]
    text = open(CREDENTIALS_PATH, 'r').read()
    client = get_client(json.loads(text))
    start_app_with(client)

def get_client(json):
    entry = json[0]
    logger.info("Loaded credentials building VkClient with {0}".format(str(entry)))
    client = VkClient(entry)
    return client

def start_app_with(client):
    a = QApplication([])
    main_dialog = MainDialog(client)
    logger.debug("Created MainDialog")
    main_dialog.show()
    a.exec()

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'config/credentials.json')

if __name__ == '__main__':
  start()
