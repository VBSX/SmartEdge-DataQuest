from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit, QLayout
    )
from PySide6.QtCore import Qt
from interfaces.base_window import BaseWindow, File, QPushButton
from PySide6.QtWidgets import (
    QFileDialog
)
class ConfigWindow(BaseWindow):
    def __init__(self, parent=None):
        super(ConfigWindow,self).__init__(parent)
        self.keyPressEvent = self.key_pressed_handle
        self.user = self.file_handler.username
        self.password = self.file_handler.password
        self.host = self.file_handler.host
        self.port = self.file_handler.port
        self.database = self.file_handler.database
        self.get_configs()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Config")
        self.setFixedSize(530, 455)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout_vertical = QVBoxLayout()

        #save button
        self.button_save = self.create_button(
            text='Salvar',
            function=self.save_data)
             
        # Field username config
        self.label_username = QLabel('Usuário: ')
        self.line_edit_username = QLineEdit()
        if self.user and self.user != 'default':
            self.line_edit_username.setText(self.user)

        self.line_edit_username.setPlaceholderText('root')
        self.line_edit_username.returnPressed.connect(self.button_save.click)
        self.line_edit_username.setMaxLength(20)
        

        
        layout_vertical_checkbox_test_mode = QVBoxLayout()
        self.test_mode_checkbox = self.create_checkbox(
            text='CQP=1 (Homologação)',
            marked= self.check_marked(self.test_mode))
        layout_vertical_checkbox_test_mode.addWidget(self.test_mode_checkbox)
        
        self.csharp_mode_checkbox = self.create_checkbox(
            text='MyCCSharp=1 (Usar telas C# \nem teste)',
            marked= self.check_marked(self.csharp_mode))
        layout_vertical_checkbox_test_mode.addWidget(self.csharp_mode_checkbox)
        
        ## Set the layout of the label and the line edit in the same line
        self.horizontal_layout_set(self.label_username, self.line_edit_username, layout_vertical_checkbox_test_mode, None)
        
        # field password config
        self.label_password = QLabel('Senha: ')
        self.line_edit_password = QLineEdit()
 
        self.line_edit_password.returnPressed.connect(self.button_save.click)
        self.line_edit_password.setPlaceholderText('****')
        if self.password and self.password != "default":
            self.line_edit_password.setText(self.password)
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setMaxLength(35)
        
        self.dropbox_password = self.create_button(
            text='Mostrar',
            function=self.show_password)
        self.horizontal_layout_set(self.label_password, self.line_edit_password, self.dropbox_password, None)
        
        #field host config
        self.label_host = QLabel('Host: ')
        self.combobox_host = QComboBox()
        if self.host == '':
            self.combobox_host.addItems(['10.1.1.220', 'localhost'])
        elif self.host == 'localhost':
            self.combobox_host.addItems(['localhost', '10.1.1.220'])
        else:
            self.combobox_host.addItems([self.host, 'localhost'])
        
        #field port config
        self.label_port = QLabel('Porta: ')
        self.line_edit_port = QLineEdit()
        self.line_edit_port.setMaxLength(4)
        
        if not self.port:
            self.line_edit_port.setText('3306')
        else: 
            self.line_edit_port.setText(self.port)
            
        self.line_edit_port.setPlaceholderText('3306')
        self.line_edit_port.returnPressed.connect(self.button_save.click)
        
        # config of host and port itens on same line
        self.horizontal_layout_set(self.label_host, self.combobox_host,self.label_port, self.line_edit_port)
        
        #field database config
        self.label_database = QLabel('Nome do Banco: ')
        self.line_edit_database = QLineEdit()
        if not self.database or self.database =='None':
            self.line_edit_database.setText('')
            self.line_edit_database.setPlaceholderText('db_name')
        else:
            self.line_edit_database.setText(self.database)
        self.line_edit_database.setPlaceholderText('db_name')
        self.line_edit_database.returnPressed.connect(self.button_save.click)
        self.line_edit_database.setMaxLength(20)
        
        self.horizontal_layout_set(self.label_database, self.line_edit_database, None, None)
        # field config_path
        self.label_config_path = QLabel('Caminho do Config.ini:')
        self.line_edit_config_path = QLineEdit()

        if self.file_handler.ini_config.config_path:
            self.line_edit_config_path.setText(self.file_handler.get_config_path())

        else:
            self.line_edit_config_path.setText(r'C:\Visual Software\MyCommerce\Config.ini')


        self.line_edit_config_path.setPlaceholderText(r'C:\Visual Software\MyCommerce\Config.ini')

        # Botão para abrir o explorador
        self.button_browse = QPushButton("📂")
        self.button_browse.setFixedWidth(45)
        self.button_browse.clicked.connect(self.browse_config_file)

        # Layout na mesma linha
        self.horizontal_layout_set(self.label_config_path, self.line_edit_config_path, self.button_browse, None)        
        self.layout_vertical.addWidget(self.button_save)   
        
        central_widget.setLayout(self.layout_vertical)
        
        #absolute window, cant acess the main window ultil the window is closed
        self.setWindowModality(Qt.WindowModal)
        self.show()

    def check_marked(self, mode):
        # organiza na lista todos os checkboxes, e depois lista qual é qual para que seja usado o mesmo algoritimo para marcar ou desmarcar

        if mode == 1 or mode == 'None' or mode == '1':
            check_marked = True
        elif mode == 0 or mode == '0':
            check_marked = False
        elif mode == 'None':
            check_marked = True
        
        return check_marked
   
    def horizontal_layout_set(self, first_item, second_item, third_item=None, fourth_item=None):
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)
        layout_horizontal.setAlignment(Qt.AlignLeft)

        layout_horizontal.addWidget(first_item)
        layout_horizontal.addWidget(second_item)

        if third_item:
            if isinstance(third_item, QLayout):
                layout_horizontal.addLayout(third_item)
            else:
                layout_horizontal.addWidget(third_item)
        if fourth_item:
            if isinstance(fourth_item, QLayout):
                layout_horizontal.addLayout(fourth_item)
            else:
                layout_horizontal.addWidget(fourth_item)

        self.layout_vertical.addLayout(layout_horizontal)

    
    def get_data_from_json(self):
        return self.file_handler.read_json()

    def save_data(self):
        username_input = self.line_edit_username.text()
        password_input = self.line_edit_password.text()
        host_input = self.combobox_host.currentText()
        port_input = self.line_edit_port.text()
        database_input = self.line_edit_database.text()
        test_mode_input = self.test_mode_checkbox.isChecked()
        csharp_mode_input = self.csharp_mode_checkbox.isChecked()
        
        if csharp_mode_input:
            csharp_mode_input = '1'
        else:
            csharp_mode_input = '0'
        
        if test_mode_input:
            test_mode_input = '1'
        else:
            test_mode_input = '0'

        config_path_input = self.line_edit_config_path.text().strip()
        if not config_path_input:
            self.show_dialog("O caminho do Config.ini não pode estar vazio")
            return

        self.file_handler.set_config_path(config_path_input)

        self.file_handler = File(config_path=config_path_input)


        if (username_input == self.user and
            password_input == self.password and
            host_input == self.host and
            port_input == self.port and
            database_input == self.database and
            test_mode_input == self.test_mode and
            csharp_mode_input == self.csharp_mode
            ):
            self.close()
            self.parent().reset_layout()
        elif not password_input or not username_input:
            self.show_dialog("Preencha todos os campos")
        else:
            self.file_handler.set_username(username_input)
            self.file_handler.set_password(password_input)
            self.file_handler.set_host(host_input)
            self.file_handler.set_port(port_input)
            self.file_handler.set_database(database_input)
            self.file_handler.set_test_mode(test_mode_input)
            self.file_handler.set_csharp_mode(csharp_mode_input)

            return_file = self.file_handler.write_json()

            if return_file == 'sucess':
                self.line_edit_config_path.setText(self.file_handler.ini_config.config_path)

                self.close()
                self.parent().reset_layout()
                self.parent().show_dialog("Configuração realizada com sucesso")

    
    def show_password(self):
        if self.line_edit_password.echoMode() == QLineEdit.Password:
            self.line_edit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.line_edit_password.setEchoMode(QLineEdit.Password)

    def browse_config_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione o arquivo de configuração",
            "",
            "Arquivos INI (*.ini);;Todos os arquivos (*)"
        )
        if file_path:
            self.line_edit_config_path.setText(file_path)

                       
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from sys import argv, exit
    app = QApplication(argv)
    window = ConfigWindow()
    exit(app.exec())