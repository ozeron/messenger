from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDateTime
from PyQt5.uic import loadUi

class MainDialog(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.ui = loadUi('main_dialog.ui', self)
		self.ui.btnTest.clicked.connect(self.__on_test_btn_clicked)
	
	def __on_test_btn_clicked(self):
		self.ui.lblMessage.setText('Hello There!' + '\n'+ QDateTime.currentDateTime().toString())
