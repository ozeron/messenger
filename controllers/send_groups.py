from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCompleter, QListView, QListWidgetItem,QMessageBox, QCheckBox, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSize, QObject
from PyQt5.uic import loadUi

from messenger import logger
from messenger import groups_manager


class SendGroupsDialog(QObject):
    def __init__(self, client, ui):
        QObject.__init__(self)
        self.logger = logger.get(__name__)
        self.vk_client = client
        self.ui = ui
        self.ui.btnSend.clicked.connect(self.__on_btn_send_clicked)
        self.ui.btnLoadPhotos.clicked.connect(self.__on_btnLoadPhotos_clicked)
        self.ui.lstPhotos.setViewMode(QListView.IconMode)
        self.ui.lstPhotos.setGridSize(QSize(200, 200))
        self.ui.lstPhotos.setIconSize(QSize(150, 150))
        self.ui.lstPhotos.setFlow(QListView.LeftToRight)
        self.ui.lstPhotos.setSelectionMode(QListView.MultiSelection)
        self.__show_favourites()
        self.__networkManager = QNetworkAccessManager()
        self.__networkManager.finished.connect(self.__process_network_response)
        self.__items_dict = {}
        self.ui.tableGroups.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tableGroups.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.lineFilter.textChanged.connect(self.__on_filter_text_changed)

    def __show_favourites(self):
        names = groups_manager.get_groups()
        T = self.ui.tableGroups
        while (T.rowCount() != 0):
          T.removeRow(0)
        for name in names:
            T.insertRow(0)
            T.setCellWidget(0, 0, QCheckBox())
            T.setItem(0, 1, QTableWidgetItem(name['name']))
            T.setItem(0, 2, QTableWidgetItem(str(name['id'])))

    def __on_filter_text_changed(self, text):
        text = text.strip().lower()
        for i in range(self.ui.tableGroups.rowCount()):
            if not text in self.ui.tableGroups.item(i, 1).text().lower():
                self.ui.tableGroups.setRowHidden(i, True)
            else:
                self.ui.tableGroups.setRowHidden(i, False)

        self.__get_selected_groups()

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

    def __get_selected_groups(self):
        names = []
        T = self.ui.tableGroups
        for row in range(T.rowCount()):
            if not T.isRowHidden(row) and T.cellWidget(row, 0).isChecked():
                names.append([T.item(row, 1).text(), int(T.item(row, 2).text())])
        print(names)
        return names

    def __send_over_group(self,name):
        group_id = name[1]
        message = self.ui.msMessageEdit.toPlainText()
        if len(message) == 0:
            self._display_error("Enter message to send!")
            return

        time_out = self.ui.msTimeoutEdit.value()
        if time_out <= 0:
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
            self.ui.statusbar.showMessage("Sending!")
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
