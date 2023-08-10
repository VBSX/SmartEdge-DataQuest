
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy
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
        self.setWindowTitle("Inicio")
        self.resize(500, 500)
        self.setStyleSheet("padding :15px;background-color: #000000;color: #FFFFFF;font-size: 17px; ")
        self.button_db_default_config = QPushButton("Configuração padrão DB")
        self.button_db_default_config.clicked.connect(self.update_db)
        
        self.config_button = QPushButton("Config")
        self.config_button.clicked.connect(self.start_config)
        
        self.button_reset_users_password = QPushButton("Resetar senha de usuários")
        self.button_reset_users_password.clicked.connect(self.reset_users_password)
        
        
        self.button_style_config(self.button_reset_users_password)
        self.button_style_config(self.config_button)
        self.button_style_config(self.button_db_default_config)
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()
        central_widget.setLayout(layout_principal)
        layout_principal.addWidget(self.button_db_default_config)
        layout_principal.addWidget(self.button_reset_users_password)
        layout_principal.addItem(self.spacer)
        layout_principal.addWidget(self.config_button)
        
        
    
    def button_style_config(self, button):
        button.setStyleSheet("background-color: #FFFFFF;color: #000000;border-radius: 10px;")
        button.setCursor(Qt.PointingHandCursor)
    
    def update_db(self):
        if self.file_handler.verify_if_json_exists():
            query_return = self.db.db_default_config()
            if query_return =='sucess':
                self.show_dialog("Configuração realizada com sucesso")
            else:
                self.show_dialog(str(query_return))
        else:
            self.show_dialog("Configuração ainda não realizada")
    
    def reset_users_password(self):
        query_return = self.db.reset_users_password()
        if query_return =='sucess':
            self.show_dialog("Senhas resetadas com sucesso")
        else:
            self.show_dialog(str(query_return))
    
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