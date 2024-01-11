import os
import sys
path = os.path.abspath('./')
sys.path.append(path)

from interfaces.base_window import BaseWindow
from interfaces.credentials_window import DialogCredentialsPosts
from components.last_version_finder import LatestVersion
from interfaces.thread_pyside import DownloadThread

from PySide6.QtCore import Qt 
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QProgressDialog
)

class VersionReleaseInterface(BaseWindow):
    def __init__(self, parent=None):
        super(VersionReleaseInterface, self).__init__(parent)
        self.latest_version_handler = LatestVersion()
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Liberar Versão")
        width = 650
        height = 700
        self.setFixedSize(width, height)
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
        self.horizontal_layout_mycomanda = QHBoxLayout()
        final_list =[
            self.horizontal_layout_release,self.horizontal_layout_mycommerce_pdv,
            self.horizontal_layout_mylocacao, 
            self.horizontal_layout_mypet, self.horizontal_layout_myzap, self.horizontal_layout_vsintegracao,
            self.horizontal_layout_mycomanda,
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

        self.checkbox_final_version = self.create_checkbox(
            text="Versão final",
            marked=False)
        self.horizontal_history_version.addWidget(self.checkbox_final_version)

        self.checkbox_compativel_mycomanda = self.create_checkbox(text= "Compatível")
        self.horizontal_layout_mycomanda.addWidget(self.checkbox_compativel_mycomanda)
        
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
        
        self.label_mycomanda = self.create_label(
            text="MyComanda: "
        )
        self.horizontal_layout_mycomanda.addWidget(self.label_mycomanda)
        
    def create_all_line_edits(self):
        self.line_edit_mycommerce_pdv_version = self.create_line_edit(
            placeholder="versão do MyCommerce PDV",
            set_text=self.latest_version_handler.latest_release_version_text_pdv()
        )
        self.horizontal_layout_mycommerce_pdv.addWidget(self.line_edit_mycommerce_pdv_version)
        
        self.line_edit_mylocacao_version = self.create_line_edit(
            placeholder="versão do MyLocação",
            set_text=self.latest_version_handler.latest_release_version_text_mylocacao()
        )
        self.horizontal_layout_mylocacao.addWidget(self.line_edit_mylocacao_version)

        self.line_edit_mypet = self.create_line_edit(
            placeholder="versão do MyPet",
            set_text=self.latest_version_handler.latest_release_version_text_mypet()
        )
        self.horizontal_layout_mypet.addWidget(self.line_edit_mypet)
        
        self.line_edit_myzap = self.create_line_edit(
            placeholder="versão do MyZap",
            set_text=self.latest_version_handler.latest_release_version_text_myzap()
        )
        self.horizontal_layout_myzap.addWidget(self.line_edit_myzap)
        
        self.line_edit_vsintegracao = self.create_line_edit(
            placeholder="versão do VsIntegracao",
            set_text=self.latest_version_handler.latest_release_version_text_vsintegracoes()
        )
        self.horizontal_layout_vsintegracao.addWidget(self.line_edit_vsintegracao)
        
        self.line_edit_version_mycommerce_release = self.create_line_edit(
            placeholder="versão do MyCommerce",
            set_text=self.latest_version_handler.latest_release_version_text()
        )
        self.horizontal_layout_release.addWidget(self.line_edit_version_mycommerce_release)

        self.line_edit_mycomanda = self.create_line_edit(placeholder="Versão Mycomanda")
        self.horizontal_layout_mycomanda.addWidget(self.line_edit_mycomanda)
        
        self.process_input(self.line_edit_version_mycommerce_release)
        self.process_input(self.line_edit_mycommerce_pdv_version)
        self.process_input(self.line_edit_mylocacao_version)
        self.process_input(self.line_edit_mypet)
        self.process_input(self.line_edit_myzap)
        self.process_input(self.line_edit_vsintegracao)
        self.process_input(self.line_edit_mycomanda)
        
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
        self.line_edit_return_pressed(self.line_edit_version_mycommerce_release, self.line_edit_mycomanda)
        self.line_edit_return_pressed(self.line_edit_mycomanda, self.line_edit_mycommerce_pdv_version)

    def line_edit_return_pressed(self, line_edit, next_focus):
        line_edit.returnPressed.connect(lambda: self.process_input(line_edit))
        line_edit.returnPressed.connect(lambda:next_focus.setFocus())
     
    def process_input(self,line_edit):
        current_text = line_edit.text()
        if current_text != '...':
            parts = current_text.split('.')
            formatted_text = self.add_zero_to_left(parts)
            line_edit.setText(formatted_text)

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
        is_final_version = self.checkbox_final_version.isChecked()
        self.get_configs_forums()
        list_credentials = [
            self.bitrix_username,
            self.bitrix_password,
            self.forum_username,
            self.forum_password
        ]
        if not self.verify_if_has_login_configs(list_credentials):
            self.show_dialog('Você precisa configurar as credenciais antes de criar o post')
            self.credentials_window = DialogCredentialsPosts(self)
            self.get_configs_forums()
        else:
            message = self.copy_all_text_to_clipboard(notcopy=True)
            # confirma antes de executar o script
            if message:
                if self.show_confirmation_dialog():
                    topic_name = None
                    if is_final_version:
                        topic_name = self.dialog_input('Coloque a mensagem de tópico do fórum, exemplo: 9.12.x'
                                    )
                    self.start_automation_create_post(topic_name, is_final_version, message)
            else:
                self.show_dialog('Não há mensagem para publicar') 
            
    def verify_if_has_login_configs(self, list_credentials):
        for credential in list_credentials: 
            if credential == 'default':
                return False
        return True
    
    def start_automation_create_post(self, topic_name, is_final_version, message):
        if topic_name and is_final_version or not topic_name and not is_final_version:
            self.progress_dialog = QProgressDialog(self) 
            self.config_window_progress()
            bitrix_username = self.cripter.decrypt(self.bitrix_username)
            bitrix_passwd = self.cripter.decrypt(self.bitrix_password)
            forum_username = self.cripter.decrypt(self.forum_username)
            forum_password= self.cripter.decrypt(self.forum_password)
            self.thread_create_post = DownloadThread(
                thread_create_post=True,
                message=message,
                bitrix_username=bitrix_username,
                bitrix_password=bitrix_passwd,
                forum_username= forum_username,
                forum_password=forum_password,
                final_version=is_final_version,
                topic_name_of_final_version=topic_name
                )
            self.thread_create_post.download_finished.connect(self.thread_finished)
            self.thread_create_post.start()
            
    def config_window_progress(self):
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setWindowTitle('Criando Posts')
        self.progress_dialog.setLabelText('Aguarde enquanto é criado os posts')
        self.progress_dialog.setRange(0, 0)    

    def thread_finished(self):
        self.progress_dialog.cancel()
        self.show_dialog('Posts criados com sucesso')
        
    def copy_post_compatibilities(self, show_dialog = True):
        mycommerce_pdv = self.line_edit_mycommerce_pdv_version.text()
        mylocacao = self.line_edit_mylocacao_version.text()
        mypet = self.line_edit_mypet.text()
        myzap = self.line_edit_myzap.text()
        vsintegracao = self.line_edit_vsintegracao.text()
        mycomanda = self.line_edit_mycomanda.text()
        list_of_compatibilities = ['MyCommerce PDV', 'MyLocação', 'MyPet', 'MyZap', 'VsIntegrações', 'MyComanda']
        list_of_versions = [mycommerce_pdv, mylocacao, mypet, myzap, vsintegracao, mycomanda]
        list_of_is_compatible = [
            self.checkbox_compativel_mycommerce_pdv.isChecked(),
            self.checkbox_compativel_mylocacao.isChecked(),
            self.checkbox_compativel_mypet.isChecked(),
            self.checkbox_compativel_myzap.isChecked(),
            self.checkbox_compativel_vsintegracao.isChecked(),
            self.checkbox_compativel_mycomanda.isChecked()
            ]
        list_messages = []   
        message_mylocacao = ''
        message_mypet = ''
        message_myzap = ''
        message_vsintegracao = ''
        message_mycommerce_pdv = ''
        message_mycomanda = ''
        list_messages_raw = [message_mycommerce_pdv, message_mylocacao, message_mypet,message_myzap, message_vsintegracao, message_mycomanda  ]

        for index, version in enumerate(list_of_versions):
            name_of_program = list_of_compatibilities[index]
            is_compatible = list_of_is_compatible[index]
            
            if version != '...':
                text1_compatible = f'\nCompatível com a versão '
                text1_not_compatible = f'\nNão compatível com a versão '
                text2 = f'[b]{version}[/b] do [b]{name_of_program}[/b].'
                
                if is_compatible:
                    message = text1_compatible + text2
                else:
                    message = text1_not_compatible + text2
                list_messages.append(message)
                list_messages_raw[index] = message
                
        index_itens_message=0
        for item in list_messages:
            if item:
                if index_itens_message==0:
                    final_message = item
                else:
                    final_message += item
                index_itens_message+=1
        print(show_dialog)
        if show_dialog:  
            self.copy_to_clipboard(str(final_message))
            self.show_dialog('Mensagem copiada para a área de transferência: \n'+ final_message)
        else:
            try:
                return final_message
            except:
                self.file_handler.add_new_logs('sem mensagem final')
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
        is_final_version = self.checkbox_final_version.isChecked()
        
        message_compatibilities = self.copy_post_compatibilities(show_dialog=False)
        if not self.checkbox_history_of_version.isChecked():
            if initial_message:
                if message_compatibilities:
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
                return self.cook_message(is_final_version, initial_message, mycommerce_version, message_compatibilities, notcopy)
            else:
                return self.cook_message(is_final_version, initial_message, mycommerce_version, message_compatibilities, notcopy)
    
    def cook_message(self, is_final_version, initial_message, mycommerce_version, message_compatibilities, notcopy):
        if message_compatibilities:   
            message_forum = self.make_text_for_forum(initial_message)
            text_obs = '\n\nAtenciosamente, Vitor Hugo Borges Dos Santos.'
            if not is_final_version:
                text_greetings = f'Olá! Versão [b]{mycommerce_version}[/b] do [b]MyCommerce[/b] disponível para atualizações.\n\n'
                final_message = text_greetings + message_forum + '\n'+ message_compatibilities + text_obs
                if notcopy:
                    return final_message
                else:
                    self.copy_to_clipboard(final_message)
                    self.show_dialog('Mensagem copiada para a área de transferência')
            else: 
                text_greetings = f'Olá! Versão final [b]{mycommerce_version}[/b] do [b]MyCommerce[/b] disponível para atualizações.\n\n'
                if message_forum:
                    final_message = text_greetings + message_forum + '\n'+ message_compatibilities + text_obs
                else:
                    final_message = text_greetings + message_compatibilities + text_obs
                if notcopy:
                    return final_message
                else:
                    self.copy_to_clipboard(final_message)
                    self.show_dialog('Mensagem copiada para a área de transferência')
                
    def make_text_for_forum(self, text):
        list_messages = text.split('\n')
        message_forum = []
        relatadas_por_clientes = 'INCONSISTÊNCIAS RELATADAS POR CLIENTES:'
        relatadas_por_clientes_forum = '[b]INCONSISTÊNCIAS RELATADAS POR CLIENTES:[/b]'
        inconsistencias_encontradas_internamente = 'INCONSISTÊNCIAS ENCONTRADAS INTERNAMENTE:'
        inconsistencias_encontradas_internamente_forum = '[b]INCONSISTÊNCIAS ENCONTRADAS INTERNAMENTE:[/b]'
        customizacoes_incluidas = 'CUSTOMIZAÇÕES INCLUSAS:'
        customizacoes_incluidas_forum = '[b]CUSTOMIZAÇÕES INCLUSAS:[/b]'
        
        final_message= []
        
        for message in list_messages:
            if message:
                if message == relatadas_por_clientes:
                    message = relatadas_por_clientes_forum
                elif message == inconsistencias_encontradas_internamente:
                    message = inconsistencias_encontradas_internamente_forum
                elif message == customizacoes_incluidas:
                    message = customizacoes_incluidas_forum
                message_forum.append(message)
            else:
                message_forum.append(message)
            
        for message in message_forum:
            if message:
                print(message)
                if message == relatadas_por_clientes_forum or  message == inconsistencias_encontradas_internamente_forum or message == customizacoes_incluidas_forum:
                    final_message.append(message)
                else:
                    spli_task = message.split(' - ')
                    spli_task[0] = '[b]' + spli_task[0] + '[/b]'
                    message = ' - '.join(spli_task)
                    final_message.append(message)
            else:
                final_message.append(message)
        return '\n'.join(final_message)
                               
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VersionReleaseInterface()
    window.show()
    app.exec()