from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

from controllers.send_groups import SendGroupsDialog
from controllers.select_groups import SelectGroupsDialog


class MainDialog(QWidget):
  def __init__(self):
    QWidget.__init__(self)
    self.ui = loadUi('uis/main_dialog.ui', self)
    self.ui.btnSelectGroups.clicked.connect(self.__on_select_groups_btn_clicked)
    self.ui.btnSengGroups.clicked.connect(self.__on_seng_groups_btn_clicked)

  def __on_select_groups_btn_clicked(self):
    dialog = SelectGroupsDialog()
    dialog.show()

  def __on_seng_groups_btn_clicked(self):
    dialog = SendGroupsDialog()
    dialog.show()