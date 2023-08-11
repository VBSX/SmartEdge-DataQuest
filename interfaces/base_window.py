from PySide6.QtWidgets import QMainWindow, QMessageBox
import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from components.filehandle import File
from components.dbhandle import Database
 
class BaseWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        self.db = Database()
        self.file_handler = File()

    def setup_ui(self):
        self.setWindowTitle("Base Window")
           
    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)
        