from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QPushButton,
    QCheckBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QMessageBox,
    QDialog
    )

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextOption
from interfaces.window_input_label import WindowInput
import pyperclip
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
        
    def key_pressed_handle(self, event):
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

    def create_label(self, text):
        label = QLabel(text)
        return label
    
    def create_line_edit(self, placeholder, mask = True, fixed_size =True, password_hider = False, set_text =None):
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
        
        return line_edit
    
    def create_text_edit(self, placeholder):
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        return text_edit
    
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        # spam = pyperclip.paste()

    def get_configs_forums(self):
        self.file_handler.__init__()
        json_file = self.file_handler.read_json()
        
        self.bitrix_username = json_file['bitrix_user']
        self.bitrix_password  = json_file['bitrix_password']
        self.forum_username  = json_file['forum_user']
        self.forum_password  = json_file['forum_password']

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
    
    def show_confirmation_dialog(self):

        # Cria uma caixa de diálogo de confirmação
        reply = QMessageBox.question(None, 'Confirmação', 'Você tem certeza que deseja continuar?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # Verifica a resposta do usuário
        return reply == QMessageBox.Yes

    def dialog_input(self, text):
        window_input = WindowInput(self,text)
        if window_input.exec() == QDialog.Accepted:
            return window_input.input_result
        else: return None