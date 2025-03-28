from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from interfaces.base_window import BaseWindow
from components.last_version_finder import LatestVersion

from PySide6.QtWidgets import (
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QFrame
)

class WidgetReleaseMycommerce(BaseWindow):
    def __init__(self, parent=None):
        super(WidgetReleaseMycommerce, self).__init__(parent)
        self.latest_version_handler = LatestVersion()
        self.setup_ui()
        
        
    def setup_ui(self):
        self.main_container = QWidget()
        self.main_layout = QHBoxLayout(self.main_container)
        
        self.container_secao1 = QWidget()
        self.container_secao2 = QWidget()
        
        self.secao_vertical1 = QVBoxLayout(self.container_secao1)
        self.secao_vertical2 = QVBoxLayout(self.container_secao2)
        
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
        self.horizontal_layout_vs_services_myzap = QHBoxLayout()
        self.horizontal_layout_optoclinic = QHBoxLayout()
        
        self.secao_vertical1.addLayout(self.horizontal_layout_mycommerce_pdv)
        self.secao_vertical1.addLayout(self.horizontal_layout_mylocacao)
        self.secao_vertical1.addLayout(self.horizontal_layout_mypet)
        self.secao_vertical1.addLayout(self.horizontal_layout_myzap)
        
        self.secao_vertical2.addLayout(self.horizontal_layout_vsintegracao)
        self.secao_vertical2.addLayout(self.horizontal_layout_mycomanda)
        self.secao_vertical2.addLayout(self.horizontal_layout_vs_services_myzap)
        self.secao_vertical2.addLayout(self.horizontal_layout_optoclinic)
        
        # ADICIONA LINHA DIVISÓRIA 
        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.VLine)  # Linha vertical
        self.divider.setFrameShadow(QFrame.Sunken)
        self.divider.setLineWidth(3)  # Espessura da linha
        self.divider.setStyleSheet("""
            QFrame {
                margin: 0px 1px;
                background-color: white;
                min-height: 100%;
            }
        """)

        self.main_layout.addWidget(self.container_secao1)
        self.main_layout.addWidget(self.divider)  # Adiciona a linha divisória
        self.main_layout.addWidget(self.container_secao2)
        
        self.main_layout.setStretch(0, 1)  # container_secao1 ocupa 1 parte
        self.main_layout.setStretch(1, 0)  # linha divisória não estica
        self.main_layout.setStretch(2, 1)  # container_secao2 ocupa 1 parte
        
        self.create_all_checkboxes()
        self.create_all_labels()
        self.create_all_line_edits()
        
        # Adiciona espaçador
        self.spacer_horizontal = QSpacerItem(100, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout_release.addItem(self.spacer_horizontal)
        
        self.setCentralWidget(self.main_container)
        
    
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
        
        self.checkbox_compativel_services_myzap =self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_vs_services_myzap.addWidget(self.checkbox_compativel_services_myzap)

        self.checkbox_compativel_mycomanda = self.create_checkbox(text= "Compatível")
        self.horizontal_layout_mycomanda.addWidget(self.checkbox_compativel_mycomanda)
        
        self.checkbox_compativel_optoclinic = self.create_checkbox(text= "Compatível")
        self.horizontal_layout_optoclinic.addWidget(self.checkbox_compativel_optoclinic)
        
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
            text="VsIntegrações: "
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
        
        self.label_vs_services_myzap = self.create_label(
            text="VsServices MyZap: "
        )
        self.horizontal_layout_vs_services_myzap.addWidget(self.label_vs_services_myzap)
        
        self.label_optoclinic = self.create_label(
            text="Optoclinic: "
        )
        self.horizontal_layout_optoclinic.addWidget(self.label_optoclinic)
        
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
        
        self.line_edit_vs_services_myzap = self.create_line_edit(
            placeholder="versão do vs.Services MyZap",
            set_text=self.latest_version_handler.latest_release_version_text_myzap()
        )
        self.horizontal_layout_vs_services_myzap.addWidget(self.line_edit_vs_services_myzap)
        
        self.line_edit_optoclinic = self.create_line_edit(
            placeholder="versão do Optoclinic"
        )
        self.horizontal_layout_optoclinic.addWidget(self.line_edit_optoclinic)
        
        self.process_input(self.line_edit_version_mycommerce_release)
        self.process_input(self.line_edit_mycommerce_pdv_version)
        self.process_input(self.line_edit_mylocacao_version)
        self.process_input(self.line_edit_mypet)
        self.process_input(self.line_edit_myzap)
        self.process_input(self.line_edit_vsintegracao)
        self.process_input(self.line_edit_mycomanda)
        self.process_input(self.line_edit_vs_services_myzap)
        self.process_input(self.line_edit_optoclinic)

        # passa para o proximo line_edit quando o usuario pressionar enter
        self.line_edit_return_pressed(self.line_edit_mycommerce_pdv_version, self.line_edit_mylocacao_version)
        self.line_edit_return_pressed(self.line_edit_mylocacao_version, self.line_edit_mypet)
        self.line_edit_return_pressed(self.line_edit_mypet, self.line_edit_myzap)
        self.line_edit_return_pressed(self.line_edit_myzap, self.line_edit_vsintegracao)
        self.line_edit_return_pressed(self.line_edit_vsintegracao, self.line_edit_mycomanda)
        self.line_edit_return_pressed( self.line_edit_mycomanda, self.line_edit_vs_services_myzap)
        self.line_edit_return_pressed(self.line_edit_mycomanda, self.line_edit_vs_services_myzap)
        self.line_edit_return_pressed(self.line_edit_vs_services_myzap, self.line_edit_optoclinic)
        self.line_edit_return_pressed(self.line_edit_optoclinic, self.line_edit_version_mycommerce_release)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = WidgetReleaseMycommerce()
    window.show()
    app.exec()