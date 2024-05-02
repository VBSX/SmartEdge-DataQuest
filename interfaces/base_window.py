from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QPushButton,
    QCheckBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QMessageBox,
    QDialog
    )
from os.path import (abspath as path_os, dirname, join)
import sys
path = path_os('./')
sys.path.append(path)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextOption, QIntValidator
from interfaces.window_input_label import WindowInput
from pyperclip import (copy, paste)
from components.filehandle import File
from components.dbhandle import Database
from components.cript_handle import Cripter
from webbrowser import open_new_tab 


class BaseWindow(QMainWindow):
    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)
        
        self.db = Database()
        self.file_handler = File()
        self.cripter = Cripter()
        
    def key_pressed_handle(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
             
    def setup_ui(self):
        self.setWindowTitle("Base Window")
        
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr( sys, '_MEIPASS', dirname(path_os(__file__)))
        print(base_path, '\n', relative_path)
        return join(base_path, relative_path)  

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
            button.setStyleSheet("background-color: #FFFFFF;color: #000000;border-radius: 25px;")
        if icon:
            button.setIcon(icon)
            if icon_size:
                button.setIconSize(QSize(icon_size,icon_size))
            else:
                button.setIconSize(QSize(64,64))
            if text:
                width = len(text)
                width = width*14
                button.setFixedSize(width+64,64)
            else:
                button.setFixedSize(64,64)
        button.setCursor(Qt.PointingHandCursor)
        return button        
    
    def create_checkbox(self, text, marked = True):
        checkbox = QCheckBox()
        # Deixa o checkbox ja marcado:
        if marked:
            checkbox.setChecked(True)
        else:
            checkbox.setChecked(False)
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.setText(text)
        return checkbox

    def create_label(self, text, is_hidden = False):
        label = QLabel(text)
        if is_hidden:
            label.hide()
        return label
    
    def create_line_edit(
        self, placeholder,
        mask = True,
        fixed_size =True,
        password_hider = False,
        set_text =None,
        limit_char = None,
        only_number = False
        ):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)

        if mask:
            # Configurando a máscara
            line_edit.setInputMask("00.00.00.0000")
        
        if password_hider:
            line_edit.setEchoMode(QLineEdit.Password)

        if fixed_size:
            line_edit.setFixedSize(140,53)

        if set_text:
            line_edit.setText(set_text)
        
        if limit_char:
            line_edit.setMaxLength(limit_char)
        
        if only_number:
            line_edit.setValidator(QIntValidator())
        
        return line_edit
    
    def create_text_edit(self, placeholder):
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        return text_edit
    
    def copy_to_clipboard(self, text):
        copy(text)

    def get_configs_forums(self):
        self.file_handler.__init__()
        json_file = self.file_handler.read_json()
        
        self.bitrix_username = json_file['bitrix_user']
        self.bitrix_password  = json_file['bitrix_password']
        self.forum_username  = json_file['forum_user']
        self.forum_password  = json_file['forum_password']
        self.user_releaser = json_file['user_releaser']
        self.name_of_program = json_file['name_of_program']

    def create_layouts(self, widget_list):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        
        for item in widget_list:
            if type(item) == QHBoxLayout:
                self.layout_principal.addLayout(item)
            elif type(item) == QSpacerItem:
                self.layout_principal.addItem(item)
            else:
                self.layout_principal.addWidget(item)
                
        self.central_widget.setLayout(self.layout_principal)     
    
    def show_confirmation_dialog(self, texto):
        # Cria uma caixa de diálogo de confirmação
        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle('Confirmação')
        confirmation_box.setText(texto)

        # Definindo os textos dos botões em português
        confirmation_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation_box.setButtonText(QMessageBox.Yes, "Sim")
        confirmation_box.setButtonText(QMessageBox.No, "Não")
        
        # Exibe a caixa de diálogo e verifica a resposta do usuário
        reply = confirmation_box.exec_()
        return reply == QMessageBox.Yes
       
    def dialog_input(self, text):
        window_input = WindowInput(self,text)
        if window_input.exec() == QDialog.Accepted:
            return window_input.input_result
        else: return None
        
    def get_configs(self):
        json_file = self.file_handler.read_json()
        self.host = json_file['host']
        self.port = json_file['port']
        self.database = json_file['database']
        
    def get_clipboard(self):
        return paste()
    
    def process_input(self,line_edit, raw_text = False):
        
        if not raw_text:
            current_text = line_edit.text()
        else:
            current_text = line_edit
        if current_text != '...':
            parts = current_text.split('.')
            formatted_text = self.add_zero_to_left(parts)
            if not raw_text:
                line_edit.setText(formatted_text)
            else:
                return formatted_text

    def add_zero_to_left(self, parts_of_text):
        # Adicionando zeros à esquerda conforme necessário
        # Exemplo: 9.1.3.4 -> 09.01.03.0004
        
        formatted_parts = []
        index_of_parts = 1
        for part in parts_of_text:
            if index_of_parts < 4:
                part = part.zfill(2)  
            elif index_of_parts == 4:
                part = part.zfill(4)
            formatted_parts.append(part)
            index_of_parts += 1

        formatted_text = '.'.join(formatted_parts)
        return formatted_text
    
    def line_edit_return_pressed(self, line_edit, next_focus):
        line_edit.returnPressed.connect(lambda: self.process_input(line_edit))
        line_edit.returnPressed.connect(lambda:next_focus.setFocus())