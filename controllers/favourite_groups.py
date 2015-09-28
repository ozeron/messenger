from PyQt5.QtWidgets import QWidget, QDialog, QTableWidgetItem, QTableWidget, QMessageBox,QAbstractItemView
from PyQt5.QtCore import QObject
from PyQt5.uic import loadUi
from PyQt5.QtGui import QBrush, QColor
from messenger import logger
from messenger import groups_manager
from controllers.add_favourite import AddFavourite

class FavouriteGroupsDialog(QObject):
  def __init__(self, vk_client, ui):
    QObject.__init__(self)
    self.logger = logger.get(__name__)
    self.vk_client = vk_client
    self.ui = ui
    self.ui.btnAddFavourites.clicked.connect(self.__on_add_btn_clicked)
    self.ui.btnDelete.clicked.connect(self.__on_delete_btn_clicked)
    self.grid = self.ui.fGroupsList
    self.grid.setEditTriggers( QTableWidget.NoEditTriggers )
    self.show_favourites()

  def show_favourites(self):
    self.grid.setColumnCount(2)
    self.grid.setHorizontalHeaderLabels(['Name', 'ID'])
    self.grid.setSelectionBehavior(QAbstractItemView.SelectRows);
    self.grid.horizontalHeader().setStretchLastSection(True)
    self.grid.horizontalHeader().resizeSection(0, 300)
    self._clear_table();
    self._fill_table_with_data();


  def __on_add_btn_clicked(self):
    dialog = AddFavourite(self.vk_client)
    self.logger.debug("Created SendGroupsDialog")
    if dialog.exec() == QDialog.Accepted:
        self.logger.debug("Dialog done!")
        self._clear_table()
        self._fill_table_with_data()
    else:
        self.logger.debug("Dialog cancel!")

  def __on_delete_btn_clicked(self):
      rows = self.grid.selectionModel().selectedRows()
      if len(rows) > 0:
          self._delete_rows(rows)
      else:
          self._display_error("Select groups to delete!")

  def _delete_rows(self, list):
      self.logger.debug("Trying to delete %s" % str(list))
      for i in range(len(list)):
          item = list.pop()
          row = item.row()
          name = self.grid.item(row, 0).text()
          id = self.grid.item(row, 1).text()
          groups_manager.remove_from_favourites(id,name)
          self.grid.removeRow(row)

  def _display_error(self, msg):
      self.logger.debug(msg)
      QMessageBox(QMessageBox.Warning, "Error!", msg).exec()


  def _fill_table_with_data(self):
    groups = groups_manager.get_groups()
    for i, group in enumerate(groups):
      self.grid.setRowCount(i + 1)
      self.grid.setItem(i, 0, QTableWidgetItem(group['name']))
      self.grid.setItem(i, 1, QTableWidgetItem(str(group['id'])))


  def _clear_table(self):
    while self.grid.rowCount() > 0:
        self.grid.removeRow(0)
    self.logger.debug("Table cleared")
