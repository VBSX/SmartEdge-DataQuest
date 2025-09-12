from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from components.last_version_finder import LatestVersion
from interfaces.base_window import BaseWindow

from PySide6.QtWidgets import (
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy
)

class WidgetReleaseMyZap(BaseWindow):
    def __init__(self, parent=None):
        super(WidgetReleaseMyZap, self).__init__(parent)
        self.latest_version_handler = LatestVersion()
        self.setup_ui()
    
    def setup_ui(self):
        self.horizontal_layout_release = QHBoxLayout()
        self.horizontal_layout_mycommerce = QHBoxLayout()
        self.horizontal_layout_omniMulti = QHBoxLayout()
        final_list =[
            self.horizontal_layout_release,
            self.horizontal_layout_mycommerce,
            self.horizontal_layout_omniMulti
            ]
        
        self.create_all_checkboxes()
        self.create_all_labels()
        self.create_all_line_edits()
        
        self.horizontal_layout_release.addWidget(self.label_version_myzap)
        self.horizontal_layout_release.addWidget(self.line_edit_version_myzap_release)
        self.horizontal_layout_release.addWidget(self.label_version_vsServices_MyZap)
        self.horizontal_layout_release.addWidget(self.line_edit_version_vsServices_MyZap)
        
        self.horizontal_layout_mycommerce.addWidget(self.checkbox_compativel_mycommerce)
        self.horizontal_layout_mycommerce.addWidget(self.label_mycommerce)
        self.horizontal_layout_mycommerce.addWidget(self.line_edit_mycommerce_version)
        
        self.horizontal_layout_omniMulti.addWidget(self.checkbox_compativel_omniMulti)
        self.horizontal_layout_omniMulti.addWidget(self.label_omniMulti)
        self.horizontal_layout_omniMulti.addWidget(self.line_edit_omniMulti_version)
        
        
        self.spacer_horizontal = QSpacerItem(100,10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout_release.addItem(self.spacer_horizontal)
        
        self.create_layouts(final_list)
        
    def create_all_checkboxes(self):
        self.checkbox_compativel_mycommerce = self.create_checkbox(
            text="Compatível"
        )
        self.checkbox_compativel_omniMulti = self.create_checkbox(
            text="Compatível"
        )

    def create_all_labels(self):
        self.label_mycommerce = self.create_label(
            text="MyCommerce: "
        ) 
        self.label_omniMulti = self.create_label(
            text="OmniMulti: "
        )
        
        
        self.label_version_myzap = self.create_label(
            text="Versão do Robô MyZap: "
        )
        self.label_version_vsServices_MyZap = self.create_label(
            text="Versão do vsServices MyZap: "
        )

    def create_all_line_edits(self):
        self.line_edit_mycommerce_version = self.create_line_edit(
            placeholder="versão do MyCommerce",
            set_text=self.latest_version_handler.latest_release_version_text()
        )
        
        self.line_edit_omniMulti_version = self.create_line_edit(
            placeholder="versão do OmniMulti",
            set_text=""
        )
        
        self.line_edit_version_myzap_release = self.create_line_edit(
            placeholder="versão do MyZap",
            set_text=self.latest_version_handler.latest_release_version_text_myzap()
        )
        self.line_edit_version_vsServices_MyZap = self.create_line_edit(
            placeholder="versão do vsServices MyZap",
            set_text=self.latest_version_handler.latest_release_version_text_myzap()
        )
        self.process_input(self.line_edit_omniMulti_version)
        self.process_input(self.line_edit_version_myzap_release)
        self.process_input(self.line_edit_mycommerce_version)
        self.process_input(self.line_edit_version_vsServices_MyZap)
        
        
        # passa para o proximo line_edit quando o usuario pressionar enter
        self.line_edit_return_pressed(self.line_edit_omniMulti_version, self.line_edit_version_myzap_release)
        self.line_edit_return_pressed(self.line_edit_version_myzap_release, self.line_edit_version_vsServices_MyZap) 
        self.line_edit_return_pressed(self.line_edit_version_vsServices_MyZap, self.line_edit_mycommerce_version) 
        self.line_edit_return_pressed(self.line_edit_mycommerce_version, self.line_edit_omniMulti_version)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = WidgetReleaseMyZap()
    window.show()
    app.exec()