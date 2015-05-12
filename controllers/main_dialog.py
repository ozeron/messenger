from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

from controllers.send_groups import SendGroupsDialog
from controllers.select_groups import SelectGroupsDialog
from controllers.favourite_groups import FavouriteGroupsDialog
from messenger import logger

class MainDialog(QWidget):
  def __init__(self, vk_client):
    QWidget.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = loadUi('uis/main_dialog.ui', self)
    self.ui.btnSelectGroups.clicked.connect(self.__on_select_groups_btn_clicked)
    self.ui.btnSengGroups.clicked.connect(self.__on_seng_groups_btn_clicked)
    self.ui.btnAddGroups.clicked.connect(self.__on_add_groups_btn_clicked)

  def __on_select_groups_btn_clicked(self):
    dialog = SelectGroupsDialog(self.vk_client)
    dialog.show()

  def __on_seng_groups_btn_clicked(self):
    dialog = SendGroupsDialog(self.vk_client)
    self.logger.debug("Created SendGroupsDialog")
    dialog.show()

  def __on_add_groups_btn_clicked(self):
    dialog = FavouriteGroupsDialog(self.vk_client)
    self.logger.debug("Created FavouriteGroups")
    dialog.show()