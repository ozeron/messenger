from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCompleter, QListView, QListWidgetItem,QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5 import QtCore
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
        self.ui.btnLoadAllPublicPhotos.clicked.connect(self.__on_btnLoadAllPublicPhotos_clicked)
        self.ui.lstPhotos.setViewMode(QListView.IconMode)
        self.ui.lstPhotos.setGridSize(QSize(200, 200))
        self.ui.lstPhotos.setIconSize(QSize(150, 150))
        self.ui.lstPhotos.setFlow(QListView.LeftToRight)
        self.ui.lstPhotos.setSelectionMode(QListView.MultiSelection)
        self.model = QStandardItemModel(self.ui.list)
        self.__show_favourites()
        self.__networkManager = QNetworkAccessManager()
        self.__networkManager.finished.connect(self.__process_network_response)
        self.__items_dict = {}

    def __show_favourites(self):
        names = groups_manager.get_group_names()
        for name in names:
            item = QStandardItem(name)
            item.setCheckable(True)
            self.model.appendRow(item)
        self.model.item(0).setCheckState(QtCore.Qt.Checked)
        self.ui.list.setModel(self.model)

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

    def __on_btnLoadAllPublicPhotos_clicked(self):
        self.logger.debug("Success");
        albums = self.vk_client.get_albums()['items']
        



    def __get_selected_groups(self):
        names = []
        model = self.ui.list.model()
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                names.append(item.text())
        return names

    def __send_over_group(self,name):
        group_id = int(groups_manager.get_group_id(name))
        message = self.ui.editMessage.text()
        if len(message) == 0:
            self._display_error("Select Groups to send!")
            return
        try:
            time_out = int(self.ui.editTimeOut.text())
        except:
            self._display_error("TimeOut must be a positive int!")
            return
        if time_out < 0:
            self._display_error("TimeOut must be a positive int!")
            return

        photos = []

        for list_item in self.ui.lstPhotos.selectedItems():
            photos.append('photo{0}_{1}'.format(list_item.photo['owner_id'], list_item.photo['id']))


        self.logger.debug('Sending messages to %s msg: %s, with time out: %s sec', group_id, message, time_out)
        self.vk_client.comment_every_post(group_id, message, time_out, ','.join(photos))

        self.logger.debug('Succesfully sent messages to target group!')
        self.ui.lblStatus.setText("Sent message to target group" + '\n' + message)

    def __on_btn_send_clicked(self):
        try:
            self.ui.lblStatus.setText("Sending!")
            self.ui.btnSend.setEnabled(False);
            names = self.__get_selected_groups()
            if len(names) == 0:
                self._display_error("Select Groups to send!")
                self.ui.btnSend.setEnabled(True);
                return False
            for name in names:
                self.__send_over_group(name)

        finally:
            self.ui.btnSend.setEnabled(True);

    def _display_error(self, msg):
      self.logger.debug(msg)
      QMessageBox(QMessageBox.Warning, "Error!", msg).exec()
