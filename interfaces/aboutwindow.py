from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QApplication

from interfaces.base_window import BaseWindow

class AboutProgramWindow(BaseWindow):
    def __init__(self, parent=None):
        super(AboutProgramWindow, self).__init__(parent)
        self.github_icon_path = r'images/github.png'
        self.oakbox_icon_path = r'images/oakbox.png'
        self.keyPressEvent = self.key_pressed_handle
        self.setup_ui()

    def setup_ui(self):
        self.config_imgs()
        self.setWindowTitle('Sobre o Programa')
        self.setFixedSize(400, 300)
        self.setWindowModality(Qt.WindowModal)
        
        self.button_git = self.create_button(
            config_style=False,
            text='Visite Meu Github',
            function=lambda: self.open_browser_link('https://github.com/vbsx'),
            icon=self.github_icon
        )

        self.visit_websites_button = self.create_button(
            config_style=False,
            text='Visite Meu Site',
            function=lambda: self.open_browser_link(r'https://oakbox.com.br'),
            icon=self.oakbox_icon
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()

        self.layout_vertical_version = QHBoxLayout()
        self.label_version = QLabel('Versão 1.13')
        self.layout_vertical_version.addWidget(self.label_version, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout_principal.addWidget(self.visit_websites_button, alignment=Qt.AlignCenter)
        self.layout_principal.addWidget(self.button_git, alignment=Qt.AlignCenter)
        self.layout_principal.addLayout(self.layout_vertical_version)

        self.central_widget.setLayout(self.layout_principal)

    def config_imgs(self):
        has_image_folder = self.file_handler.verify_if_images_path_exists()
        if not has_image_folder:
            self.github_icon = QIcon(self.resource_path(self.github_icon_path))
            self.oakbox_icon = QIcon(self.resource_path(self.oakbox_icon_path))
        else:
            self.github_icon = QIcon(self.github_icon_path)
            self.oakbox_icon = QIcon(self.oakbox_icon_path)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    about_program_window = AboutProgramWindow()
    about_program_window.show()
    sys.exit(app.exec())
