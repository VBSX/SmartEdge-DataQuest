from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from PySide6.QtWidgets import (
    QHBoxLayout,
    QApplication,
    QComboBox
    )

from interfaces.base_window import BaseWindow

class SovisWindow(BaseWindow):
    def __init__(self, parent=None):
        super(SovisWindow, self).__init__(parent)
        self.list_of_layouts = []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Sovis") 
        width = 600
        height = 300
        self.setFixedSize(width, height)
        self.get_configs()
        self.horizontal_layout_import_order = QHBoxLayout()
        self.list_of_layouts.append(self.horizontal_layout_import_order)
        #
        self.horizontal_layout_change_id_order = QHBoxLayout()
        self.list_of_layouts.append(self.horizontal_layout_change_id_order)
        
        self.horizontal_layout_buttons_actions = QHBoxLayout()
        self.list_of_layouts.append(self.horizontal_layout_buttons_actions)
        
        self.create_all_labels()
        self.create_all_line_edits()
        self.create_all_combobox()
        self.create_all_buttons()
        
        self.create_layouts(self.list_of_layouts)
        
    def create_all_line_edits(self):
        self.line_edit_order_number = self.create_line_edit(
            placeholder='',
            mask=False,
            limit_char=8,
            only_number=True,
            fixed_size=True
        )
        self.line_edit_order_number.textChanged.connect(self.update_type_id_combo)
        self.horizontal_layout_import_order.addWidget(self.line_edit_order_number)
        
    def create_all_labels(self):
        self.label_import_order_number = self.create_label(
            text='Coloque o número do pedido'
        )
        self.horizontal_layout_import_order.addWidget(self.label_import_order_number)
        #
        self.label_change_id_order = self.create_label(
            'IDTipoPedido'
        )
        self.horizontal_layout_change_id_order.addWidget(self.label_change_id_order)
        #
        self.label_id_changed_description = self.create_label(
            '',
            is_hidden=True
        )
        self.horizontal_layout_change_id_order.addWidget(self.label_id_changed_description)
        
    def create_all_buttons(self):
        self.button_import_order = self.create_button(
            text='Importar',
            function=self.import_order
        )
        self.horizontal_layout_buttons_actions.addWidget(self.button_import_order)
        
        self.button_change_id_order = self.create_button(
            text='Mudar o ID do pedido (IDTIPOPEDIDO)',
            function=self.change_id_order
        )
        self.horizontal_layout_buttons_actions.addWidget(self.button_change_id_order)   
        
    def create_all_combobox(self):
        self.combobox_ids_order = QComboBox()
        for item in range(1,10):
            self.combobox_ids_order.addItems(str(item))
        
        self.update_type_id_combo()
        self.combobox_ids_order.currentIndexChanged.connect(self.combobox_id_order_set_description)
        self.horizontal_layout_change_id_order.addWidget(self.combobox_ids_order)

    def combobox_id_order_set_description(self):
        list_of_descriptions = [
            'Venda (Importação Manual) ',
            'TROCA',
            'BONIFICAÇÃO(Monitor Faturamento) ',
            'NOTA REMESSA ',
            'NOTA REMESSA NÃO FATURA ' ,
            'BONIFICAÇÃO MONITOR ' ,
            'PERDA ',
            'NFCe ',
            'PRÉ-VENDA (Monitor Faturamento) '
            ]
        # usa o range para preencher a lista de ids com os números de 1 a 9
        list_of_ids = list(range(0,9))

        for index in list_of_ids:
            if self.combobox_ids_order.currentIndex() == index:
                self.label_id_changed_description.setText(list_of_descriptions[index])
                self.label_id_changed_description.show()
                break
    
    def import_order(self):
        order_number = self.line_edit_order_number.text()
        if order_number != '':
            db_return, order_return = self.db.get_sovis_order(order_number)
            if db_return =='sucess' and order_return:
                self.db.import_sovis_order(order_number)
                self.show_dialog('Pedido importado com sucesso')
            else:
                self.show_dialog('Pedido não encontrado')
        else:   
            self.show_dialog('Preencha o campo pedido')
    
    def change_id_order(self):
        id_type_order = self.combobox_ids_order.currentIndex() + 1
        order_number = self.line_edit_order_number.text()
        if order_number != '':
            db_return, order_return = self.db.get_sovis_order(order_number)
            if db_return == 'sucess' and order_return:
                self.db.update_type_id_order_sovis(order_number, id_type_order)
                for index in range(1,10):
                    if id_type_order == index:
                        self.db.update_type_id_itens_order_sovis(order_number, index)
                        self.show_dialog('IDTIPOPEDIDO alterado com sucesso')
                        break       
            else:
                self.show_dialog('Pedido não encontrado')
        else:
            self.show_dialog('Preencha o campo pedido')
    
    def details_of_order(self):
        pass
    
    def update_type_id_combo(self): 
        order_number = self.line_edit_order_number.text()
        if order_number:
            db_return, id_type_order_db = self.db.get_type_id_order_sovis(order_number)
            if db_return == 'sucess' and id_type_order_db:
                index = int(id_type_order_db[0][0])
                self.combobox_ids_order.setCurrentIndex(index-1)
        self.combobox_id_order_set_description()
        

if __name__=='__main__':
    from sys import argv
    app = QApplication(argv)
    sovis = SovisWindow()
    sovis.show()
    app.exec()