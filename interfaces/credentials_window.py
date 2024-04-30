from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from interfaces.base_window import BaseWindow
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QComboBox
)
from PySide6.QtCore import Qt

class DialogCredentialsPosts(BaseWindow):
    def __init__(self, parent=None):
        super(DialogCredentialsPosts,self).__init__(parent)
        self.keyPressEvent = self.key_pressed_handle
        self.list_credentials = [
            'bitrix_username',
            'forum_username',
        ]
        self.list_of_program_names = ['Mycommerce', 'MyPet', 'MyFrota']
        
        self.key = b'nPwQhXeEkt3A7DC4ZqtdVl2xzYQe6IHoq3kmztTIx1M='

        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowModality(Qt.WindowModal)
        width = 530
        height = 500
        self.setFixedSize(width, height)
        self.setWindowTitle("Credenciais")
        self.get_configs_forums()
        self.layout_vertical_name_of_program = QHBoxLayout()
        self.layout_vertical_user_releaser = QHBoxLayout()  
        self.layout_vertical_instructions = QHBoxLayout()
        self.layout_vertical_username_forum = QHBoxLayout()
        self.layout_vertical_password_forum = QHBoxLayout()
        self.layout_vertical_username_bitrix = QHBoxLayout()
        self.layout_vertical_password_bitrix = QHBoxLayout()
        self.layout_vertical_buttons = QHBoxLayout()

        final_list =[
            self.layout_vertical_name_of_program,
            self.layout_vertical_user_releaser,
            self.layout_vertical_instructions ,
            self.layout_vertical_username_forum ,
            self.layout_vertical_password_forum ,
            self.layout_vertical_username_bitrix ,
            self.layout_vertical_password_bitrix ,
            self.layout_vertical_buttons
            ]
        
        self.create_all_labels()
        self.create_all_line_edits()
        self.create_all_combobox()
        self.create_all_buttons()
        self.create_layouts(final_list)

    def create_all_labels(self):
        self.label_select_name_of_program = self.create_label("Selecione o programa a ser liberado: ")
        self.layout_vertical_name_of_program.addWidget(self.label_select_name_of_program)
        
        self.label_user_releaser = self.create_label('Nome do "Atenciosamente": ')
        self.layout_vertical_user_releaser.addWidget(self.label_user_releaser)
        
        self.label_instructions = self.create_label("Insira as credenciais abaixo: ")
        self.layout_vertical_instructions.addWidget(self.label_instructions)
        
        self.label_username_forum = self.create_label("Usuário do fórum:")
        self.layout_vertical_username_forum.addWidget(self.label_username_forum)
        
        self.label_password_forum = self.create_label("Senha do fórum:")
        self.layout_vertical_password_forum.addWidget(self.label_password_forum)
        
        self.label_username_bitrix = self.create_label("Usuário do Bitrix:")
        self.layout_vertical_username_bitrix.addWidget(self.label_username_bitrix)
        
        self.label_password_bitrix = self.create_label("Senha do Bitrix:")
        self.layout_vertical_password_bitrix.addWidget(self.label_password_bitrix)
    
    def create_all_line_edits(self):
        list_line_edits =[]
        self.line_edit_user_releaser = self.create_line_edit(
            placeholder='', mask=False, fixed_size=False, limit_char=30)
        if self.user_releaser != 'default' and self.user_releaser:
            self.line_edit_user_releaser.setText(self.user_releaser)
        list_line_edits.append(self.line_edit_user_releaser)
        
        self.line_edit_forum_username = self.create_line_edit(
            placeholder='Username', mask=False, fixed_size=False, limit_char=160) 
        list_line_edits.append(self.line_edit_forum_username)
        
        self.line_edit_forum_password = self.create_line_edit(
            placeholder='Password', mask=False, password_hider=True, fixed_size=False, limit_char=160)
        self.line_edit_forum_password.setText('******')
        list_line_edits.append(self.line_edit_forum_password)
        
        self.line_edit_bitrix_username = self.create_line_edit(
            placeholder='Username', mask=False, fixed_size=False, limit_char=160)
        list_line_edits.append(self.line_edit_bitrix_username)
        
        self.line_edit_bitrix_password = self.create_line_edit(
            placeholder='Password', mask=False,password_hider=True, fixed_size=False, limit_char=160)
        self.line_edit_bitrix_password.setText('******')
        list_line_edits.append(self.line_edit_bitrix_password)
        
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
        
        for line_edit in list_line_edits:
            line_edit.returnPressed.connect(self.save)

        self.layout_vertical_user_releaser.addWidget(self.line_edit_user_releaser)                    
        self.layout_vertical_username_forum.addWidget(self.line_edit_forum_username)
        self.layout_vertical_password_forum.addWidget(self.line_edit_forum_password)   
        self.layout_vertical_username_bitrix.addWidget(self.line_edit_bitrix_username)                 
        self.layout_vertical_password_bitrix.addWidget(self.line_edit_bitrix_password)
    
    def create_all_combobox(self):
        self.combobox_name_programs = QComboBox()
        self.combobox_name_programs.addItems(self.list_of_program_names)
        for index, item in enumerate(self.list_of_program_names):
            # aqui ele vai focar no item que ja esta no json
            if self.name_of_program == item:
                self.combobox_name_programs.setCurrentIndex(index)
                   
        self.layout_vertical_name_of_program.addWidget(self.combobox_name_programs)
    
    def create_all_buttons(self):
        self.button_save = self.create_button(text="Salvar", function=self.save)
        self.layout_vertical_buttons.addWidget(self.button_save)
    
    def save(self):
        user_releaser = self.line_edit_user_releaser.text()
        name_of_program = self.combobox_name_programs.currentText()
        
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
                if not self.verify_if_is_default(user_releaser):
                    self.file_handler.set_user_releaser(user_releaser)
                if user_releaser == '':
                    self.file_handler.set_user_releaser('default')
                if not self.verify_if_is_default(name_of_program):
                    self.file_handler.set_name_of_program(name_of_program)
                return_file = self.file_handler.write_json()
                if return_file == 'sucess':
                    self.close()
                    self.parent().show_dialog("Credenciais salvas com sucesso!")
                   
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
        if input == '******' or input == 'default':
            return True
        return False
    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DialogCredentialsPosts()
    window.show()
    app.exec()