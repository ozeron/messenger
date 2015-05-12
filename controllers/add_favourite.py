from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QBrush, QColor

from messenger import logger
from messenger import groups_manager
import sys

class AddFavourite(QDialog):
  def __init__(self, vk_client):
    QDialog.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = loadUi('uis/add_favourite.ui', self)
    self.ui.buttonBox.accepted.connect(self.__on_add_btn_clicked)

  def __on_add_btn_clicked(self):
    self.logger.debug("Add new group clicked!")
    group_id = self.ui.edit.text()
    name = self.vk_client.get_group_name(group_id)
    status, msg = self.__try_add_new_group_to_favourites(group_id, name)
    if status:
      self.accept()
    else:
      self.__showText(msg)
    return 0

  def __try_add_new_group_to_favourites(self, group_id, name):
    self.logger.debug("Adding group %s with %s" % (str(name), str(group_id)))
    #try:
    groups_manager.add_favourite_group(group_id, name)
    #except:
    #     e = sys.exc_info()[0]
    #     self.logger.debug("Error: %s" % e)
    #     return False, e
    # else:
    return True, "Success"

  def __showText(self, msg):
      self.ui.lblStatus.setText(str(msg))

