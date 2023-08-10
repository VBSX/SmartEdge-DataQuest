from PySide6.QtWidgets import QMainWindow, QLabel,QWidget, QVBoxLayout, QPushButton,QMessageBox, QLineEdit, QTableWidget
from dbhandle import Database
import re
class QueryWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QueryWindow, self).__init__(parent)
        self.setup_ui()
        self.setWindowTitle("Query")


    def setup_ui(self):
        self.setWindowTitle("Query")
        self.resize(400, 400)
        
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
        self.show()

    def start_query(self):
        db = Database()
        query = self.line_edit_query.text()
        pattern = re.compile(r'select')
        match = pattern.search(query)
        if match:
            return_db = db.execute_query(query)
            if return_db == 'sucess':
                self.show_content_table(db.get_content_table())
        
        return_db = db.execute_query(query)
        if return_db == 'sucess':
            self.show_dialog('Query Executed')
        else:
            self.show_dialog(str(return_db))

    def show_dialog(self, text):
        QMessageBox.about(self, 'DIALOG', text)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = QueryWindow()
    sys.exit(app.exec())