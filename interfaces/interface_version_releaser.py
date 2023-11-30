import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from interfaces.base_window import BaseWindow
from PySide6.QtCore import Qt
from interfaces.credentials_window import DialogCredentialsPosts
from components.last_version_finder import LatestVersion
from components.automation_windows.create_post import BrowserController

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QSpacerItem
)

class VersionReleaseInterface(BaseWindow):
    def __init__(self, parent=None):
        super(VersionReleaseInterface, self).__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Liberar Versão")
        
        self.setFixedSize(650, 700)
        self.get_configs_forums()
        self.horizontal_layout_mycommerce_pdv = QHBoxLayout()
        self.horizontal_layout_mylocacao = QHBoxLayout()
        self.horizontal_layout_mypet = QHBoxLayout()
        self.horizontal_layout_myzap = QHBoxLayout()
        self.horizontal_layout_vsintegracao = QHBoxLayout()
        self.horizontal_layout_release = QHBoxLayout()
        self.horizontal_layout_manual_release = QHBoxLayout()
        self.horizontal_layout_messages = QHBoxLayout()
        self.horizontal_history_version = QHBoxLayout()
        
        final_list =[
            self.horizontal_layout_release,self.horizontal_layout_mycommerce_pdv,
            self.horizontal_layout_mylocacao, 
            self.horizontal_layout_mypet, self.horizontal_layout_myzap, self.horizontal_layout_vsintegracao,
            self.horizontal_history_version,
            self.horizontal_layout_messages ,self.horizontal_layout_manual_release
            ]
        
        self.create_all_checkboxes()
        self.create_all_labels()
        self.create_all_line_edits()
        self.create_all_buttons()
        self.create_layouts(final_list)

    def create_all_buttons(self):
        self.button_release_version = self.create_button(
            text="Liberar Versão", function=self.release_version)
        self.horizontal_layout_release.addWidget(self.button_release_version)
        
        self.button_create_post = self.create_button(
            text="Criar Post", function=self.create_post)
        self.horizontal_layout_manual_release.addWidget(self.button_create_post)
        
        self.button_copy_post_compatibilities = self.create_button(
            text="Copiar compatibilidades", function=lambda:self.copy_post_compatibilities(show_dialog=True)
        ) 
        self.horizontal_layout_manual_release.addWidget(self.button_copy_post_compatibilities)
        
        self.button_copy_complete_message = self.create_button(
            text="Copiar mensagem completa", function=self.copy_all_text_to_clipboard
        ) 
        self.horizontal_layout_manual_release.addWidget(self.button_copy_complete_message)
        
    def create_all_checkboxes(self):
        self.checkbox_compativel_mycommerce_pdv = self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_mycommerce_pdv.addWidget(self.checkbox_compativel_mycommerce_pdv)
        
        self.checkbox_compativel_mylocacao = self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_mylocacao.addWidget(self.checkbox_compativel_mylocacao)
        
        self.checkbox_compativel_mypet = self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_mypet.addWidget(self.checkbox_compativel_mypet)
        
        self.checkbox_compativel_myzap = self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_myzap.addWidget(self.checkbox_compativel_myzap)
        
        self.checkbox_compativel_vsintegracao = self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_vsintegracao.addWidget(self.checkbox_compativel_vsintegracao)
        
        self.checkbox_history_of_version = self.create_checkbox(
            text="Histórico de versão"
        )
        self.horizontal_history_version.addWidget(self.checkbox_history_of_version)

        
    def create_all_labels(self):
        self.label_mycommerce_pdv = self.create_label(
            text="MyCommerce PDV: ")
        self.horizontal_layout_mycommerce_pdv.addWidget(self.label_mycommerce_pdv)
        
        self.label_mylocacao_version = self.create_label(
            text="MyLocação: ")
        self.horizontal_layout_mylocacao.addWidget(self.label_mylocacao_version)
        
        self.label_mypet =self.create_label(
            text="MyPet: "
        )
        self.horizontal_layout_mypet.addWidget(self.label_mypet)
        
        self.label_myzap = self.create_label(
            text="MyZap: "  
        )
        self.horizontal_layout_myzap.addWidget(self.label_myzap)
        
        self.label_vsintegracao = self.create_label(
            text="VsIntegracao: "
        )
        self.horizontal_layout_vsintegracao.addWidget(self.label_vsintegracao)
        
        self.label_version_mycommerce_release = self.create_label(
            text="Versão do MyCommerce: "
        )
        self.horizontal_layout_release.addWidget(self.label_version_mycommerce_release)
        
    def create_all_line_edits(self):
        self.line_edit_mycommerce_pdv_version = self.create_line_edit(
            placeholder="versão do MyCommerce PDV"
        )
        self.horizontal_layout_mycommerce_pdv.addWidget(self.line_edit_mycommerce_pdv_version)
        
        self.line_edit_mylocacao_version = self.create_line_edit(
            placeholder="versão do MyLocação"
        )
        self.horizontal_layout_mylocacao.addWidget(self.line_edit_mylocacao_version)

        self.line_edit_mypet = self.create_line_edit(
            placeholder="versão do MyPet"
        )
        self.horizontal_layout_mypet.addWidget(self.line_edit_mypet)
        
        self.line_edit_myzap = self.create_line_edit(
            placeholder="versão do MyZap"
        )
        self.horizontal_layout_myzap.addWidget(self.line_edit_myzap)
        
        self.line_edit_vsintegracao = self.create_line_edit(
            placeholder="versão do VsIntegracao"
        )
        self.horizontal_layout_vsintegracao.addWidget(self.line_edit_vsintegracao)
        
        self.line_edit_version_mycommerce_release = self.create_line_edit(
            placeholder="versão do MyCommerce"
        )
        self.horizontal_layout_release.addWidget(self.line_edit_version_mycommerce_release)
        self.line_edit_version_mycommerce_release.setText(
            LatestVersion().latest_release_version_text())

        self.process_input(self.line_edit_version_mycommerce_release)
        
        self.line_edit_messages_fixes = self.create_text_edit(
            placeholder="Mensagens ajustes",
        )
        # ajusta a altura e largura do line edit conforme for inserido o texto
        self.line_edit_messages_fixes.setMinimumHeight(200)
        self.line_edit_messages_fixes.textChanged.connect(lambda:self.resize_text_edit(self.line_edit_messages_fixes))
        self.horizontal_layout_messages.addWidget(self.line_edit_messages_fixes)
        
        
        # passa para o proximo line_edit quando o usuario pressionar enter
        self.line_edit_return_pressed(self.line_edit_mycommerce_pdv_version, self.line_edit_mylocacao_version)
        self.line_edit_return_pressed(self.line_edit_mylocacao_version, self.line_edit_mypet)
        self.line_edit_return_pressed(self.line_edit_mypet, self.line_edit_myzap)
        self.line_edit_return_pressed(self.line_edit_myzap, self.line_edit_vsintegracao)
        self.line_edit_return_pressed(self.line_edit_vsintegracao, self.line_edit_version_mycommerce_release)
        self.line_edit_return_pressed(self.line_edit_version_mycommerce_release, self.line_edit_mycommerce_pdv_version)

    def line_edit_return_pressed(self, line_edit, next_focus):
        line_edit.returnPressed.connect(lambda: self.process_input(line_edit))
        line_edit.returnPressed.connect(lambda:next_focus.setFocus())
     
    def process_input(self,line_edit ):
        current_text = line_edit.text()
        if current_text != '...':
            # Adicionando zeros à esquerda conforme necessário
            parts = current_text.split('.')
            formatted_parts = []
            i = 1
            for part in parts:
                if i < 4:
                    part = part.zfill(2)  
                elif i == 4:
                    part = part.zfill(4)
                formatted_parts.append(part)
                i += 1

            formatted_text = '.'.join(formatted_parts)
            line_edit.setText(formatted_text)
        
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
    
    def release_version(self):
        pass
    
    def create_post(self):
        
        list_credentials = [
            self.bitrix_username,
            self.bitrix_password,
            self.forum_username,
            self.forum_password
        ]

        for credential in list_credentials:
            if credential == 'default':
                self.show_dialog('Você precisa configurar as credenciais antes de criar o post')
                self.credentials_window = DialogCredentialsPosts(self)
                self.get_configs_forums()
                break
            
        message = self.copy_all_text_to_clipboard(notcopy=True)
        # confirma antes de executar o script
        if self.show_confirmation_dialog():
            BrowserController(
                    message_version=message,
                    bitrix_username=self.bitrix_username,
                    bitrix_passwd=self.bitrix_password,
                    forum_username=self.forum_username,
                    forum_passwd=self.forum_password
                    )
        else:
            print(2)

    def copy_post_compatibilities(self, show_dialog = True):
        
        mycommerce_pdv = self.line_edit_mycommerce_pdv_version.text()
        mylocacao = self.line_edit_mylocacao_version.text()
        mypet = self.line_edit_mypet.text()
        myzap = self.line_edit_myzap.text()
        vsintegracao = self.line_edit_vsintegracao.text()
        list_messages = []   
        message_mylocacao = ''
        message_mypet = ''
        message_myzap = ''
        message_vsintegracao = ''
        message_mycommerce_pdv = ''
        
        #mycommerce_pdv
        if self.checkbox_compativel_mycommerce_pdv.isChecked():
            if mycommerce_pdv != '...':
                message_mycommerce_pdv = f'\nCompatível com a versão [b]{mycommerce_pdv}[/b] do [b]MyCommerce PDV[/b].'
        else:
            message_mycommerce_pdv = '\n[b]Não compatível[/b] com o [b]MyCommerce PDV[/b].'
        if message_mycommerce_pdv:  
            list_messages.append(message_mycommerce_pdv)
        
        #mylocacao  
        if self.checkbox_compativel_mylocacao.isChecked():
            if mylocacao != '...':
                message_mylocacao = f'\nCompatível com a versão [b]{mylocacao}[/b] do [b]MyLocação[/b].'
        else:
            message_mylocacao = '\n[b]Não compatível[/b] com o [b]MyLocação[/b].' 
        if message_mylocacao:
            list_messages.append(message_mylocacao)

        #mypet
        if self.checkbox_compativel_mypet.isChecked():
            if mypet != '...':
                message_mypet = f'\nCompatível com a versão [b]{mypet}[/b] do [b]MyPet[/b].'
        else:
            message_mypet = '\n[b]Não compatível[/b] com o [b]MyPet[/b].'
        if message_mypet:
            list_messages.append(message_mypet)
        
        #myzap
        if self.checkbox_compativel_myzap.isChecked():
            if myzap != '...':
                message_myzap = f'\nCompatível com a versão [b]{myzap}[/b] do [b]MyZap[/b].'
        else:
            message_myzap = '\n[b]Não compatível[/b] com o [b]MyZap[/b].'
        if message_myzap:
            list_messages.append(message_myzap)
        
        #vsintegracao
        if self.checkbox_compativel_vsintegracao.isChecked():
            if vsintegracao != '...':
                message_vsintegracao = f'\nCompatível com a versão [b]{vsintegracao}[/b] do [b]VsIntegrações[/b].'
        else:
            message_vsintegracao = '\n[b]Não compatível[/b] com o [b]VsIntegrações[/b].'
        if message_vsintegracao:
            list_messages.append(message_vsintegracao)
        
        i=0
        for item in list_messages:
            if item:
                if i==0:
                    final_message = item
                else:
                    final_message += item
                i+=1
        print(show_dialog)
        if show_dialog:  
            self.copy_to_clipboard(str(final_message))
            self.show_dialog('Mensagem copiada para a área de transferência: \n'+ final_message)
        else:
            try:
                return final_message
            except:
                print('sem mensagem final')

    def resize_text_edit(self, text_edit):
        # # TODO
        # document_height = text_edit.size().height()
        # document_width = text_edit.size().width()
        # text_edit.setMinimumSize(document_width, document_height)
        # print(document_height)
        pass

    def copy_all_text_to_clipboard(self, notcopy = False):
        mycommerce_version = self.line_edit_version_mycommerce_release.text()
        initial_message = self.line_edit_messages_fixes.toPlainText()
        # Olá! Versão 9.11.08.0000 do MyCommerce disponível para atualizações. 

        # INCONSISTÊNCIAS RELATADAS POR CLIENTES
        # 142545 - Ajustada inconsistência no relatório de ordem de entrega

        # Compatível com a versão 3.33.33.3333 do MyCommerce PDV. 

        # Atenciosamente, Vitor Hugo Borges Dos Santos.
        message_compatibilities = self.copy_post_compatibilities(show_dialog=False)
        if not self.checkbox_history_of_version.isChecked():
            if initial_message:
                if message_compatibilities is not None:
                    parts_of_text = initial_message.split('MyCommerce PDV[/b].')
                    print(parts_of_text, '\n\n\n',parts_of_text[0])
                    parts_of_text[0] += 'MyCommerce PDV[/b]'
                    parts_of_text[0] += message_compatibilities
                    final_message = ''.join(parts_of_text)
                    print(final_message)
                    if notcopy:
                        return final_message
                    else:
                        self.copy_to_clipboard(final_message)
                        self.show_dialog('Mensagem copiada para a área de transferência')
        else:
            if initial_message:
                if message_compatibilities is not None:
                    text_greetings = f"""Olá! Versão {mycommerce_version} do MyCommerce disponível para atualizações."""
                    text_obs = """Atenciosamente, Vitor Hugo Borges Dos Santos."""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    window = VersionReleaseInterface()
    window.show()
    app.exec()