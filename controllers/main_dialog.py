from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

from controllers.send_groups import SendGroupsDialog
from controllers.select_groups import SelectGroupsDialog
from controllers.favourite_groups import FavouriteGroupsDialog
from controllers.config import ConfigDialog
from messenger import logger

class MainDialog(QMainWindow):
  def __init__(self, vk_client):
    QMainWindow.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = loadUi('uis/onewindow.ui', self)
    self.ui.mainTab.setCurrentIndex(0)
    self.ui.mainTab.currentChanged.connect(self.__on_tab_changed)

  def __on_tab_changed(self, id):
      try:
          self.controller = [
              None, FavouriteGroupsDialog,
              SelectGroupsDialog, SendGroupsDialog,
              None
              ][id](self.vk_client, self.ui)
      except TypeError:
          pass

  def __on_select_groups_btn_clicked(self):
    dialog = SelectGroupsDialog(self.vk_client, self.ui)
    dialog.show()

  def __on_seng_groups_btn_clicked(self):
    dialog = SendGroupsDialog(self.vk_client)
    self.logger.debug("Created SendGroupsDialog")
    dialog.show()

  def __on_add_groups_btn_clicked(self):
    dialog = FavouriteGroupsDialog(self.vk_client)
    self.logger.debug("Created FavouriteGroups")
    dialog.show()

  def guiExceptionHook(self, excType, excValue, tracebackobj):
      self.ui.statusbar.showMessage(str(excValue))
