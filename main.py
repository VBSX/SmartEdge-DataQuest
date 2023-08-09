
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setStyleSheet("padding :15px;background-color: #000000;color: #FFFFFF ")
        self.button_db_default_config = QPushButton("Configuração padrão DB")
        self.button_db_default_config.clicked.connect(self.db.db_default_config)
        self.config_button = QPushButton("Config")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button_db_default_config)
        self.layout.addWidget(self.config_button)
        self.setLayout(self.layout)
        
        
    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)
        
if __name__ == "__main__": 
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()