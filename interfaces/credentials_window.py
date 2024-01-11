import sys
import os
path = os.path.abspath('./')
sys.path.append(path)
from interfaces.base_window import BaseWindow
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

class DialogCredentialsPosts(BaseWindow):
    def __init__(self, parent=None):
        super(DialogCredentialsPosts,self).__init__(parent)
        self.list_credentials = [
            'bitrix_username',
            'forum_username',
        ]
        self.key = b'nPwQhXeEkt3A7DC4ZqtdVl2xzYQe6IHoq3kmztTIx1M='

        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowModality(Qt.WindowModal)
        self.setFixedSize(460, 410)
        self.setWindowTitle("Credenciais")
        self.get_configs_forums()
        self.layout_vertical_instructions = QHBoxLayout()
        self.layout_vertical_username_forum = QHBoxLayout()
        self.layout_vertical_password_forum = QHBoxLayout()
        self.layout_vertical_username_bitrix = QHBoxLayout()
        self.layout_vertical_password_bitrix = QHBoxLayout()
        self.layout_vertical_buttons = QHBoxLayout()

        final_list =[
            self.layout_vertical_instructions ,
            self.layout_vertical_username_forum ,
            self.layout_vertical_password_forum ,
            self.layout_vertical_username_bitrix ,
            self.layout_vertical_password_bitrix ,
            self.layout_vertical_buttons
            ]
        
        self.create_all_labels()
        self.create_all_line_edits()
        self.create_all_buttons()
        self.create_layouts(final_list)

    def create_all_labels(self):
        self.label_instructions = self.create_label("Insira as credenciais abaixo")
        self.layout_vertical_instructions.addWidget(self.label_instructions)
        
        self.label_username_forum = self.create_label("Usuário do fórum")
        self.layout_vertical_username_forum.addWidget(self.label_username_forum)
        
        self.label_password_forum = self.create_label("Senha do fórum")
        self.layout_vertical_password_forum.addWidget(self.label_password_forum)
        
        self.label_username_bitrix = self.create_label("Usuário do Bitrix")
        self.layout_vertical_username_bitrix.addWidget(self.label_username_bitrix)
        
        self.label_password_bitrix = self.create_label("Senha do Bitrix")
        self.layout_vertical_password_bitrix.addWidget(self.label_password_bitrix)
    
    def create_all_line_edits(self):
        self.line_edit_forum_username = self.create_line_edit(placeholder='Username', mask=False) 
        
        self.line_edit_forum_password = self.create_line_edit(placeholder='Password', mask=False, password_hider=True)
        self.line_edit_forum_password.setText('******')
        
        self.line_edit_bitrix_username = self.create_line_edit(placeholder='Username', mask=False)
        
        self.line_edit_bitrix_password = self.create_line_edit(placeholder='Password', mask=False,password_hider=True)
        self.line_edit_bitrix_password.setText('******')
    
        list_credentials = [
            self.bitrix_username,
            self.forum_username,
        ]
        for credential in self.list_credentials:
                for data_credential in list_credentials:
                    if data_credential != 'default':
                        if credential=='forum_username':
                            fr_user = self.cripter.decrypt(self.forum_username)
                            self.line_edit_forum_username.setText(fr_user)
                        elif credential=='bitrix_username':
                            bt_user = self.cripter.decrypt(self.bitrix_username)
                            self.line_edit_bitrix_username.setText(bt_user)
                            
        self.layout_vertical_username_forum.addWidget(self.line_edit_forum_username)
        self.layout_vertical_password_forum.addWidget(self.line_edit_forum_password)   
        self.layout_vertical_username_bitrix.addWidget(self.line_edit_bitrix_username)                 
        self.layout_vertical_password_bitrix.addWidget(self.line_edit_bitrix_password)
    
    def create_all_buttons(self):
        self.button_save = self.create_button(text="Salvar", function=self.save)
        self.layout_vertical_buttons.addWidget(self.button_save)
    
    def save(self):
        forum_username = self.line_edit_forum_username.text()
        forum_username_encripted= self.cripter.encrypt(forum_username)
        forum_username_json_decripted = self.cripter.decrypt(self.forum_username)
        
        
        forum_password = self.line_edit_forum_password.text()
        forum_password_encripted= self.cripter.encrypt(forum_password)
        forum_password_json_decripted = self.cripter.decrypt(self.forum_password)

        bitrix_username = self.line_edit_bitrix_username.text()
        bitrix_username_encripted= self.cripter.encrypt(bitrix_username)
        bitrix_username_json_decripted = self.cripter.decrypt(self.bitrix_username)
        
        bitrix_password = self.line_edit_bitrix_password.text()
        bitrix_password_encripted= self.cripter.encrypt(bitrix_password)
        bitrix_password_json_decripted = self.cripter.decrypt(self.bitrix_password)
        
        list_user_input = [forum_username, forum_password, bitrix_username, bitrix_password]
        list_credentials_decript = [forum_username_json_decripted, forum_password_json_decripted, bitrix_username_json_decripted, bitrix_password_json_decripted]
        
        if self.verify_if_is_empty(list_user_input): 
            self.show_dialog("Preencha todos os campos")
        else:
            if self.verify_if_is_equal(list_user_input, list_credentials_decript):
                self.close()
            else:
                self.file_handler.set_forum_user(forum_username_encripted)
                if not self.verify_if_is_default(forum_password):
                    self.file_handler.set_forum_password(forum_password_encripted)
                self.file_handler.set_bitrix_user(bitrix_username_encripted)
                if not self.verify_if_is_default(bitrix_password):
                    self.file_handler.set_bitrix_password(bitrix_password_encripted)        
                return_file = self.file_handler.write_json()
                if return_file == 'sucess':
                    self.close()
                    
    def verify_if_is_empty(self, list_user_input):
        for item in list_user_input:
            if item == '':
                return True
        return False 
    
    def verify_if_is_equal(self, list_user_input, list_credentials):
        for index, user_input in enumerate(list_user_input):
            if user_input[index] != list_credentials[index]:
                return False
        return True
    
    def verify_if_is_default(self, input):
        if input == '******':
            return True
        return False
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DialogCredentialsPosts()
    window.show()
    app.exec()