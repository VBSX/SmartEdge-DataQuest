from PySide6.QtWidgets import QMainWindow, QMessageBox
import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from components.filehandle import File
from components.dbhandle import Database
from PySide6.QtCore import Qt

class BaseWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        self.db = Database()
        self.file_handler = File()
        
    def close_at_esc(self, event):
        if event.key() == Qt.Key_Escape:
            self.close() 
             
    def setup_ui(self):
        self.setWindowTitle("Base Window")
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)  

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child.layout())  
        
    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)
        