import sys
from cryptography.fernet import Fernet
import base64
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
                            fr_user = self.decrypt(self.forum_username)
                            self.line_edit_forum_username.setText(fr_user)
                        elif credential=='bitrix_username':
                            bt_user = self.decrypt(self.bitrix_username)
                            self.line_edit_bitrix_username.setText(bt_user)
                            
        self.layout_vertical_username_forum.addWidget(self.line_edit_forum_username)
        self.layout_vertical_password_forum.addWidget(self.line_edit_forum_password)   
        self.layout_vertical_username_bitrix.addWidget(self.line_edit_bitrix_username)                 
        self.layout_vertical_password_bitrix.addWidget(self.line_edit_bitrix_password)
    
    def decrypt(self, password):
        try:
            # Decodifica a string base64
            encrypted_bytes = base64.urlsafe_b64decode(password)

            # Cria um objeto Fernet com a chave e descriptografa
            cipher = Fernet(self.key)
            decrypted_text = cipher.decrypt(encrypted_bytes).decode('utf-8')
            return decrypted_text
        except Exception as e:
            print(f"Erro ao descriptografar: {e}")
            return None
        
    def encrypt(self, password):
        # Cria um objeto Fernet com a chave
        cipher = Fernet(self.key)

        # Criptografa o texto e codifica para base64
        encrypted_bytes = cipher.encrypt(password.encode('utf-8'))
        encrypted_text = base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_text
    
    def create_all_buttons(self):
        self.button_save = self.create_button(text="Salvar", function=self.save)
        self.layout_vertical_buttons.addWidget(self.button_save)
    
    def save(self):
        forum_username = self.line_edit_forum_username.text()
        forum_username_encripted= self.encrypt(forum_username)
        forum_username_json_decripted = self.decrypt(self.forum_username)
        
        forum_password = self.line_edit_forum_password.text()
        forum_password_encripted= self.encrypt(forum_password)
        forum_password_json_decripted = self.decrypt(self.forum_password)
        
        bitrix_username = self.line_edit_bitrix_username.text()
        bitrix_username_encripted= self.encrypt(bitrix_username)
        bitrix_username_json_decripted = self.decrypt(self.bitrix_username)
        
        bitrix_password = self.line_edit_bitrix_password.text()
        bitrix_password_encripted= self.encrypt(bitrix_password)
        bitrix_password_json_decripted = self.decrypt(self.bitrix_password)
        
        if (forum_username == '' or
            forum_password == '' or
            bitrix_username == '' or
            bitrix_password == ''
        ):
            self.show_dialog("Preencha todos os campos")
        else:
            if (forum_username == forum_username_json_decripted and
                forum_password == forum_password_json_decripted and
                bitrix_username == bitrix_username_json_decripted and
                bitrix_password == bitrix_password_json_decripted):

                self.close()
            else:
                self.file_handler.set_forum_user(forum_username_encripted)
                self.file_handler.set_forum_password(forum_password_encripted)
                self.file_handler.set_bitrix_user(bitrix_username_encripted)
                self.file_handler.set_bitrix_password(bitrix_password_encripted)        
                return_file = self.file_handler.write_json()
                
                if return_file == 'sucess':
                    self.close()
                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DialogCredentialsPosts()
    window.show()
    app.exec()