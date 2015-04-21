from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

from messenger import logger


class SelectGroupsDialog(QWidget):
  def __init__(self, vk_client):
    QWidget.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = loadUi('uis/select_groups.ui', self)
    self.ui.btnSearch.clicked.connect(self.__on_search_btn_clicked)

  def __on_search_btn_clicked(self):
    city = self.ui.editCity.text()
    search_query = self.ui.editQuery.text()
    quantity = int(self.ui.editQuanity.text())
    groups = self.vk_client.vk_messenger.get_top_n_groups_by_location(city, quantity, search_query)
    self.logger.debug('Searching groups top %s in %s with search query %s ', quantity, city, search_query)

    self.ui.vwvGroups.setColumnCount(2)
    self.ui.vwvGroups.setHorizontalHeaderLabels(['Name', 'ID'])
    self.ui.vwvGroups.horizontalHeader().setStretchLastSection(True)
    self.ui.vwvGroups.horizontalHeader().resizeSection(0, 300)

    for i, group in enumerate(groups):
      self.ui.vwvGroups.setRowCount(i + 1)
      self.ui.vwvGroups.setItem(i, 0, QTableWidgetItem(group['name']))
      self.ui.vwvGroups.setItem(i, 1, QTableWidgetItem(str(group['id'])))

    self.logger.debug('Succesfully searched!')
