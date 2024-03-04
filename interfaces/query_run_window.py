from PySide6.QtWidgets import QLabel,QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from components.dbhandle import Database
import re
from re import (compile, IGNORECASE)
from interfaces.base_window import BaseWindow

class QueryWindow(BaseWindow):
    def __init__(self, parent=None):
        super(QueryWindow, self).__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Query")
        self.resize(400, 400)
        self.table_widget = QTableWidget(self)
        
        self.label_query = QLabel("Query")
        
        self.line_edit_query = QLineEdit()
        self.line_edit_query.setPlaceholderText("Insert Query")
        
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.start_query)
        # when press enter, activate button start
        self.line_edit_query.returnPressed.connect(self.button_start.click)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_principal = QVBoxLayout()
        central_widget.setLayout(layout_principal)
        
        layout_principal.addWidget(self.label_query)
        layout_principal.addWidget(self.line_edit_query)
        layout_principal.addWidget(self.button_start)
        layout_principal.addWidget(self.table_widget)
        self.show()

    def start_query(self):
        db = Database()
        query = self.line_edit_query.text()
        pattern = compile(r'select', IGNORECASE)
        match = pattern.search(query)
        if match:
            return_db = db.execute_query_return(query)
            result, return_query = return_db
            if result == 'sucess':
                print(return_db)
                self.show_content_table(return_query)
            elif result == 'error':
                self.show_dialog(str(return_query))
        else:
            return_db = db.execute_query(query)
            if return_db == 'sucess':
                self.show_dialog('Query Executed')
            else:
                self.show_dialog(str(return_db))

    def show_content_table(self, content_table):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(content_table))
        self.table_widget.setColumnCount(len(content_table[0]))
        self.table_widget.setHorizontalHeaderLabels(content_table[0])
        for i in range(len(content_table)):
            for j in range(len(content_table[0])):
                item = QTableWidgetItem(str(content_table[i][j]))
                self.table_widget.setItem(i, j, item)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.table_widget.show()
        
if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = QueryWindow()
    sys.exit(app.exec())