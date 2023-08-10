
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
    QSizePolicy,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from dbhandle import Database
import sys
from filehandle import File
from query_run import QueryWindow
from configwindow import ConfigWindow
from os_handle import OsHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.db = Database()
        self.file_handler = File()
        self.config_window = None
        self.host = self.file_handler.host
        self.port = self.file_handler.port
        self.database = self.file_handler.database
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
        
        self.button_close_mycommerce = QPushButton("Fechar o mycommerce")
        self.button_close_mycommerce.clicked.connect(self.mycommerce_close)
        
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.query_button = QPushButton("Iniciar uma Query")
        self.query_button.clicked.connect(self.start_query) 
        
        self.host_label = QLabel()
        self.host_label.setText(f"Host: {self.host}")
        
        self.port_label = QLabel()
        self.port_label.setText(f"Porta: {self.port}")
        
        self.database_label = QLabel()
        self.database_label.setText(f"Database: {self.database}")
        
        self.button_style_config(self.query_button)
        self.button_style_config(self.button_reset_users_password)
        self.button_style_config(self.config_button)
        self.button_style_config(self.button_db_default_config)
        self.button_style_config(self.button_close_mycommerce)
        self.button_style_config(self.query_button)
                  
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.layout_horizontal = QHBoxLayout()

        self.central_widget.setLayout(self.layout_principal)
        
        self.layout_principal.addWidget(self.button_db_default_config)
        self.layout_principal.addWidget(self.button_reset_users_password)
        self.layout_principal.addItem(self.spacer)
        self.layout_principal.addWidget(self.button_close_mycommerce)
        self.layout_principal.addWidget(self.query_button)
        self.layout_principal.addItem(self.spacer)
        self.layout_principal.addWidget(self.config_button)
        
        self.layout_horizontal.addWidget(self.host_label)
        self.layout_horizontal.addWidget(self.port_label)
        self.layout_horizontal.addWidget(self.database_label)
        
        self.layout_principal.addLayout(self.layout_horizontal)
    
    def reset_layout(self):
        self.centralWidget().setParent(None)
        self.clearLayout(self.layout_principal)
        self.clearLayout(self.layout_horizontal)
        json_file = self.file_handler.read_json()
        self.host = json_file['host']
        self.port = self.file_handler.port
        self.database = self.file_handler.database
        print(self.database)
        self.setup_ui()
    
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
    
    def mycommerce_close(self):
        process = OsHandler().kill_mycommerce_process()
        self.show_dialog(str(process))
        
    def start_query(self):
        self.query_window = QueryWindow(self)
        self.query_window.show()
    
    def start_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()

    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)
        
    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child.layout())  
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()