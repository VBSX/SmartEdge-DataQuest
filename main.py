
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget
)
from PySide6.QtCore import Qt
from dbhandle import Database
import sys
from filehandle import File

from configwindow import ConfigWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.db = Database()
        self.file_handler = File()
        self.config_window = None
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("padding :15px;background-color: #000000;color: #FFFFFF ")
        self.button_db_default_config = QPushButton("Configuração padrão DB")
        self.button_db_default_config.clicked.connect(self.update_db)
        self.config_button = QPushButton("Config")
        self.config_button.clicked.connect(self.start_config)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()
        central_widget.setLayout(layout_principal)
        layout_principal.addWidget(self.button_db_default_config)
        layout_principal.addWidget(self.config_button)
        
    def update_db(self):
        if self.file_handler.verify_if_json_exists():
            
            self.db.db_default_config()
        else:
            self.show_dialog("Configuração ainda não realizada")
    
    def start_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()
    
    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)
        
if __name__ == "__main__": 
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()