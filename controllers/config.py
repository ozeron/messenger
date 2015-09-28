# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import pyqtSlot as Slot, QObject
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from messenger import config


class ConfigDialog(QObject):
    def __init__(self, client, ui):
        QObject.__init__(self)
        self.vk_client = client
        self.ui = ui
        data = json.loads(open(config.CREDENTIALS_PATH, 'r').read())[0]
        ui.cLineLogin.setText(data['login'])
        ui.cLinePassword.setText(data['password'])
        ui.cLineKey.setText(data['access_token'])
