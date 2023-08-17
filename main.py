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
        self.img_mycommerce_path = r'images/mycommerce.png'
        self.img_config_path = r'images/config.png'
        self.img_about_path = r'images/about.png'
        self.img_smartedge_path = r'images/smartedge.png'
        self.img_pin_path = r'images/pin.png'
        self.setup_ui()
        
    def setup_ui(self):
        has_image_folder = self.file_handler.verify_if_images_path_exists()
        if not has_image_folder:
            self.icon_close_mycommerce = QIcon(self.resource_path(self.img_mycommerce_path))
            self.icon_config = QIcon(self.resource_path(self.img_config_path))
            self.icon_about = QIcon(self.resource_path(self.img_about_path))
            self.icon_pin = QIcon(self.resource_path(self.img_pin_path))
            self.setWindowIcon(QIcon(self.resource_path(self.img_smartedge_path)))
        else:
            self.icon_close_mycommerce = QIcon(self.img_mycommerce_path)
            self.icon_config = QIcon(self.img_config_path)
            self.icon_about = QIcon(self.img_about_path)
            self.icon_pin = QIcon(self.img_pin_path)
            self.setWindowIcon(QIcon(self.img_smartedge_path))
            
        self.setWindowTitle("SmartEdge - DataQuest")
        self.resize(500, 500)
        self.setStyleSheet("padding :15px;background-color: #000000;color: #FFFFFF;font-size: 17px; ")
        self.get_configs()

        self.layout_horizontal_config_program = QHBoxLayout()
        self.layout_horizontal_close_programs = QHBoxLayout()
        self.all_buttons()
        self.layout_horizontal_config_program.addWidget(self.config_button)
        self.layout_horizontal_config_program.addWidget(self.button_about_program) 
        
        self.label_close_programs = QLabel()
        self.label_close_programs.setText("Fechar programas")

        self.layout_horizontal_close_programs.addWidget(self.label_close_programs)
        self.layout_horizontal_close_programs.addWidget(self.button_close_mycommerce)
        
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.host_label = QLabel()
        self.host_label.setText(f"Host: {self.host}")
        
        self.port_label = QLabel()
        self.port_label.setText(f"Porta: {self.port}")
        
        self.database_label = QLabel()
        self.database_label.setText(f"Database: {self.database}")
              
        self.layout_config()
    
    def layout_config(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        self.layout_horizontal = QHBoxLayout()

        self.central_widget.setLayout(self.layout_principal)
        
        self.layout_principal.addWidget(self.button_pin)
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
    
    def window_fixed(self):
        window_fixed = False
        if not window_fixed:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            window_fixed = True
        else:
            self.setWindowFlags(~Qt.WindowStaysOnTopHint)
            window_fixed = False
        self.show()
     
    def all_buttons(self):
        #
        self.button_pin = self.create_button(
            config_style=False,
            function=self.window_fixed
            )
        self.button_pin.setIcon(QIcon(self.icon_pin))
        self.button_pin.setIconSize(QSize(32,32))
        self.button_pin.setFixedSize(32,32)
        #
        self.button_db_default_config = self.create_button(
            text="Configuração padrão DB",
            function=self.update_db
            )
        self.config_button = self.create_button(
            config_style=False,
            text="Config",
            function=self.start_config
            )
        self.config_button.setIcon(QIcon(self.icon_config))
        self.config_button.setIconSize(QSize(64,64))
        #
        self.button_about_program = self.create_button(
            config_style=False,
            function=self.about_program_window
            )
        self.button_about_program.setIcon(QIcon(self.icon_about))
        self.button_about_program.setIconSize(QSize(64,64))
        self.button_about_program.setFixedSize(64,64)
        #
        self.button_reset_users_password = self.create_button(
            text="Resetar senha de usuários",
            function=self.reset_users_password
            )
        #
        self.button_close_mycommerce = self.create_button(
            config_style=False,
            function=self.mycommerce_close
            )
        self.button_close_mycommerce.clicked.connect(self.mycommerce_close)
        self.button_close_mycommerce.setIcon(QIcon(self.icon_close_mycommerce))    
        self.button_close_mycommerce.setIconSize(QSize(64,64))
        self.button_close_mycommerce.setFixedSize(64,64)
        #
        self.query_button = self.create_button(
            text="Iniciar uma Query",
            function=self.start_query
            )
        
        
    def create_button(self,config_style=True, text=None, function=None  ):
        button = QPushButton()
        if text:
            button.setText(text)
        if function:
            button.clicked.connect(function) 
        if config_style == True:
            button.setStyleSheet("background-color: #FFFFFF;color: #000000;border-radius: 10px;")
        button.setCursor(Qt.PointingHandCursor)
        return button
    
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