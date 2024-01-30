import os
import sys
path = os.path.abspath('./')
from PySide6.QtWidgets import (
    QHBoxLayout,
    QApplication,
    QComboBox
    )

from base_window import BaseWindow

class SovisWindow(BaseWindow):
    def __init__(self, parent=None):
        super(SovisWindow, self).__init__(parent)
        self.list_of_layouts = []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Sovis") 
        self.width = 800
        self.height = 600
    
        self.horizontal_layout_import_order = QHBoxLayout()
        self.list_of_layouts.append(self.horizontal_layout_import_order)
        #
        self.horizontal_layout_change_id_order = QHBoxLayout()
        self.list_of_layouts.append(self.horizontal_layout_change_id_order)
        
        
        self.create_all_labels()
        self.create_all_line_edits()
        self.create_all_combobox()
        self.create_all_buttons()
        
        self.create_layouts(self.list_of_layouts)
        
    def create_all_line_edits(self):
        self.line_edit_order_number = self.create_line_edit(
            placeholder='',
            mask=False,
            limit_char=8
        )
        self.horizontal_layout_import_order.addWidget(self.line_edit_order_number)
        
    def create_all_labels(self):
        self.label_import_order_number = self.create_label(
            text='Coloque o número do pedido'
        )
        self.horizontal_layout_import_order.addWidget(self.label_import_order_number)
        #
        self.label_change_id_order = self.create_label(
            'Mudar o ID do pedido (IDTIPOPEDIDO)'
        )
        self.horizontal_layout_change_id_order.addWidget(self.label_change_id_order)
        #
        
    def create_all_buttons(self):
        self.button_import_order = self.create_button(
            text='Importar',
            function=self.import_order
        )
        self.horizontal_layout_import_order.addWidget(self.button_import_order)
        
    def create_all_combobox(self):
        self.combobox_ids_order = QComboBox()
        for item in range(1,10):
            self.combobox_ids_order.addItems(str(item))
     
        self.horizontal_layout_change_id_order.addWidget(self.combobox_ids_order)

    def import_order(self):
        pass

if __name__=='__main__':
    app = QApplication(sys.argv)
    sovis = SovisWindow()
    sovis.show()
    app.exec()