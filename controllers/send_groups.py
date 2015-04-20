from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

from messenger import logger

class SendGroupsDialog(QWidget):
  def __init__(self, client):
    QWidget.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = client
    self.ui = loadUi('uis/send_groups.ui', self)
    self.ui.btnSend.clicked.connect(self.__on_btn_send_clicked)

  def __on_btn_send_clicked(self):
    group_id = int(self.ui.editGroupIds.text())
    message = self.ui.editMessage.text()
    time_out = int(self.ui.editTimeOut.text())
    self.logger.debug('Sending messages to %s msg: %s, with time out: %s sec', group_id, message, time_out)
    self.vk_client.comment_every_post(group_id, message, time_out)
    self.logger.debug('Succesfully sent messages to target group!')
    self.ui.lblStatus.setText("Sent message to target group" + '\n'+ message)