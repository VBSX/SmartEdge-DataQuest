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

class WidgetReleaseMyfrota(BaseWindow):
    def __init__(self, parent=None):
        super(WidgetReleaseMyfrota, self).__init__(parent)
        self.latest_version_handler = LatestVersion()
        self.setup_ui()
    
    def setup_ui(self):
        self.horizontal_layout_release = QHBoxLayout()
        self.horizontal_layout_mycommerce = QHBoxLayout()
        
        final_list =[
            self.horizontal_layout_release,
            self.horizontal_layout_mycommerce
            ]
        
        self.create_all_checkboxes()
        self.create_all_labels()
        self.create_all_line_edits()
        
        self.spacer_horizontal = QSpacerItem(100,100, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_layout_release.addItem(self.spacer_horizontal)
        
        self.create_layouts(final_list)
        
    def create_all_checkboxes(self):
        self.checkbox_compativel_mycommerce = self.create_checkbox(
            text="Compatível"
        )
        self.horizontal_layout_mycommerce.addWidget(self.checkbox_compativel_mycommerce)
        
    def create_all_labels(self):
        self.label_mycommerce = self.create_label(
            text="MyCommerce: ")
        self.horizontal_layout_mycommerce.addWidget(self.label_mycommerce)
        
        
        self.label_version_myfrota = self.create_label(
            text="Versão do MyFrota: "
        )
        self.horizontal_layout_release.addWidget(self.label_version_myfrota)
        
    def create_all_line_edits(self):
        self.line_edit_mycommerce_version = self.create_line_edit(
            placeholder="versão do MyCommerce",
            set_text=self.latest_version_handler.latest_release_version_text()
        )
        self.horizontal_layout_mycommerce.addWidget(self.line_edit_mycommerce_version)
        
        self.line_edit_version_myfrota_release = self.create_line_edit(
            placeholder="versão do MyFrota",
            set_text=self.latest_version_handler.latest_release_version_text_myfrota()
        )
        self.horizontal_layout_release.addWidget(self.line_edit_version_myfrota_release)
        
        self.process_input(self.line_edit_version_myfrota_release)
        self.process_input(self.line_edit_mycommerce_version)
        
        # passa para o proximo line_edit quando o usuario pressionar enter
        self.line_edit_return_pressed(self.line_edit_mycommerce_version, self.line_edit_version_myfrota_release)
        self.line_edit_return_pressed(self.line_edit_version_myfrota_release, self.line_edit_mycommerce_version)     

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = WidgetReleaseMyfrota()
    window.show()
    app.exec()