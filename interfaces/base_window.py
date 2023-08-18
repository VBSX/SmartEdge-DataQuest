from PySide6.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from components.filehandle import File
from components.dbhandle import Database
from webbrowser import open_new_tab 

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
                 
    def open_browser_link(self, link):
        open_new_tab(
        link
        )
    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)

    def create_button(self,config_style=True, text=None, function=None, icon=None, icon_size=None  ):
        button = QPushButton()
        if text:
            button.setText(text)
        if function:
            button.clicked.connect(function) 
        if config_style:
            button.setStyleSheet("background-color: #FFFFFF;color: #000000;border-radius: 10px;")
        if icon:
            button.setIcon(icon)
            if icon_size:
                button.setIconSize(QSize(icon_size,icon_size))
            else:
                button.setIconSize(QSize(64,64))
            if text:
                width = len(text)
                width = width*14
                print(width)
                button.setFixedSize(width+64,64)
            else:
                button.setFixedSize(64,64)
        button.setCursor(Qt.PointingHandCursor)
        return button
    
        