import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QHBoxLayout,
)
import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from interfaces.query_run_window import QueryWindow
from interfaces.configwindow import ConfigWindow
from components.os_handle import OsHandler
from interfaces.base_window import BaseWindow
from interfaces.aboutwindow import  AboutProgramWindow

class MainWindow(BaseWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.config_window = None
        self.about_window_is_open = False
        
        self.setup_ui()
        
    def setup_ui(self):
        has_image_folder = self.file_handler.verify_if_images_path_exists()
        img_mycommerce_path = r'images/mycommerce.png'
        img_config_path = r'images/config.png'
        img_about_path = r'images/about.png'
        img_smartedge_path = r'images/smartedge.png'
        if not has_image_folder:
            icon_close_mycommerce = QIcon(self.resource_path(img_mycommerce_path))
            icon_config = QIcon(self.resource_path(img_config_path))
            icon_about = QIcon(self.resource_path(img_about_path))
            self.setWindowIcon(QIcon(self.resource_path(img_smartedge_path)))
        else:
            icon_close_mycommerce = QIcon(img_mycommerce_path)
            icon_config = QIcon(img_config_path)
            icon_about = QIcon(img_about_path)
            self.setWindowIcon(QIcon(img_smartedge_path))
        self.setWindowTitle("SmartEdge - DataQuest")
        self.resize(500, 500)
        self.setStyleSheet("padding :15px;background-color: #000000;color: #FFFFFF;font-size: 17px; ")
        self.get_configs()
        self.button_db_default_config = QPushButton("Configuração padrão DB")
        self.button_db_default_config.clicked.connect(self.update_db)
        
        self.layout_horizontal_config_program = QHBoxLayout()
        self.config_button = QPushButton("Config")
        self.config_button.clicked.connect(self.start_config)
        self.config_button.setIcon(QIcon(icon_config))
        self.config_button.setIconSize(QSize(64,64))

        self.layout_horizontal_config_program.addWidget(self.config_button)
        
        self.about_program = QPushButton()
        self.about_program.clicked.connect(self.about_program_window)
        self.about_program.setIcon(QIcon(icon_about))
        self.about_program.setIconSize(QSize(64,64))
        self.about_program.setFixedSize(64,64)
        self.layout_horizontal_config_program.addWidget(self.about_program) 
        
        
        self.button_reset_users_password = QPushButton("Resetar senha de usuários")
        self.button_reset_users_password.clicked.connect(self.reset_users_password)
        
        self.layout_horizontal_close_programs = QHBoxLayout()
        self.label_close_programs = QLabel()
        self.label_close_programs.setText("Fechar programas")
        
        self.button_close_mycommerce = QPushButton()
        self.button_close_mycommerce.clicked.connect(self.mycommerce_close)
        self.button_close_mycommerce.setIcon(QIcon(icon_close_mycommerce))    
        self.button_close_mycommerce.setIconSize(QSize(64,64))
        self.button_close_mycommerce.setFixedSize(64,64)
        
        self.layout_horizontal_close_programs.addWidget(self.label_close_programs)
        self.layout_horizontal_close_programs.addWidget(self.button_close_mycommerce)
        
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
        # self.button_style_config(self.config_button)
        self.button_style_config(self.button_db_default_config)
        self.button_style_config(self.query_button)
                  
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.layout_horizontal = QHBoxLayout()

        self.central_widget.setLayout(self.layout_principal)
        
        self.layout_principal.addWidget(self.button_db_default_config)
        self.layout_principal.addWidget(self.button_reset_users_password)
        self.layout_principal.addItem(self.spacer)
        self.layout_principal.addLayout(self.layout_horizontal_close_programs)
        self.layout_principal.addWidget(self.query_button)
        self.layout_principal.addItem(self.spacer)
        self.layout_principal.addLayout(self.layout_horizontal_config_program)
        
        self.layout_horizontal.addWidget(self.host_label)
        self.layout_horizontal.addWidget(self.port_label)
        self.layout_horizontal.addWidget(self.database_label)
        
        self.layout_principal.addLayout(self.layout_horizontal)
    
    def reset_layout(self):
        self.centralWidget().setParent(None)
        self.clearLayout(self.layout_principal)
        self.clearLayout(self.layout_horizontal)
        self.setup_ui()
    
    def button_style_config(self, button):
        button.setStyleSheet("background-color: #FFFFFF;color: #000000;border-radius: 10px;")
        button.setCursor(Qt.PointingHandCursor)
    
    def update_db(self):
        # TODO
        # quando inicia com a porta do banco errada ele so diz
        # que o banco esta desconectado
        if self.file_handler.verify_if_json_exists():
            query_return = self.db.db_default_config()
            if query_return == 'sucess':
                self.show_dialog("Configuração realizada com sucesso")
            else:
                self.show_dialog(str(query_return))
        else:
            self.show_dialog("Configuração ainda não realizada")
    
    def reset_users_password(self):
        query_return = self.db.reset_users_password()
        if query_return == 'sucess':
            self.show_dialog("Senhas resetadas com sucesso")
        else:
            self.show_dialog(str(query_return))
    
    def mycommerce_close(self):
        process = OsHandler().kill_mycommerce_process()
        self.show_dialog(str(process))
        
    def start_query(self):
        has_connection = self.db.start_connection()
        if has_connection:
            self.query_window = QueryWindow(self)
            self.query_window.show()
        else:
            self.show_dialog(str(self.db.message_connection_error))
            
    def start_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()


    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child.layout())  
    
    def get_configs(self):
        json_file = self.file_handler.read_json()
        self.host = json_file['host']
        self.port = json_file['port']
        self.database = json_file['database']
    
    def about_program_window(self):
        if not self.about_window_is_open:
            self.about_window = AboutProgramWindow(self)
            self.about_window.show()
            self.about_window_is_open = True
        else:
            self.about_window.close()
            self.about_window.show()
                


if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()