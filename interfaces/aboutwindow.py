import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from interfaces.base_window import BaseWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton,QLabel, QVBoxLayout, QWidget, QHBoxLayout
from webbrowser import open_new_tab 

class AboutProgramWindow(BaseWindow):
    def __init__(self, parent = None):
        super(AboutProgramWindow, self).__init__(parent)
        self.github_icon = self.resource_path(r'images/github.png')
        self.oakbox_icon = self.resource_path(r'images/oakbox.png')
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('About')
        self.setFixedSize(400, 300)
        self.button_git = QPushButton('Visite Meu Github')
        self.button_git.clicked.connect(lambda: self.open_browser_link('https://github.com/vbsx'))
        self.button_git.setIcon(QIcon(self.github_icon))
        self.button_git.setIconSize(QSize(64,64))
        
        self.visit_websites_button = QPushButton('Visite Meus Site')
        self.visit_websites_button.clicked.connect(lambda: self.open_browser_link(r'https://oakbox.com.br'))
        self.visit_websites_button.setIcon(QIcon(self.oakbox_icon))
        self.visit_websites_button.setIconSize(QSize(64,64))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout()
        
        self.layout_vertical_version = QHBoxLayout()
        self.label_version = QLabel('Versão 1.0')
        self.layout_vertical_version.addWidget(self.label_version, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.layout_principal.addWidget(self.visit_websites_button)
        self.layout_principal.addWidget(self.button_git)
        self.layout_principal.addLayout(self.layout_vertical_version)
        
        self.central_widget.setLayout(self.layout_principal)
        
    def open_browser_link(self, link):
        open_new_tab(
        link
        )

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    about_program_window = AboutProgramWindow()
    about_program_window.show()
    sys.exit(app.exec())   