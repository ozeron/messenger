from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox,QAbstractItemView
from PyQt5.QtCore import QDateTime, QVariant, QTimer, Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QBrush, QColor
from messenger import logger, groups_manager

class SelectGroupsDialog(QWidget):
	
  def __init__(self, vk_client):
    QWidget.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = loadUi('uis/select_groups.ui', self)
    self.grid = self.ui.vwvGroups
    self.__init_timers()
    self.__init_lists()
    self.__init_connections()
    
  def __init_lists(self):
    self.ui.selectCountry.clear()
    self.ui.selectCountry.addItem("Россия", QVariant(1))
    self.ui.selectCountry.addItem("Украина", QVariant(2))
    self.__on_new_country_selected(0)
    
  def __init_timers(self):
    self.reloadTimer = QTimer()
    self.reloadTimer.setSingleShot(True)
    self.reloadTimer.setInterval(1000)
    self.reloadTimer.timeout.connect(self.__reload_groups_list)
    self.scrollTimer = QTimer()
    self.scrollTimer.setSingleShot(True)
    self.scrollTimer.setInterval(500)
    self.scrollTimer.timeout.connect(self.__load_more_groups)
    
  def __init_connections(self):
    self.ui.btnAdd.clicked.connect(self.__on_add_btn_clicked)
    self.ui.btnRemove.clicked.connect(self.__on_delete_btn_clicked)
    self.ui.selectCountry.currentIndexChanged.connect(self.__on_new_country_selected)
    self.ui.selectCity.editTextChanged.connect(self.__on_city_select_edittext_changed)
    self.ui.selectCity.currentIndexChanged.connect(self.__on_query_text_changed)
    self.ui.vwvGroups.verticalScrollBar().valueChanged.connect(self.__on_groups_slider_move)
    self.ui.editQuery.textChanged.connect(self.__on_query_text_changed)
    self.ui.vwvGroups.cellDoubleClicked.connect(self.__on_double_click_on_group)
    
  def __load_more_groups(self):
	  self.__populate_groups_list(20)
    
  def __reload_groups_list(self):
    while (self.grid.rowCount() != 0):
      self.grid.removeRow(0)
    self.__load_more_groups()
    
  def __on_query_text_changed(self, query):
    self.scrollTimer.stop()
    self.reloadTimer.start()
    
  def __on_groups_slider_move(self, current):
    self.scrollTimer.start()
    
  def __on_new_country_selected(self, index):
    self.ui.selectCity.clear()
    self.__on_city_select_edittext_changed("")
    self.ui.selectCity.setCurrentIndex(0)
        
  def __on_city_select_edittext_changed(self, string):
    if self.ui.selectCity.findText(string, flags = Qt.MatchStartsWith) != -1:
      return

    countryId = self.ui.selectCountry.itemData(self.ui.selectCountry.currentIndex())
    suggestedCity = self.vk_client.vk_messenger.get_top_n_cities_by_country_and_name_with_offset(countryId, string, 20)
    
    if (suggestedCity['count'] == 0):
      return
      
    temporal_block = self.ui.selectCity.blockSignals(True)
    self.ui.selectCity.clear()      
    for city in suggestedCity['items']:
      self.ui.selectCity.addItem(city['title'], QVariant(city['id']))
    self.ui.selectCity.setCurrentText(string)
    self.ui.selectCity.blockSignals(temporal_block)

  def __on_add_btn_clicked(self):
    rows = self.ui.grid.selectionModel().selectedRows()
    if len(rows) > 0:
        self.__add_rows(rows)
    else:
        self._display_error("Select groups to add!")

  def __add_rows(self, list):
    self.logger.debug("Trying to add %s" % str(list))
    for i in range(len(list)):
        item = list.pop()
        row = item.row()
        name = self.grid.item(row, 0).text()
        id = self.grid.item(row, 1).text()
        groups_manager.add_favourite_group(id,name)
        self._highlite_row(item.row(), self._highlite_brush())

  def __delete_rows(self, list):
    self.logger.debug("Trying to delete %s" % str(list))
    for i in range(len(list)):
        item = list.pop()
        row = item.row()
        name = self.grid.item(row, 0).text()
        id = self.grid.item(row, 1).text()
        groups_manager.remove_from_favourites(id,name)
        self._highlite_row(item.row(), self._white_brush())

  def __on_delete_btn_clicked(self):
    rows = self.ui.grid.selectionModel().selectedRows()
    if len(rows) > 0:
      self.__delete_rows(rows)
    else:
        self._display_error("Select groups to delete!")
	  
  def __populate_groups_list(self, count):
    cId = self.ui.selectCity.itemData(self.ui.selectCity.currentIndex())
    search_query = self.ui.editQuery.text()
    if not search_query:
      return
    groups = self.vk_client.vk_messenger.get_top_n_groups_by_location(cId, count, search_query, self.ui.vwvGroups.rowCount())
	  
    for group in groups:
      self.grid.insertRow(self.grid.rowCount())
      self.grid.setItem(self.grid.rowCount()-1, 0, QTableWidgetItem(group['name']))
      self.grid.setItem(self.grid.rowCount()-1, 1, QTableWidgetItem(str(group['id'])))
      if groups_manager.already_in_favourites(group['id'], group['name']):
          self._highlite_row(grid.rowCount()-1, self._highlite_brush())
    self.logger.debug('Succesfully searched!')
	
  def __on_double_click_on_group(self, row):
    name = self.grid.item(row,0)
    id = self.grid.item(row,1)
    
    if groups_manager.already_in_favourites(id.text(), name.text()):
      self._remove_group_from_favourites(name, id)
    else:
      self._add_group_to_favourites(name, id)

  def _remove_group_from_favourites(self, name, id):
      groups_manager.remove_from_favourites(id.text(), name.text())
      self._highlite_row(name.row(), self._white_brush())
      self.logger.debug("Receive to remove from favourites! '%s' id: '%s'" % (name.text(), id.text()))


  def _add_group_to_favourites(self, name, id):
      assert (self.grid.columnCount() == 2), "Grid should be size 2"
      self._highlite_row(name.row(), self._highlite_brush())
      self.logger.debug("Receive add group to favourites! '%s' id: '%s'" % (name.text(), id.text()))
      groups_manager.add_favourite_group(id.text(), name.text())

  def _get_group_data(self, item):
      row = int(item.row())
      name = self.grid.item(row,0)
      id = self.grid.item(row, 1)
      return (name, id)

  def _highlite_row(self,row, color = None):
      if not color:
          color = self._highlite_brush()
      for i in range(self.grid.columnCount()):
          self.grid.item(row,i).setBackground(color)

  def _highlite_brush(self):
      # RGB: #495B85
      return QColor(73,91,133)

  def _white_brush(self):
      return QColor(255,255,255)

  def _display_error(self, msg):
    self.logger.debug(msg)
    QMessageBox(QMessageBox.Warning, "Error!", msg).exec()
