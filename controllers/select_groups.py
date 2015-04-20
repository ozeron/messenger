from PyQt5.QtWidgets import QWidget
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
    result = "Result:\n"
    i = 1
    for group in groups:
        result += str(i)+'. '+group['name']+'\t'+"id - "+str(group['id'])+'\n'
        self.ui.editResult.setText(result)
        i += 1
    self.logger.debug('Succesfully searched!')