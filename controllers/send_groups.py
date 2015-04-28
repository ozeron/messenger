from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtWidgets import QCompleter
from PyQt5.uic import loadUi

from messenger import logger
from messenger import groups_manager

class SendGroupsDialog(QWidget):
  def __init__(self, client):
    QWidget.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = client
    self.ui = loadUi('uis/send_groups.ui', self)
    self.ui.btnSend.clicked.connect(self.__on_btn_send_clicked)
    self.ui.btnLoadPhotos.clicked.connect(self.__on_btnLoadPhotos_clicked)
    completer = QCompleter(groups_manager.get_group_names(), self)
    self.ui.editGroupIds.setCompleter(completer)


  def __on_btnLoadPhotos_clicked(self):
    self.ui.tblPthotos.setColumnCount(2)
    self.ui.tblPthotos.setHorizontalHeaderLabels(['Text', 'ID'])
    self.ui.tblPthotos.horizontalHeader().setStretchLastSection(True)
    self.ui.tblPthotos.horizontalHeader().resizeSection(0, 200)

    pictures = self.vk_client.get_pictures(self.ui.editAlbumID.text())['items']

    for i, item in enumerate(pictures):
        self.ui.tblPthotos.setRowCount(i + 1)
        self.ui.tblPthotos.setItem(i, 0, QTableWidgetItem(item['text']))
        self.ui.tblPthotos.setItem(i, 1, QTableWidgetItem('photo{0}_{1}'.format(str(item['owner_id']), str(item['id']))))

  def __on_btn_send_clicked(self):
    group_id = int(self._get_group_id(self.ui.editGroupIds.text()))
    message = self.ui.editMessage.text()
    time_out = int(self.ui.editTimeOut.text())
    self.logger.debug('Sending messages to %s msg: %s, with time out: %s sec', group_id, message, time_out)
    picture = self.ui.editPhotoID.text()
    self.vk_client.comment_every_post(group_id, message, time_out, picture)

    self.logger.debug('Succesfully sent messages to target group!')
    self.ui.lblStatus.setText("Sent message to target group" + '\n' + message)

  def _get_group_id(self, str):
      return groups_manager.get_group_id(str)
