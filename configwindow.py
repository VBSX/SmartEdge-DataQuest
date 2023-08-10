from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout,QPushButton
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit
from filehandle import File

class ConfigWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ConfigWindow,self).__init__(parent)
        self.file_handler = File()
        self.user = self.file_handler.username
        self.password = self.file_handler.password
        self.host = self.file_handler.host
        self.port = self.file_handler.port
        self.database = self.file_handler.database
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Config")
        self.setFixedSize(400, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout_vertical = QVBoxLayout()
        
        # Field username config
        self.label_username = QLabel('Usuário: ')
        self.line_edit_username = QLineEdit()
        if not self.user:
            self.line_edit_username.setText('root')
        else:
            self.line_edit_username.setText(self.user)
        self.line_edit_username.setPlaceholderText('root')
        
        ## Set the layout of the label and the line edit in the same line
        self.horizontal_layout_set(self.label_username, self.line_edit_username, None, None)
        
        # field password config
        self.label_password = QLabel('Senha: ')
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText('****')
        self.line_edit_password.setText(self.password)
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        self.horizontal_layout_set(self.label_password, self.line_edit_password, None, None)
        
        #field host config
        self.label_host = QLabel('Host: ')
        self.line_edit_host = QLineEdit()
        if self.host == '':
            self.line_edit_host.setPlaceholderText('10.1.1.220')
        else:
            self.line_edit_host.setText(self.host)
        self.line_edit_host.setPlaceholderText('10.1.1.220')
        
        
        #field port config
        self.label_port = QLabel('Porta: ')
        self.line_edit_port = QLineEdit()
        if not self.port:
            self.line_edit_port.setText('3306')
        else: 
            self.line_edit_port.setText(self.port)
            
        self.line_edit_port.setPlaceholderText('3306')
        # config of host and port itens on same line
        self.horizontal_layout_set(self.label_host, self.line_edit_host,self.label_port, self.line_edit_port)
        
        #field database config
        self.label_database = QLabel('Nome do Banco: ')
        self.line_edit_database = QLineEdit()
        if not self.database:
            self.line_edit_database.setText('db_name')
        else:
            self.line_edit_database.setText(self.database)
        self.line_edit_database.setPlaceholderText('db_name')
        self.horizontal_layout_set(self.label_database, self.line_edit_database, None, None)
        
        #save button
        self.button_save = QPushButton('Salvar')
        self.button_save.clicked.connect(self.save_data)
        self.button_style_config(self.button_save)
        self.layout_vertical.addWidget(self.button_save)
        
        central_widget.setLayout(self.layout_vertical)
        print(self.line_edit_username.text())

        
        #absolute window, cant acess the main window ultil the window is closed
        self.setWindowModality(Qt.WindowModal)
        self.show()   
    
    def button_style_config(self, button):
        button.setStyleSheet("background-color: #FFFFFF;color: #000000;border-radius: 10px;")
        button.setCursor(Qt.PointingHandCursor)
    
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
        ## add the layout to the vertical layout
        self.layout_vertical.addLayout(layout_horizontal)
    
    def get_data_from_json(self):
        return self.file_handler.read_json()

    def save_data(self):
        username_input = self.line_edit_username.text()
        password_input = self.line_edit_password.text()
        host_input = self.line_edit_host.text()
        port_input = self.line_edit_port.text()
        database_input = self.line_edit_database.text()
        username_not_changed = False
        password_not_changed = False
        host_not_changed = False
        port_not_changed = False
        database_not_changed = False
              
        
        if username_input != self.user:
            self.file_handler.set_username(username_input)
        else:
            username_not_changed = True
        if password_input != self.password:
            self.file_handler.set_password(password_input)
        else:
            password_not_changed = True
            
        if host_input != self.host:
            self.file_handler.set_host(host_input)
        else:
            host_not_changed = True
            
        if port_input != self.port:
            self.file_handler.set_port(port_input)
        else:
            port_not_changed = True
            
        if database_input != self.database:
            self.file_handler.set_database(database_input)
        else: 
            database_not_changed = True
        
        if username_not_changed and password_not_changed and host_not_changed and port_not_changed and database_not_changed:
            self.close()
        else:
            return_file = self.file_handler.write_json()
            
            if return_file == 'sucess':
                self.close()
                self.parent().show_dialog("Configuração realizada com sucesso")
    

            
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ConfigWindow()
    sys.exit(app.exec())