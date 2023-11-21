import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from interfaces.base_window import BaseWindow
from pywinauto import application
from PySide6.QtCore import Qt

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
        # Mensagem padrão
        # pdv ja esta certo
        # Compatível com a versão 3.60.65.0000 do MyCommerce PDV. 
        # vai precisar configurar para as de baixo
        # Compatível com a versão 9.10.00.0000 do MyLocação.
        # Compatível com a versão 9.08.02.0000 do MyPet.
        # Compatível com a versão 2.11.02.0000 do MyZap.
        # Compatível com a versão 6.10.02.0000 do VsIntegrações.
        self.setup_ui()
    
    # vai ter um botão para liberar seguindo todos os passos automaticamente, 
    # e vai ter um botão para liberar manualmente, parte por parte
    
    def setup_ui(self):
        self.setWindowTitle("Liberar Versão")
        self.horizontal_layout_release = QHBoxLayout()
        self.horizontal_layout_mylocacao = QHBoxLayout()
        self.horizontal_layout_mypet = QHBoxLayout()
        self.horizontal_layout_myzap = QHBoxLayout()
        self.horizontal_layout_vsintegracao = QHBoxLayout()
        
        final_list =[
            self.horizontal_layout_release, self.horizontal_layout_mylocacao, 
            self.horizontal_layout_mypet, self.horizontal_layout_myzap, self.horizontal_layout_vsintegracao]
        
        print(final_list)
        self.create_all_checkboxes()
        self.create_all_labels()
        self.create_all_line_edits()
        self.create_all_buttons()
        self.create_layouts(final_list)

    def create_all_buttons(self):
        self.button_release_version = self.create_button(
            text="Liberar Versão", function=self.release_version)
        self.horizontal_layout_release.addWidget(self.button_release_version)

    def create_all_checkboxes(self):
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
        

    def create_all_labels(self):
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
        
    def create_all_line_edits(self):
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
        
        # passa para o proximo line_edit quando o usuario pressionar enter
        self.line_edit_return_pressed(self.line_edit_mylocacao_version, self.line_edit_mypet)
        self.line_edit_return_pressed(self.line_edit_mypet, self.line_edit_myzap)
        self.line_edit_return_pressed(self.line_edit_myzap, self.line_edit_vsintegracao)
        self.line_edit_return_pressed(self.line_edit_vsintegracao, self.line_edit_mylocacao_version)

    def line_edit_return_pressed(self, line_edit, next_focus):
        line_edit.returnPressed.connect(lambda: self.process_input(line_edit))
        line_edit.returnPressed.connect(lambda:next_focus.setFocus())
        
        print(next_focus)
        
    def process_input(self,line_edit ):
        current_text = line_edit.text()
        print(current_text)
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
         
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    window = VersionReleaseInterface()
    window.show()
    app.exec()