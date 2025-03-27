from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from interfaces.base_window import BaseWindow
from interfaces.credentials_window import DialogCredentialsPosts
from components.last_version_finder import LatestVersion
from interfaces.thread_pyside import DownloadThread
from interfaces.widget_release_myfrota import WidgetReleaseMyfrota
from interfaces.widget_release_mycommerce import WidgetReleaseMycommerce
from interfaces.widget_release_mypet import WidgetReleaseMypet

from PySide6.QtCore import Qt 
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QProgressDialog
)
from random import choice
class VersionReleaseInterface(BaseWindow):
    def __init__(self, parent=None):
        super(VersionReleaseInterface, self).__init__(parent)
        self.keyPressEvent = self.key_pressed_handle
        self.latest_version_handler = LatestVersion()

        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Liberar Versão")
        width = 730
        
        self.get_configs_forums()
        if self.name_of_program =='Mycommerce':
            height = 920
            self.widget_mycommerce = WidgetReleaseMycommerce()
            final_list = [self.widget_mycommerce]
            self.create_layouts(final_list)
        elif self.name_of_program == 'MyFrota':
            height = 650
            self.widget_myfrota = WidgetReleaseMyfrota()
            final_list = [self.widget_myfrota]
        elif self.name_of_program == 'MyPet':
            height = 650
            self.widget_mypet = WidgetReleaseMypet()
            final_list = [self.widget_mypet]
        elif self.name_of_program == 'default' or self.name_of_program == 'Mycommerce PDV':
            height = 650
            final_list = []   
        self.setFixedSize(width, height)
        
        self.horizontal_layout_manual_release = QHBoxLayout()
        self.horizontal_layout_messages = QHBoxLayout()
        self.horizontal_history_version = QHBoxLayout()
        final_list.append(self.horizontal_history_version)
        final_list.append(self.horizontal_layout_messages)
        final_list.append(self.horizontal_layout_manual_release)
        
        self.create_all_checkboxes()
        self.create_all_buttons()
        self.create_all_line_edits()
        self.create_layouts(final_list)

    def create_all_buttons(self):
        self.button_config = self.create_button(
            text="Configurações", function=self.open_credentials_window
        )
        self.horizontal_history_version.addWidget(self.button_config)
        
        # self.button_release_version = self.create_button(
        #     text="Liberar Versão", function=self.release_version)
        # self.horizontal_layout_release.addWidget(self.button_release_version)
        
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
        
        self.button_cancel = self.create_button(
            text = "Cancelar/Sair" , function=self.close_reset_the_class
        )
        self.horizontal_layout_manual_release.addWidget(self.button_cancel)
        
    def create_all_checkboxes(self):
        self.checkbox_final_version = self.create_checkbox(
            text="Versão final",
            marked=False)
        self.horizontal_history_version.addWidget(self.checkbox_final_version)
        

    def create_all_line_edits(self):
        self.line_edit_messages_fixes = self.create_text_edit(
            placeholder="Mensagens ajustes",
        )
        
        # ajusta a altura e largura do line edit conforme for inserido o texto
        self.line_edit_messages_fixes.setMinimumHeight(300)
        self.line_edit_messages_fixes.textChanged.connect(lambda:self.resize_text_edit(self.line_edit_messages_fixes))
        self.horizontal_layout_messages.addWidget(self.line_edit_messages_fixes)
        
        
    def release_version(self):
        pass
    
    def open_credentials_window(self):
        self.credentials_window = DialogCredentialsPosts(self)
    
    def create_post(self):
        is_final_version = self.checkbox_final_version.isChecked()
        
        if self.name_of_program == 'Mycommerce':
            version_software_release = self.widget_mycommerce.line_edit_version_mycommerce_release.text()
        elif self.name_of_program == 'MyFrota':
            version_software_release = self.widget_myfrota.line_edit_version_myfrota_release.text()
        elif self.name_of_program == 'MyPet':
            version_software_release = self.widget_mypet.line_edit_version_mypet_release.text()
        
        self.get_configs_forums()
        list_credentials = [
            self.bitrix_username,
            self.bitrix_password,
            self.forum_username,
            self.forum_password
        ]
        if not self.verify_if_has_login_configs(list_credentials):
            self.show_dialog('Você precisa configurar as credenciais antes de criar o post')
            self.open_credentials_window()
            self.get_configs_forums()
        else:
            message = self.copy_all_text_to_clipboard(notcopy=True)
            # confirma antes de executar o script
            if message:
                if self.show_confirmation_dialog('Você tem certeza que deseja continuar?'):
                    topic_name = None
                    if is_final_version:
                        topic_name = self.dialog_input('Coloque a mensagem de tópico do fórum, exemplo: 9.12.x'
                                    )
                    self.file_handler.add_new_logs(f'Criando posts da versão: {version_software_release}')
                    self.start_automation_create_post(topic_name, is_final_version, message)
            else:
                self.file_handler.add_new_logs('Não há mensagem para publicar')
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
            print(is_final_version)
            self.thread_create_post = DownloadThread(
                thread_create_post=True,
                message=message,
                bitrix_username=bitrix_username,
                bitrix_password=bitrix_passwd,
                forum_username= forum_username,
                forum_password=forum_password,
                final_version=is_final_version,
                topic_name_of_final_version=topic_name,
                name_of_program=self.name_of_program
                )
            self.thread_create_post.download_finished.connect(self.thread_finished)
            self.thread_create_post.error.connect(self.error_creating_post)
            self.thread_create_post.start()
    
    def error_creating_post(self):
        self.progress_dialog.cancel()
        self.show_dialog(f'Erro ao criar o post: \n {self.thread_create_post.msg_error}')
        
    def config_window_progress(self):
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setWindowTitle('Criando Posts')
        self.progress_dialog.setLabelText('Aguarde enquanto é criado os posts')
        self.progress_dialog.setRange(0, 0)    

    def thread_finished(self):
        self.progress_dialog.cancel()
        self.show_dialog('Posts criados com sucesso')
        self.file_handler.add_new_logs('Posts criados com sucesso')
        
    def copy_post_compatibilities(self, show_dialog = True):
        if self.name_of_program == 'Mycommerce':
            mycommerce_pdv = self.widget_mycommerce.line_edit_mycommerce_pdv_version.text()
            mylocacao = self.widget_mycommerce.line_edit_mylocacao_version.text()
            mypet = self.widget_mycommerce.line_edit_mypet.text()
            myzap = self.widget_mycommerce.line_edit_myzap.text()
            vsintegracao = self.widget_mycommerce.line_edit_vsintegracao.text()
            mycomanda = self.widget_mycommerce.line_edit_mycomanda.text()
            vs_services_myzap = self.widget_mycommerce.line_edit_vs_services_myzap.text()
            optclinic = self.widget_mycommerce.line_edit_optoclinic.text()
            list_of_compatibilities = [
                f'MyCommerce PDV',
                f'MyLocação',
                f'MyPet',
                f'MyZap',
                f'VsIntegrações',
                f'MyComanda',
                f'vs.Services MyZap',
                f'Optoclinic'
                ]
            list_of_versions = [mycommerce_pdv, mylocacao, mypet, myzap, vsintegracao, mycomanda, vs_services_myzap, optclinic]
            list_of_is_compatible = [
                self.widget_mycommerce.checkbox_compativel_mycommerce_pdv.isChecked(),
                self.widget_mycommerce.checkbox_compativel_mylocacao.isChecked(),
                self.widget_mycommerce.checkbox_compativel_mypet.isChecked(),
                self.widget_mycommerce.checkbox_compativel_myzap.isChecked(),
                self.widget_mycommerce.checkbox_compativel_vsintegracao.isChecked(),
                self.widget_mycommerce.checkbox_compativel_mycomanda.isChecked(),
                self.widget_mycommerce.checkbox_compativel_services_myzap.isChecked(),
                self.widget_mycommerce.checkbox_compativel_optoclinic.isChecked()
                ]
            message_mylocacao = ''
            message_mypet = ''
            message_myzap = ''
            message_vsintegracao = ''
            message_mycommerce_pdv = ''
            message_mycomanda = ''
            message_vs_services_myzap = ''
            # list_messages_raw = [message_mycommerce_pdv, message_mylocacao, message_mypet,message_myzap, message_vsintegracao, message_mycomanda,  message_vs_services_myzap ]
        
        elif self.name_of_program == 'MyFrota':
            mycommerce_version = self.widget_myfrota.line_edit_mycommerce_version.text()
            list_of_compatibilities = ['Mycommerce']
            list_of_versions = [mycommerce_version]
            list_of_is_compatible = [
                self.widget_myfrota.checkbox_compativel_mycommerce.isChecked()
                ]
            message_myfrota = ''
            # list_messages_raw = [message_myfrota]
            
        elif self.name_of_program == 'MyPet':
            mycommerce_version = self.widget_mypet.line_edit_mycommerce_version.text()
            list_of_compatibilities = ['Mycommerce']
            list_of_versions = [mycommerce_version]
            list_of_is_compatible = [
                self.widget_mypet.checkbox_compativel_mycommerce.isChecked()
                ]
            message_mypet = ''
            # list_messages_raw = [message_mypet]
  
        final_message = ''
        compatible_messages = []
        not_compatible_messages = []
        
        inicio_message_list = '[b]Compatibilidades[/b]'
            
        
        for index, version in enumerate(list_of_versions):
            name_of_program = list_of_compatibilities[index]
            is_compatible = list_of_is_compatible[index]
            
            if version != '...':
                compativel = f'Compatível com a versão [b]{version}[/b] do [b]{name_of_program}[/b]'
                nao_compativel = f'A versão [b]{version}[/b] do [b]{name_of_program}[/b]'
                if is_compatible:
                    compatible_messages.append(compativel)
                else:
                    not_compatible_messages.append(nao_compativel)
                
        if not_compatible_messages:
            final_message += f"Atenção: [b]Não[/b] compatível com: \n" + "\n".join(not_compatible_messages)  + "\n\n"
        
        if compatible_messages:
            final_message += f"{inicio_message_list}: \n" + "\n".join(compatible_messages)

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
        if self.name_of_program == 'Mycommerce':
            software_version = self.widget_mycommerce.line_edit_version_mycommerce_release.text()
        elif self.name_of_program == 'MyFrota':
            software_version = self.widget_myfrota.line_edit_version_myfrota_release.text()
        elif self.name_of_program == 'MyPet':
            software_version = self.widget_mypet.line_edit_version_mypet_release.text()
            
        initial_message = self.line_edit_messages_fixes.toPlainText()
        is_final_version = self.checkbox_final_version.isChecked()
        
        message_compatibilities = self.copy_post_compatibilities(show_dialog=False)

        if initial_message:
            return self.cook_message(is_final_version, software_version, message_compatibilities, notcopy, initial_message)
        else:
            return self.cook_message(is_final_version, software_version, message_compatibilities, notcopy)
    
    def cook_message(self, is_final_version, software_version, message_compatibilities, notcopy, initial_message = None):    
        # variações do incio do texto:
        inicio_list = f'Olá! Versão'
        final_list = 'disponível para atualizações.'

        if message_compatibilities:   
            if initial_message:
                message_forum = self.make_text_for_forum(initial_message)
                
            self.get_configs_forums()
            user_releaser = self.user_releaser
            user_releaser = str(user_releaser)
            name_of_program = self.name_of_program
            if user_releaser != 'default':
                user_releaser = user_releaser.capitalize()
                text_obs = f'\nAtenciosamente, {user_releaser}.'
            else:
                text_obs = '\nAtenciosamente, Vitor Hugo Borges Dos Santos.'
            if not is_final_version:
                # text_greetings = f'Olá! A versão [b]{software_version}[/b] do [b]{name_of_program}[/b] disponível para atualizações.{self.emoji_foguete}\n\n'
                text_greetings = f'{inicio_list} [b]{software_version}[/b] do [b]{name_of_program}[/b] {final_list}\n\n'
                
                if initial_message:
                    final_message = text_greetings + message_forum + '\n\n'+ message_compatibilities +'\n' + text_obs
                else:
                    final_message = text_greetings + message_compatibilities +'\n' + text_obs
                if notcopy:
                    return final_message
                else:
                    self.copy_to_clipboard(final_message)
                    self.show_dialog('Mensagem copiada para a área de transferência')
            else: 
                text_greetings = f'{inicio_list} final [b]{software_version}[/b] do [b]{name_of_program}[/b] {final_list}\n\n'
                if initial_message:
                    final_message = text_greetings + message_forum + '\n\n'+ message_compatibilities +'\n'+ text_obs
                else:
                    final_message = text_greetings + message_compatibilities +'\n'+ text_obs
                if notcopy:
                    return final_message
                else:
                    self.copy_to_clipboard(final_message)
                    self.show_dialog('Mensagem copiada para a área de transferência')
                
    def make_text_for_forum(self, text):
        list_messages = text.split('\n')
        message_forum = []

        relatadas_por_clientes = 'INCONSISTÊNCIAS RELATADAS POR CLIENTES:'
        relatadas_por_clientes_forum = f'[b]INCONSISTÊNCIAS RELATADAS POR CLIENTES:[/b]'
        inconsistencias_encontradas_internamente = 'INCONSISTÊNCIAS ENCONTRADAS INTERNAMENTE:'
        inconsistencias_encontradas_internamente_forum = f'[b]INCONSISTÊNCIAS ENCONTRADAS INTERNAMENTE:[/b]'
        customizacoes_incluidas = 'CUSTOMIZAÇÕES INCLUSAS:'
        customizacoes_incluidas_forum = f'[b]CUSTOMIZAÇÕES INCLUSAS:[/b]'
        
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
                    split_task = message.split(' - ')
                    split_task[0] = '[b]' + split_task[0] + '[/b]'
                    message = ' - '.join(split_task)
                    final_message.append(message)
                    #else:
                        
                    # # verifica se tem o tamanho do codigo de tarefas do sia
                    # if len(split_task[0]) == 6:
                    #     split_task[0] = ''
                    #     split_task = ' - '.join(split_task)
                    #     final_message.append(split_task)
                    # else:
                    #     final_message.append(f'[b]' + message + '[/b]')
            else:
                final_message.append(message)
        return '\n'.join(final_message)
    
    def close_reset_the_class(self):
        # fecha a janela e toda a construção desta classe
        self.close()
        self.destroy()
        self.parent().interface_version_releaser_is_open = False
        del self

    def open_credentials_window(self):
        self.credentials_window = DialogCredentialsPosts(self)
    
    def reset_layout(self):
        self.centralWidget().deleteLater() 
        self.clearLayout(self.layout_principal)
        
        self.setup_ui()
        
    def changed_program(self):
        texto_confirmacao = 'Verificado que o programa a ser liberado foi alterado\nDeseja continuar? (as alterações feitas serão perdidas!)'
        if self.show_confirmation_dialog(texto_confirmacao):
            self.reset_layout()
    
    
                          
if __name__ == "__main__":
    from sys import argv
    app = QApplication(argv)
    window = VersionReleaseInterface()
    window.show()
    app.exec()