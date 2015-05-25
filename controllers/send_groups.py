from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCompleter, QListView, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtCore import QUrl, QSize
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
        self.ui.lstPhotos.setViewMode(QListView.IconMode)
        self.ui.lstPhotos.setGridSize(QSize(200, 200))
        self.ui.lstPhotos.setIconSize(QSize(150, 150))
        self.ui.lstPhotos.setFlow(QListView.LeftToRight)
        self.ui.lstPhotos.setSelectionMode(QListView.MultiSelection)
        
        self.__networkManager = QNetworkAccessManager()
        self.__networkManager.finished.connect(self.__process_network_response)
        self.__items_dict = {}


    def __process_network_response(self, reply):
        list_item = self.__items_dict[reply]
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll(), "jpg")
        list_item.setIcon(QIcon(pixmap))


    def slotItemClicked(self):
        row = self.ui.tblPthotos.currentItem().row()
        currenttext = self.ui.editPhotoID.text()
        newtext = self.ui.tblPthotos.item(row, 1).text()
        if currenttext == "":
            self.ui.editPhotoID.setText(newtext)
        else:
            self.ui.editPhotoID.setText(currenttext+','+newtext)


    def __on_btnLoadPhotos_clicked(self):
        pictures = self.vk_client.get_pictures(self.ui.editAlbumID.text())['items']

        print(pictures)

        for i, item in enumerate(pictures):
            url = QUrl(item['photo_604'])
            list_item = QListWidgetItem(item['text'])
            list_item.photo = item
            reply = self.__networkManager.get(QNetworkRequest(url))
            self.__items_dict[reply] = list_item
            self.ui.lstPhotos.addItem(list_item)


    def __on_btn_send_clicked(self):
        group_id = int(self._get_group_id(self.ui.editGroupIds.text()))
        message = self.ui.editMessage.text()
        time_out = int(self.ui.editTimeOut.text())

        photos = []

        for list_item in self.ui.lstPhotos.selectedItems():
            photos.append('photo{0}_{1}'.format(list_item.photo['owner_id'], list_item.photo['id']))


        self.logger.debug('Sending messages to %s msg: %s, with time out: %s sec', group_id, message, time_out)
        self.vk_client.comment_every_post(group_id, message, time_out, ','.join(photos))

        self.logger.debug('Succesfully sent messages to target group!')
        self.ui.lblStatus.setText("Sent message to target group" + '\n' + message)


    def _get_group_id(self, str):
        return groups_manager.get_group_id(str)
