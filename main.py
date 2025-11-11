from os.path import abspath as path_os
from os import startfile
from sys import path as syspath
path = path_os('./')
syspath.append(path)
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QSpacerItem,
    QHBoxLayout,
    QProgressDialog
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSizePolicy, QGraphicsOpacityEffect
from interfaces.query_run_window import QueryWindow
from interfaces.configwindow import ConfigWindow
from interfaces.base_window import BaseWindow
from interfaces.aboutwindow import  AboutProgramWindow
from components.last_version_finder import LatestVersion
from components.os_handle import OsHandler
from interfaces.interface_version_releaser import VersionReleaseInterface
from interfaces.thread_pyside import DownloadThread
from interfaces.sovis_window import SovisWindow
# from memory_profiler import profile

class MainWindow(BaseWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.keyPressEvent = self.handle_events
        self.config_window = None
        self.interface_version_releaser_is_open = False
        self.interface_query_window_is_open = False
        self.interface_sovis_is_open = False
        self.latest_version_handler = None
        self.img_mycommerce_path = r'images\mycommerce.png'
        self.img_config_path = r'images\config.png'
        self.img_about_path = r'images\about.png'
        self.img_smartedge_path = r'images\smartedge.png'
        self.img_pin_path = r'images\pin.png'
        self.img_att_path = r'images\att_db.png'
        self.img_mymonitorfat_path = r'images\mymonitorfat.png'
        self.img_close_path = r'images\x.png'
        self.img_stop_myzap_path = r'images\myzap_ico.png'
        self.is_the_window_fixed = False
        self.os_handler = OsHandler()
        self.setup_ui()
  
    def setup_ui(self, reset_layout= False):
        
        if not reset_layout:
            self.config_imgs()
        self.setWindowTitle('SmartEdge - DataQuest')
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
        self.create_all_line_edit_of_the_window()
        
        self.spacer = QSpacerItem(20,50)
        # espaçador horizontal que deixa todos os itens alinhados à esquerda
        self.spacer_horizontal = QSpacerItem(
            40, 20,
            QSizePolicy.Expanding,  # horizontal policy
            QSizePolicy.Minimum     # vertical policy
        )
                
        self.layout_horizontal_buttons_sql = QHBoxLayout()
        self.layout_horizontal_buttons_sql.addWidget(self.button_db_default_config)
        self.layout_horizontal_buttons_sql.addWidget(self.button_reset_users_password)
        self.layout_horizontal_buttons_sql.addWidget(self.query_button)
        self.layout_horizontal_buttons_sql.addWidget(self.button_release_the_version)
        
        self.layout_horizontal_buttons_sql2 = QHBoxLayout()
        self.layout_horizontal_buttons_sql2.addWidget(self.button_open_sovis_window)
        self.layout_horizontal_buttons_sql2.addWidget(self.label_manual_version_download)
        self.layout_horizontal_buttons_sql2.addWidget(self.line_edit_version_download)
        self.layout_horizontal_buttons_sql2.addWidget(self.baixar_versao_especifica)
        
        self.layout_horizontal_top_tools = QHBoxLayout()
        
        self.layout_horizontal_config_program = QHBoxLayout()
        self.layout_horizontal_close_programs = QHBoxLayout()
        

        self.layout_horizontal_top_tools.addWidget(self.button_pin)
        self.layout_horizontal_top_tools.addWidget(self.button_att_db)
        self.layout_horizontal_top_tools.addWidget(self.button_open_mymonitorfat)
        self.layout_horizontal_top_tools.addWidget(self.button_start_myzap_service)
        
        self.layout_horizontal_config_program.addWidget(self.config_button)
        self.layout_horizontal_config_program.addWidget(self.button_about_program) 

        self.layout_horizontal_close_programs.addWidget(self.label_stop_services)
        #bolinha indicando se o serviço está rodando ou nao
        self.layout_horizontal_close_programs.addWidget(self.label_myzap_service_status)
        self.layout_horizontal_close_programs.addWidget(self.button_stop_myzap_service)
        self.layout_horizontal_close_programs.addItem(self.spacer_horizontal)
        
        self.layout_horizontal_close_programs.addWidget(self.label_close_programs)
        self.layout_horizontal_close_programs.addWidget(self.button_close_mycommerce)
        self.layout_horizontal_close_programs.addWidget(self.button_close_mymonitorfat)
        self.layout_horizontal_close_programs.addWidget(self.button_close_att_db)
        
        
    
        self.layout_database_info = QHBoxLayout()
        self.layout_database_info.addWidget(self.database_label) 
        self.layout_database_info.addWidget(self.button_remove_database)
                
        self.layout_horizontal_database_info = QHBoxLayout()
        self.layout_horizontal_database_info.addWidget(self.host_label)
        self.layout_horizontal_database_info.addWidget(self.port_label)
        self.layout_horizontal_database_info.addItem(self.layout_database_info) 
        
        self.layout_horizontal_downloads = QHBoxLayout()
        self.layout_horizontal_downloads.addWidget(self.label_last_build_version)
        self.layout_horizontal_downloads.addWidget(
            self.download_last_build_version_button)
        
        self.layout_horizontal_downloads.addWidget(self.label_last_release_version)
        self.layout_horizontal_downloads.addWidget(
            self.download_last_release_version_button)
        self.layout_config()
        self.apply_modern_style()
        QTimer.singleShot(0, self.load_deferred_data)
        
    def apply_modern_style(self):
        modern_style = """
        QWidget {
            background-color: #1e1e1e;
            color: #f0f0f0;
            font-family: 'Segoe UI';
            font-size: 15px;
        }

        QLabel {
            color: #dcdcdc;
            font-weight: 500;
        }

        QPushButton {
            background-color: #2d89ef;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
        }

        QPushButton:hover {
            background-color: #1b5fc1;
        }

        QPushButton:pressed {
            background-color: #144a91;
        }

        /* Botões apenas com ícone (config_style="false") — aparência flat e elegante */
        QPushButton[config_style="false"] {
            background: transparent;
            border: none;
            padding: 6px;
            border-radius: 8px;
            min-width: 32px;
            min-height: 32px;
        }

        QPushButton[config_style="false"]:hover {
            background-color: rgba(255, 255, 255, 0.07);
        }

        QPushButton[config_style="false"]:pressed {
            background-color: rgba(255, 255, 255, 0.14);
        }

        QPushButton[config_style="false"]::icon {
            margin: 2px;
        }

        /* NOVO: Estilo para o botão de Perigo (vermelho) */
        #DangerButton {
            background: transparent;
        }
        #DangerButton:hover {
            background-color: #aa2222; 
        }
        #DangerButton:pressed {
            background-color: #881111; 
        }

        QLineEdit {
            background-color: #2b2b2b;
            color: #ffffff;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 6px 8px;
        }

        QLineEdit:focus {
            border: 1px solid #2d89ef;
            background-color: #303030;
        }

        QProgressDialog {
            background-color: #222;
            color: #fff;
        }

        QScrollBar:vertical {
            background: #2b2b2b;
            width: 10px;
            margin: 0px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #555;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #888;
        }
        """
        self.setStyleSheet(modern_style)
        for button in self.list_of_buttons: 
            button.setProperty("config_style", False)

        if hasattr(self, "layout_principal"):
            self.layout_principal.setContentsMargins(30, 20, 30, 20)
            self.layout_principal.setSpacing(15)

        opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity_effect)

        self.fade_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.fade_animation.setDuration(600)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def load_deferred_data(self):
        """
        Esta função é chamada via QTimer APÓS a janela principal ser exibida.
        Ela executa todas as operações lentas de I/O (Rede, Disco, Serviços)
        para não travar a inicialização.
        """
        # 1. Inicializa o log (que pode ser lento)
        self.file_handler.init_txt()

        # 2. Inicializa o handler de versão (que faz PING)
        self.latest_version_handler = LatestVersion()

        # 3. Busca as versões na rede (a parte mais lenta)
        text_latest_build_version = self.latest_version_handler.latest_build_version_text()
        text_latest_release_version = self.latest_version_handler.latest_release_version_text()

        # 4. Processa os textos (lógica que já existia)
        if text_latest_build_version == 'SemBuild':
            display_build_version = 'SemBuild'
            processed_build = 'SemBuild'
        else:
            processed_build = self.process_input(text_latest_build_version, raw_text=True)
            display_build_version = f'{processed_build}'
            
        if text_latest_release_version == None:
            display_release_version = 'SemRelease'
            processed_release = 'SemRelease'
        else:
            processed_release = self.process_input(text_latest_release_version, raw_text=True)
            display_release_version = processed_release

        # 5. Atualiza os labels com os dados reais
        self.label_last_build_version.setText(f'Última Build: {display_build_version}')
        self.label_last_release_version.setText(f'Última Release: {display_release_version}')
        
        # 6. Atualiza o status do serviço (primeira verificação)
        self.label_myzap_service_status.setText(self.os_handler.myzap_service_status())
        
        # 7. Atualiza os handlers de clique para usar as variáveis locais reais
        self.label_last_build_version.mouseDoubleClickEvent = lambda event: self.copy_to_clipboard(processed_build)
        self.label_last_release_version.mouseDoubleClickEvent = lambda event: self.copy_to_clipboard(processed_release)
        
     
    def config_imgs(self):
        has_image_folder = self.file_handler.verify_if_images_path_exists()
        if not has_image_folder:
            self.icon_stop_myzap = QIcon(self.resource_path(self.img_stop_myzap_path))
            self.icon_close_mycommerce = QIcon(self.resource_path(self.img_mycommerce_path))
            self.icon_config = QIcon(self.resource_path(self.img_config_path))
            self.icon_about = QIcon(self.resource_path(self.img_about_path))
            self.icon_pin = QIcon(self.resource_path(self.img_pin_path))
            self.icon_att_db = QIcon(self.resource_path(self.img_att_path))
            self.icon_mymonitorfat = QIcon(self.resource_path(self.img_mymonitorfat_path))
            self.icon_close = QIcon(self.resource_path(self.img_close_path))
            self.setWindowIcon(QIcon(self.resource_path(self.img_smartedge_path)))
        else:
            self.icon_stop_myzap = QIcon(self.img_stop_myzap_path)
            self.icon_close_mycommerce = QIcon(self.img_mycommerce_path)
            self.icon_config = QIcon(self.img_config_path)
            self.icon_about = QIcon(self.img_about_path)
            self.icon_pin = QIcon(self.img_pin_path)
            self.icon_att_db = QIcon(self.img_att_path)
            self.icon_mymonitorfat = QIcon(self.img_mymonitorfat_path)
            self.icon_close = QIcon(self.img_close_path)
            self.setWindowIcon(QIcon(self.img_smartedge_path))

    def layout_config(self):
        self.list_of_widgets = [
            self.layout_horizontal_top_tools,
            self.layout_horizontal_buttons_sql,
            self.spacer,
            self.layout_horizontal_buttons_sql2,
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
        
        for item in self.list_of_widgets:
            if type(item) == QHBoxLayout:
                self.layout_principal.addLayout(item)
            elif type(item) == QSpacerItem:
                self.layout_principal.addItem(item)
            else:
                self.layout_principal.addWidget(item)
                
        self.central_widget.setLayout(self.layout_principal)      
        
    # @profile               
    def reset_layout(self):
        try:
            self.config_window.destroy()
            del self.config_window
            self.config_window = None
        except:
            self.file_handler.add_new_logs('Janela "config" fechada')
            print('Janela "config" fechada')
        try:
            self.about_window.destroy()
            self.about_window = None
        except:
            self.file_handler.add_new_logs('Janela "sobre" fechada')
            print('Janela "sobre" fechada')

        self.centralWidget().deleteLater() 
        self.clearLayout(self.layout_principal)
        # self.clearLayout(self.layout_horizontal_database_info)
        
        self.setup_ui(reset_layout=True)
            
    def window_fixed(self):
        if not self.is_the_window_fixed:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.is_the_window_fixed = True
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.is_the_window_fixed = False
        self.show()
        
     
    def create_all_buttons_of_the_window(self):
        self.list_of_buttons = []
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
        self.button_open_mymonitorfat = self.create_button(
            config_style=False,
            function=self.mymonitor_faturamento_open,
            icon=self.icon_mymonitorfat,
            icon_size = 32
        )
        #
        self.button_start_myzap_service = self.create_button(
            config_style=False,
            function=self.start_myzap_service,
            icon=self.icon_stop_myzap,
            icon_size = 32
        )
        #
        self.button_db_default_config = self.create_button(
            text='Configuração DB padrão',
            function=self.update_db
            )
        self.config_button = self.create_button(
            config_style=False, 
            text='Config',
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
            text='Resetar senha dos usuários',
            function=self.reset_users_password
            )
        #
        self.button_open_sovis_window = self.create_button(
            text='Sovis',
            function=self.open_sovis_window
        )
        #
        self.button_stop_myzap_service = self.create_button(
            config_style=False,
            function=self.stop_myzap_service,
            icon=self.icon_stop_myzap,
            icon_size = 32
        )
        #
        self.button_close_mycommerce = self.create_button(
            config_style=False,
            function=self.mycommerce_close,
            icon=self.icon_close_mycommerce
            )
        #
        self.button_close_mymonitorfat = self.create_button(
            config_style=False,
            function=self.mymonitor_faturamento_close,
            icon=self.icon_mymonitorfat
            )
        #
        self.button_close_att_db = self.create_button(
            config_style=False,
            function=self.att_db_close,
            icon=self.icon_att_db    
        )
        
        self.query_button = self.create_button(
            text='Iniciar uma Query',
            function=self.start_query
            )
        self.download_last_build_version_button = self.create_button(
            text='Baixar Build',
            function=self.download_last_build_version
        )
        self.download_last_release_version_button = self.create_button(
            text='Baixar Release',
            function=self.download_last_release_version
        )
        self.button_release_the_version = self.create_button(
            text='Liberar a versão',
            function=self.release_the_version
        )
    
        self.button_remove_database = self.create_button(
            config_style=False,
            function=self.remove_database,
            icon=self.icon_close,
            icon_size = 32
        )
        self.button_remove_database.setObjectName("DangerButton")
        
        
        self.baixar_versao_especifica = self.create_button(
            text='Download',
            function=lambda: self.download_version(text="Baixando a versão", is_build=None, is_specific_version=True)
        )
        self.list_of_buttons.extend([
            self.button_pin,
            self.button_att_db,
            self.button_open_mymonitorfat,
            self.button_start_myzap_service,
            self.button_db_default_config,
            self.config_button,
            self.button_about_program,
            self.button_reset_users_password,
            self.button_open_sovis_window,
            self.button_stop_myzap_service,
            self.button_close_mycommerce,
            self.button_close_mymonitorfat,
            self.button_close_att_db,
            self.query_button,
            self.download_last_build_version_button,
            self.download_last_release_version_button,
            self.button_release_the_version,
            self.button_remove_database,
            self.baixar_versao_especifica
        ])
           
    def update_db(self):
        self.reset_layout()
        if self.file_handler.verify_if_path_exists(path=self.file_handler.path_json):
            query_return = self.db.db_default_config()
            if query_return == 'sucess':
                self.show_dialog('Configuração realizada com sucesso')
            else:
                self.file_handler.add_new_logs(str(query_return)+' ao rodar as sqls padrões para o banco')
                self.show_dialog(str(query_return))
        else:
            self.show_dialog('Configuração ainda não realizada')
    
    def reset_users_password(self):
        # self.reset_layout()
        query_return = self.db.reset_users_password()
        if query_return == 'sucess':
            self.show_dialog('Senhas resetadas com sucesso')
        else:
            self.file_handler.add_new_logs(str(query_return)+' ao resetar as senhas')
            self.show_dialog(str(query_return))
    
    def mycommerce_close(self):
        process = self.os_handler.kill_mycommerce_process()
        self.show_dialog(str(process))
    
    def mymonitor_faturamento_close(self):
        process = self.os_handler.kill_mymonitorfat_process()
        self.show_dialog(str(process))
    
    def att_db_close(self):
        process = self.os_handler.kill_att_db_process()
        self.show_dialog(str(process))
     
    def start_query(self):
        if not self.interface_query_window_is_open:
            self.get_configs()
            has_connection = self.db.start_connection()
            if has_connection:
                self.query_window = QueryWindow(self)
                self.query_window.show()
                self.interface_query_window_is_open = True
            else:
                self.show_dialog(str(self.db.message_connection_error))
                self.reset_layout()
                self.interface_query_window_is_open = False       
                self.file_handler.add_new_logs(str(self.db.message_connection_error)+' ao abrir a tela de query')
        else:  
            self.query_window.show()
  
    def start_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.setStyleSheet(self.styleSheet())
        self.config_window.show()
    
    def about_program_window(self):
        self.about_window = AboutProgramWindow(self)
        self.about_window.show()

    def create_all_labels_of_the_window(self):
        self.label_manual_version_download = self.create_label('Baixar versão específica')
        
        self.host_label = self.create_label(f'Host: {self.host}')
        
        self.port_label = self.create_label(f'Porta: {self.port}')
        
        self.database_label = self.create_label(f'Database: {self.database}')
        self.database_label.mouseDoubleClickEvent = lambda event: self.update_database_label()
        
        self.label_close_programs = self.create_label('Fechar programas')
        self.label_stop_services = self.create_label('Parar serviços:')

        self.label_myzap_service_status = self.create_label('...')
        self.label_myzap_service_status.mouseDoubleClickEvent = lambda event: self.label_myzap_service_status.setText(self.os_handler.myzap_service_status())
        
        self.timer = self.create_timer(
            1000,
            lambda: self.label_myzap_service_status.setText(self.os_handler.myzap_service_status())
        )
        text_latest_build_version = "Carregando..."
        text_latest_release_version = "Carregando..."
        
        self.label_last_build_version = self.create_label(f'Última Build: {text_latest_build_version}')
        self.label_last_build_version.mouseDoubleClickEvent = lambda event: self.copy_to_clipboard(self.label_last_build_version.text().split(': ')[1])
        
        self.label_last_release_version = self.create_label(f'Última Release: {text_latest_release_version}')
        
        self.label_last_release_version.mouseDoubleClickEvent = lambda event: self.copy_to_clipboard(self.label_last_release_version.text().split(': ')[1])
    
    def create_all_line_edit_of_the_window(self):
        self.line_edit_version_download = self.create_line_edit(
            placeholder="11.01.17.0000",
            mask=True
            )
        self.line_edit_return_pressed(self.line_edit_version_download, self.line_edit_version_download)
    def att_db_open(self):
        self.get_configs()
        config_path = self.file_handler.get_config_path()
        print(config_path)
        if not config_path or not self.file_handler.verify_if_path_exists(config_path):
            self.show_dialog("Caminho do Config.ini não encontrado.")
            return
        
        exe_path = config_path.replace("Config.ini", r"AtualizarDB.exe")
        print(exe_path)
        self.open_programs(exe_path)

    def mymonitor_faturamento_open(self):
        self.get_configs()
        configpath = self.file_handler.get_config_path()
        if not configpath or not self.file_handler.verify_if_path_exists(configpath):
            self.show_dialog("Caminho do Config.ini não encontrado.")
            return
        exe_path = configpath.replace("Config.ini", r"MyMonitorFaturamento.exe")
        self.open_programs(exe_path)
 
    def open_programs(self, path):
        self.get_configs()
        startfile(path)
        self.reset_layout()
        
    def download_last_build_version(self):
        self.download_version(
            'Baixando a última Build', is_build=True)
        
    def download_last_release_version(self):
        self.download_version(
            'Baixando a última Release...', is_build=False)

    def download_version(self, text, is_build, is_specific_version=False):
        specific_version_text = self.line_edit_version_download.text()
        
        if is_specific_version== True and specific_version_text == '...'  or is_specific_version== True and specific_version_text != '' and len(specific_version_text) != 13 :
            self.show_dialog('Digite a versão que deseja baixar')
            return
    
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setWindowTitle('Download')
        self.progress_dialog.setLabelText(text)
        self.progress_dialog.show()
        self.progress_dialog.setRange(0, 0)
        self.progress_dialog.canceled.connect(self.cancel_download)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.reset_layout()
        
        if is_specific_version:
            self.download_thread = DownloadThread(is_build, specific_version=specific_version_text)
        else:
            self.download_thread = DownloadThread(is_build)
        self.download_thread.download_finished.connect(lambda:self.download_finished(is_build))
        self.download_thread.start()
        
        self.download_last_release_version_button.setEnabled(False)
    
        self.download_last_build_version_button.setEnabled(False)  
            
    def download_finished(self, is_build):
        self.progress_dialog.cancel()
        # Se latest_version_handler for None, o download não foi iniciado
        if self.latest_version_handler is None:
            self.show_dialog('Aguarde o carregamento inicial dos dados antes de tentar o download.')
            self.download_last_release_version_button.setEnabled(True)
            self.download_last_build_version_button.setEnabled(True)
            return

        if is_build == None:
            if self.download_thread.specific_version_finished:
                self.show_dialog('Arquivo enviado para a pasta de downloads')
            else:   
                self.show_dialog('Não há arquivo para baixar')
        elif is_build: 
            if self.latest_version_handler.latest_build_version_text() != 'SemBuild':
                self.show_dialog('Arquivo enviado para a pasta de downloads')
            else:   
                self.show_dialog('Não há arquivo para baixar')
        else:
            if self.latest_version_handler.latest_release_version_text() != None:
                self.show_dialog('Arquivo enviado para a pasta de downloads')
            else:
                self.show_dialog('Não há arquivo para baixar')
                
        self.download_last_release_version_button.setEnabled(True)
    
        self.download_last_build_version_button.setEnabled(True)  

    def cancel_download(self):
        self.download_thread.cancel()
        if self.download_thread.download_cancelled:
            self.download_last_release_version_button.setEnabled(True)
            self.download_last_build_version_button.setEnabled(True)  
            self.show_dialog('Download cancelado')
        
    def release_the_version(self):
        if not self.interface_version_releaser_is_open:
            self.interface_version_releaser = VersionReleaseInterface(self)
            self.interface_version_releaser.show()
            self.interface_version_releaser_is_open = True
        else:
            self.interface_version_releaser.show()
   
    def open_sovis_window(self):
        if not self.interface_sovis_is_open:
            self.sovis_window = SovisWindow(self)
            self.sovis_window.show()
            self.interface_sovis_is_open = True
        else:
            self.sovis_window.show()

    def remove_database(self):
        self.get_configs()
        self.copy_to_clipboard(self.database)
        self.file_handler.set_database('')
        self.reset_layout()

    def update_database_label(self):
        self.file_handler.set_database(self.get_clipboard())
        self.reset_layout()

    def handle_events(self, event):
        if self.latest_version_handler is None:
            return

        text_latest_build_version = self.latest_version_handler.latest_build_version_text()
        text_latest_release_version = self.latest_version_handler.latest_release_version_text()
        
        processed_build = self.process_input(text_latest_build_version, raw_text=True)
        processed_release = self.process_input(text_latest_release_version, raw_text=True)

        # Verifica se as teclas Shift, Alt e S estão pressionadas simultaneamente
        if event.modifiers() == (Qt.ShiftModifier | Qt.AltModifier) and event.key() == Qt.Key_S:
            # Chama a função para copiar para o clipboard
            self.copy_to_clipboard(processed_build)
        elif event.modifiers() == (Qt.ShiftModifier | Qt.AltModifier) and event.key() == Qt.Key_D:
            self.copy_to_clipboard(processed_release)


    def stop_myzap_service(self):
        process = self.os_handler.stop_myzap_service()
        self.show_dialog(str(process))
    
    def start_myzap_service(self):
        process = self.os_handler.start_myzap_service()
        self.show_dialog(str(process))
    
    def create_timer(self, interval, function):
        timer = QTimer(self)
        timer.timeout.connect(function)
        timer.start(interval)
        return timer
    
if __name__ == '__main__': 
    from sys import argv
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
    
# pyinstaller --onefile --windowed --name=DataQuest --icon=images/smartedge.png --add-data="images/*.png;images/" --exclude PyQt5 main.py