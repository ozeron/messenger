from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox,QAbstractItemView
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtGui import QBrush, QColor
from messenger import logger
from messenger import groups_manager

class SelectGroupsDialog(QWidget):
  def __init__(self, vk_client):
    QWidget.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = loadUi('uis/select_groups.ui', self)
    self.ui.btnSearch.clicked.connect(self.__on_search_btn_clicked)
    self.ui.btnAdd.clicked.connect(self.__on_add_btn_clicked)
    self.ui.btnRemove.clicked.connect(self.__on_delete_btn_clicked)
    self.grid = self.ui.vwvGroups
    self.grid.setEditTriggers( QTableWidget.NoEditTriggers )

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


  def __on_search_btn_clicked(self):
    city = self.ui.editCity.text()
    search_query = self.ui.editQuery.text()
    quantity = int(self.ui.editQuanity.text())
    groups = self.vk_client.vk_messenger.get_top_n_groups_by_location(city, quantity, search_query)
    self.logger.debug('Searching groups top %s in %s with search query %s ', quantity, city, search_query)
    self.grid.setSelectionBehavior(QAbstractItemView.SelectRows);
    self.grid.setColumnCount(2)
    self.grid.setHorizontalHeaderLabels(['Name', 'ID'])
    self.grid.horizontalHeader().setStretchLastSection(True)
    self.grid.horizontalHeader().resizeSection(0, 300)

    for i, group in enumerate(groups):
      self.grid.setRowCount(i + 1)
      self.grid.setItem(i, 0, QTableWidgetItem(group['name']))
      self.grid.setItem(i, 1, QTableWidgetItem(str(group['id'])))
      if groups_manager.already_in_favourites(group['id'], group['name']):
          self._highlite_row(i, self._highlite_brush())
    self.logger.debug('Succesfully searched!')

  def _double_click_on_group(self, group):
      name, id = self._get_group_data(group)

      if groups_manager.already_in_favourites(id.text(), name.text()):
          self._remove_group_from_favourites(group)
      else:
          self._add_group_to_favourites(group)

  def _remove_group_from_favourites(self, group):
      name, id = self._get_group_data(group)
      groups_manager.remove_from_favourites(id.text(), name.text())
      self._highlite_row(name.row(), self._white_brush())
      self.logger.debug("Receive to remove from favourites! '%s' id: '%s'" % (name.text(), id.text()))


  def _add_group_to_favourites(self, group):
      assert (self.grid.columnCount() == 2), "Grid should be size 2"
      name, id = self._get_group_data(group)
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
