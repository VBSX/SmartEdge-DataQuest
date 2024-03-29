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
    QLineEdit
    )
from PySide6.QtCore import Qt
from interfaces.base_window import BaseWindow

class ConfigWindow(BaseWindow):
    def __init__(self, parent=None):
        super(ConfigWindow,self).__init__(parent)
        self.keyPressEvent = self.key_pressed_handle
        self.user = self.file_handler.username
        self.password = self.file_handler.password
        self.host = self.file_handler.host
        self.port = self.file_handler.port
        self.database = self.file_handler.database
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Config")
        self.setFixedSize(430, 410)

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
        if not self.user:
            self.line_edit_username.setText('root')
        else:
            self.line_edit_username.setText(self.user)
        self.line_edit_username.setPlaceholderText('root')
        self.line_edit_username.returnPressed.connect(self.button_save.click)
        self.line_edit_username.setMaxLength(20)
        
        ## Set the layout of the label and the line edit in the same line
        self.horizontal_layout_set(self.label_username, self.line_edit_username, None, None)
        
        # field password config
        self.label_password = QLabel('Senha: ')
        self.line_edit_password = QLineEdit()
 
        self.line_edit_password.returnPressed.connect(self.button_save.click)
        self.line_edit_password.setPlaceholderText('****')
        self.line_edit_password.setText(self.password)
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.line_edit_password.setMaxLength(35)
        self.horizontal_layout_set(self.label_password, self.line_edit_password, None, None)
        
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
        
        self.layout_vertical.addWidget(self.button_save)   
        
        central_widget.setLayout(self.layout_vertical)
        
        #absolute window, cant acess the main window ultil the window is closed
        self.setWindowModality(Qt.WindowModal)
        self.show()
    
    def horizontal_layout_set(self, first_item, second_item, third_item, fourth_item):
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setContentsMargins(0, 0, 0, 0)
        layout_horizontal.setSpacing(0)
        layout_horizontal.setAlignment(Qt.AlignLeft)
        layout_horizontal.addWidget(first_item)
        layout_horizontal.addWidget(second_item)
        if third_item:
            layout_horizontal.addWidget(third_item)
            if fourth_item:
                layout_horizontal.addWidget(fourth_item)
        ## add the layout horizontal to the vertical layout
        self.layout_vertical.addLayout(layout_horizontal)
    
    def get_data_from_json(self):
        return self.file_handler.read_json()

    def save_data(self):
        username_input = self.line_edit_username.text()
        password_input = self.line_edit_password.text()
        host_input = self.combobox_host.currentText()
        port_input = self.line_edit_port.text()
        database_input = self.line_edit_database.text()
        
        if (username_input == self.user and
            password_input == self.password and
            host_input == self.host and
            port_input == self.port and
            database_input == self.database):
            
            del self.file_handler
            self.close()
            self.parent().reset_layout()
        else:
            self.file_handler.set_username(username_input)
            self.file_handler.set_password(password_input)
            self.file_handler.set_host(host_input)
            self.file_handler.set_port(port_input)
            self.file_handler.set_database(database_input)
            
            return_file = self.file_handler.write_json()
            
            if return_file == 'sucess':
                self.close()
                self.parent().reset_layout()
                self.parent().show_dialog("Configuração realizada com sucesso")
                       
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from sys import argv, exit
    app = QApplication(argv)
    window = ConfigWindow()
    exit(app.exec())