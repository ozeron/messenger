from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

class SendGroupsDialog(QWidget):
  def __init__(self, client):
    QWidget.__init__(self)
    self.vk_client = client
    self.ui = loadUi('uis/send_groups.ui', self)
    self.ui.btnSend.clicked.connect(self.__on_btn_send_clicked)

  def __on_btn_send_clicked(self):
    group_id = self.ui.editGroupIds.text()
    self.vk_client.comment_every_post(int(group_id), "Hello from GUI!")
    self.ui.lblMessage.setText('Hello There!' + '\n'+ str)