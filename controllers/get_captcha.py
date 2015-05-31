import urllib
import PyQt5
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QCompleter, QListView, QListWidgetItem, QDialog
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtCore import QUrl, QSize
from PyQt5.uic import loadUi
import time

from messenger import logger





class GetCapthca(QDialog):
    def __init__(self, sid, url):
        QDialog.__init__(self)
        self.ui = loadUi('uis/captcha_dialog.ui', self)
        self.ui.btnOK.clicked.connect(self.__on_bntOK_clicked)
        self.ui.btnCancel.clicked.connect(self.__on_bntCancel_clicked)
        self.__get_picture(url)
        self.result = ''

    def __on_bntOK_clicked(self):
        self.result = self.ui.editCaptha.text()
        QDialog.close(self)
    def __on_bntCancel_clicked(self):
        self.result = False
        QDialog.close(self)
    def get_result(self):
        return self.result
    def __get_picture(self, url):
        data = urllib.request.urlopen(url).read()
        image = PyQt5.QtGui.QImage()
        image.loadFromData(data)
        self.ui.labelPhoto.setPixmap(PyQt5.QtGui.QPixmap(image))