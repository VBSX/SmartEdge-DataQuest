import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QHBoxLayout,
    QProgressDialog,
)
import gc
import sys
from PySide6.QtCore import Qt, QThread,Signal
from PySide6.QtGui import QIcon
from interfaces.query_run_window import QueryWindow
from interfaces.configwindow import ConfigWindow
from components.os_handle import OsHandler
from interfaces.base_window import BaseWindow
from interfaces.aboutwindow import  AboutProgramWindow
from components.last_version_finder import LatestVersion
from components.os_handle import OsHandler
from interfaces.interface_version_releaser import VersionReleaseInterface

class MainWindow(BaseWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.config_window = None
        self.about_window_is_open = False
        self.interface_version_relelaser_is_open = False
        self.interface_query_window_is_open = False
        
        self.img_mycommerce_path = r'images/mycommerce.png'
        self.img_config_path = r'images/config.png'
        self.img_about_path = r'images/about.png'
        self.img_smartedge_path = r'images/smartedge.png'
        self.img_pin_path = r'images/pin.png'
        self.img_att_path = r'images/att_db.png'
        self.is_the_window_fixed = False
        OsHandler()
        self.setup_ui()
        
    def setup_ui(self, reset_layout= False):
        if not reset_layout:
            self.config_imgs()
        self.setWindowTitle("SmartEdge - DataQuest")
        default_style = """
        QWidget {
            padding: 15px;
            background-color: #000000;
            color: #FFFFFF;
            font-size: 17px;
        }

        QComboBox ,QComboBox QAbstractItemView, QLineEdit {
            border:2px solid white;
            border-radius: 3px;
        }

        """
        self.setStyleSheet(default_style)
        self.get_configs()
        self.create_all_buttons_of_the_window()
        self.create_all_labels_of_the_window()
        
        self.layout_horizontal_buttons_sql = QHBoxLayout()
        self.layout_horizontal_buttons_sql.addWidget(self.button_db_default_config)
        self.layout_horizontal_buttons_sql.addWidget(self.button_reset_users_password)
        self.layout_horizontal_buttons_sql.addWidget(self.query_button)
        self.layout_horizontal_buttons_sql.addWidget(self.button_release_the_version)
        
        self.layout_horizontal_top_tools = QHBoxLayout()
        
        self.layout_horizontal_config_program = QHBoxLayout()
        self.layout_horizontal_close_programs = QHBoxLayout()
        

        self.layout_horizontal_top_tools.addWidget(self.button_pin)
        self.layout_horizontal_top_tools.addWidget(self.button_att_db)
        
        self.layout_horizontal_config_program.addWidget(self.config_button)
        self.layout_horizontal_config_program.addWidget(self.button_about_program) 

        self.layout_horizontal_close_programs.addWidget(self.label_close_programs)
        self.layout_horizontal_close_programs.addWidget(self.button_close_mycommerce)
        
        self.spacer = QSpacerItem(20,50)

        self.layout_horizontal_database_info = QHBoxLayout()
        self.layout_horizontal_database_info.addWidget(self.host_label)
        self.layout_horizontal_database_info.addWidget(self.port_label)
        self.layout_horizontal_database_info.addWidget(self.database_label) 
        
        self.layout_horizontal_downloads = QHBoxLayout()
        self.layout_horizontal_downloads.addWidget(self.label_last_build_version)
        self.layout_horizontal_downloads.addWidget(
            self.download_last_build_version_button)
        
        self.layout_horizontal_downloads.addWidget(self.label_last_release_version)
        self.layout_horizontal_downloads.addWidget(
            self.download_last_release_version_button)
        self.layout_config()
        
    def config_imgs(self):
        has_image_folder = self.file_handler.verify_if_images_path_exists()
        if not has_image_folder:
            self.icon_close_mycommerce = QIcon(self.resource_path(self.img_mycommerce_path))
            self.icon_config = QIcon(self.resource_path(self.img_config_path))
            self.icon_about = QIcon(self.resource_path(self.img_about_path))
            self.icon_pin = QIcon(self.resource_path(self.img_pin_path))
            self.icon_att_db = QIcon(self.resource_path(self.img_att_path))
            self.setWindowIcon(QIcon(self.resource_path(self.img_smartedge_path)))
        else:
            self.icon_close_mycommerce = QIcon(self.img_mycommerce_path)
            self.icon_config = QIcon(self.img_config_path)
            self.icon_about = QIcon(self.img_about_path)
            self.icon_pin = QIcon(self.img_pin_path)
            self.icon_att_db = QIcon(self.img_att_path)
            self.setWindowIcon(QIcon(self.img_smartedge_path))
          
    def layout_config(self):
        list_of_widgets = [
            self.layout_horizontal_top_tools,
            self.layout_horizontal_buttons_sql,
            self.layout_horizontal_close_programs,
            self.spacer,
            self.layout_horizontal_downloads,
            self.spacer,
            self.layout_horizontal_config_program,
            self.layout_horizontal_database_info
            ]
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        
        for item in list_of_widgets:

            if type(item) == QHBoxLayout:
                self.layout_principal.addLayout(item)
            elif type(item) == QSpacerItem:
                self.layout_principal.addItem(item)
            else:
                self.layout_principal.addWidget(item)
                
        self.central_widget.setLayout(self.layout_principal)      
                    
    def reset_layout(self):
        self.centralWidget().destroy()
        self.clearLayout(self.layout_principal)
        self.clearLayout(self.layout_horizontal_database_info)
        self.setup_ui(reset_layout=True)
        # Coletar lixo manualmente
        gc.collect() 
            
    def window_fixed(self):
        if not self.is_the_window_fixed:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.is_the_window_fixed = True
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.is_the_window_fixed = False
        self.show()
     
    def create_all_buttons_of_the_window(self):
        #
        self.button_pin = self.create_button(
            config_style=False,
            function=self.window_fixed,
            icon=self.icon_pin,
            icon_size = 32
            )
        self.button_pin.setFixedSize(32,32)
        #
        self.button_att_db = self.create_button(
            config_style=False,
            function=self.att_db_open,
            icon=self.icon_att_db,
            icon_size = 32)
        self.button_att_db.setFixedSize(32,32)
        #
        self.button_db_default_config = self.create_button(
            text="Configuração DB padrão",
            function=self.update_db
            )
        self.config_button = self.create_button(
            config_style=False,
            text="Config",
            function=self.start_config,
            icon= self.icon_config
            )
        #
        self.button_about_program = self.create_button(
            config_style=False,
            function=self.about_program_window,
            icon=self.icon_about
            )
        #
        self.button_reset_users_password = self.create_button(
            text="Resetar senha dos usuários",
            function=self.reset_users_password
            )
        #
        self.button_close_mycommerce = self.create_button(
            config_style=False,
            function=self.mycommerce_close,
            icon=self.icon_close_mycommerce
            )
        #
        self.query_button = self.create_button(
            text="Iniciar uma Query",
            function=self.start_query
            )
        self.download_last_build_version_button = self.create_button(
            text="Baixar última Build",
            function=self.download_last_build_version
        )
        self.download_last_release_version_button = self.create_button(
            text="Baixar última Release",
            function=self.download_last_release_version
        )
        self.button_release_the_version = self.create_button(
            text="Liberar a versão",
            function=self.release_the_version
        )
             
    def update_db(self):
        self.get_configs()
        if self.file_handler.verify_if_json_exists():
            query_return = self.db.db_default_config()
            if query_return == 'sucess':
                self.show_dialog("Configuração realizada com sucesso")
            else:
                self.show_dialog(str(query_return))
        else:
            self.show_dialog("Configuração ainda não realizada")
        self.reset_layout()
    
    def reset_users_password(self):

        query_return = self.db.reset_users_password()
        if query_return == 'sucess':
            self.show_dialog("Senhas resetadas com sucesso")
        else:
            self.show_dialog(str(query_return))
        self.reset_layout()
    
    def mycommerce_close(self):
        process = OsHandler().kill_mycommerce_process()
        self.show_dialog(str(process))
        
    def start_query(self):
        if not self.interface_query_window_is_open:
            self.get_configs()
            has_connection = self.db.start_connection()
            if has_connection:
                self.query_window = QueryWindow(self)
                self.query_window.show()
            else:
                self.show_dialog(str(self.db.message_connection_error))
            self.reset_layout()
            self.interface_query_window_is_open = True
        else:  
            self.query_window.show()
            
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
    

    def create_all_labels_of_the_window(self):
        self.host_label = self.create_label(f"Host: {self.host}")
        
        self.port_label = self.create_label(f"Porta: {self.port}")
        
        self.database_label = self.create_label(f"Database: {self.database}")
        
        self.label_close_programs = self.create_label("Fechar programas")
        
        self.label_last_build_version = self.create_label(f"Última Build: {LatestVersion().latest_build_version_text()}")
        # self.label_last_build_version.mouseDoubleClickEvent.connect(lambda: self.copy_to_clipboard(LatestVersion().latest_build_version_text()))
        
        self.label_last_release_version = self.create_label(f"Última Release: {LatestVersion().latest_release_version_text()}")
        # self.label_last_release_version.clicked.connect(lambda: self.copy_to_clipboard(LatestVersion().latest_release_version_text()))
    
    def att_db_open(self):
        self.get_configs()
        os.startfile("C:\Visual Software\MyCommerce\AtualizarDB.exe")
        self.reset_layout()
    
    def download_last_build_version(self):
        self.download_version(
            "Baixando a última Build", is_build=True)
        
    def download_last_release_version(self):
        self.download_version(
            "Baixando a última Release...", is_build=False)

    def download_version(self, text, is_build):
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setWindowTitle("Download")
        self.progress_dialog.setLabelText(text)
        self.progress_dialog.setRange(0, 0)
        
        self.download_thread = DownloadThread(is_build)
        self.download_thread.download_finished.connect(self.download_finished)
        self.download_thread.start()
        self.reset_layout()
        
        if is_build:
            self.download_last_release_version_button.setEnabled(False)
            self.download_last_release_version_button.setEnabled(True)  
        else:
            self.download_last_release_version_button.setEnabled(False)
            self.download_last_release_version_button.setEnabled(True)  
            
    def download_finished(self):
        self.progress_dialog.cancel()
        if LatestVersion().latest_build_version_text() != 'SemBuild':
            self.show_dialog('Arquivo enviado para a pasta de downloads')
        else:
            self.show_dialog('Não há build para baixar')

    def release_the_version(self):
        if not self.interface_version_relelaser_is_open:
            self.interface_version_relelaser = VersionReleaseInterface(self)
            self.interface_version_relelaser.show()
            self.interface_version_relelaser_is_open = True
        else:
            self.interface_version_relelaser.show()
    
class DownloadThread(QThread):
    download_finished = Signal()

    def __init__(self, is_build):
        super().__init__()
        self.is_build = is_build

    def run(self):
        if self.is_build:
            LatestVersion().download_latest_build()
        else:
            LatestVersion().download_latest_release()
        self.download_finished.emit()
        
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

# pyinstaller --onefile --windowed --name=DataQuest --icon=images/smartedge.png --add-data="images/*.png;images/" main.py