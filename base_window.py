from PySide6.QtWidgets import QMainWindow, QMessageBox
from filehandle import File
from dbhandle import Database
 
class BaseWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        self.db = Database()
        self.file_handler = File()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Base Window")
           
    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)
        