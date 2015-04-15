import sys
import os
import json

from PyQt5.QtWidgets import *

from messenger.client import VkClient
from messenger import logger
from controllers.main_dialog import MainDialog



# TODO: add quequ adding
# Token reqeust https://oauth.vk.com/authorize?client_id=4841859&scope=6274559&redirect_uri=https://oauth.vk.com/blank.html&%20display=page&v=5.29&%20response_type=token

logger = logger.get(__name__)

def init(json):
    entry = json[0]
    logger.info("Loaded credentials building VkClient with {0}".format(str(entry)))
    client = VkClient(entry)
    return client

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'config/credentials.json')

if __name__ == '__main__':
  if len(sys.argv) > 1:
    path = sys.argv[1]
  text = open(CREDENTIALS_PATH, 'r').read()
  json = json.loads(text)

  a = QApplication([])
  main_dialog = MainDialog()
  main_dialog.show()
  a.exec()
  #init(json)
