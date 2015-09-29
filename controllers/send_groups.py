from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCompleter, QListView, QListWidgetItem,QMessageBox, QCheckBox, QHeaderView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QSize, QObject
from PyQt5.uic import loadUi

from messenger import logger
from messenger import groups_manager
from controllers.select_photos import SelectPhotosDialog


class SendGroupsDialog(QObject):
    def __init__(self, client, ui):
        QObject.__init__(self)
        self.logger = logger.get(__name__)
        self.vk_client = client
        self.ui = ui
        self.ui.btnSend.clicked.connect(self.__on_btn_send_clicked)
        self.__show_favourites()
        self.ui.tableGroups.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.tableGroups.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.lineFilter.textChanged.connect(self.__on_filter_text_changed)
        self.userId = self.vk_client.get_userId()
        self.icon_size = QSize(150,150)
        self.null_pix = QPixmap("nothumb").scaled(self.icon_size)
        self.ui.photo1.setPixmap(self.null_pix)
        self.ui.photo2.setPixmap(self.null_pix)
        self.ui.btnSend.clicked.connect(self.__on_btn_send_clicked)
        self.ui.btnChangePhoto1.clicked.connect(self.__on_btnChangePhoto1_clicked)
        self.ui.btnChangePhoto2.clicked.connect(self.__on_btnChangePhoto2_clicked)
        self.net_manager = QNetworkAccessManager()
        self.net_manager.finished.connect(self._photo_loaded)
        self.selected_photo1 = {}
        self.selected_photo2 = {}
        self.photo_to_change = 0

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

    def slotItemClicked(self):
        row = self.ui.tblPthotos.currentItem().row()
        currenttext = self.ui.editPhotoID.text()
        newtext = self.ui.tblPthotos.item(row, 1).text()
        if currenttext == "":
            self.ui.editPhotoID.setText(newtext)
        else:
            self.ui.editPhotoID.setText(currenttext + ',' + newtext)

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
        if 'id' in self.selected_photo1:
            photos.append('photo{0}_{1}'.format(self.userId, self.selected_photo1['id']))
        if 'id' in self.selected_photo2:
            photos.append('photo{0}_{1}'.format(self.userId, self.selected_photo2['id']))

        self.logger.debug('Sending messages to %s msg: %s, with time out: %s sec', group_id, message, time_out)
        self.vk_client.comment_every_post(group_id, message, time_out, ','.join(photos))

        self.logger.debug('Succesfully sent messages to target group!')
        self.ui.lblStatus.setText("Sent message to target group" + '\n' + message)

    def __on_btn_send_clicked(self):
        try:
            self.ui.statusbar.showMessage("Sending!")
            self.ui.btnSend.setEnabled(False)
            names = self.__get_selected_groups()
            if len(names) == 0:
                self._display_error("Select Groups to send!")
                self.ui.btnSend.setEnabled(True)
                return False
            for name in names:
                self.__send_over_group(name)

        finally:
            self.ui.btnSend.setEnabled(True)

    def _display_error(self, msg):
      self.logger.debug(msg)
      QMessageBox(QMessageBox.Warning, "Error!", msg).exec()

    def __on_btnChangePhoto1_clicked(self):
        self.photo_to_change = 1
        self.__goto_photoSelection()

    def __on_btnChangePhoto2_clicked(self):
        self.photo_to_change = 2
        self.__goto_photoSelection()

    def __goto_photoSelection(self):
        dialog = SelectPhotosDialog(self.vk_client,self)
        self.logger.debug("Created SelectPhotos")
        dialog.show()

    def _get_photo(self,result,caller):
      caller.destroy()
      if result['album_id'] == -7:
          result['album_id'] = 'wall'
      elif result['album_id'] == -6:
          result['album_id'] = 'profile'
      elif result['album_id'] == -15:
          result['album_id'] = 'saved'
      photo = self.vk_client.get_photo(result['album_id'],result['photo_id'])
      reply = self.net_manager.get(QNetworkRequest(QUrl(photo['photo_604'])))
      if self.photo_to_change == 1:
        self.selected_photo1['reply'] = reply
        self.selected_photo1['id'] = str(result['photo_id'])
      else:
        self.selected_photo2['reply'] = reply
        self.selected_photo2['id'] = str(result['photo_id'])

    def _photo_loaded(self,reply):
        pix = QPixmap()
        pix.loadFromData(reply.readAll(), "jpg")
        if 'reply' in self.selected_photo1 :
            if reply == self.selected_photo1['reply']:
                self.ui.photo1.setPixmap(pix.scaled(self.icon_size))
                return
        if 'reply' in self.selected_photo2 :
             if reply == self.selected_photo2['reply']:
                self.ui.photo2.setPixmap(pix.scaled(self.icon_size))
